#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3.13에서 제거된 aifc 모듈 문제 해결을 위한 패치
"""

import sys
import os
from pathlib import Path

def create_aifc_stub():
    """aifc 모듈 스텁 생성"""
    
    # 가상환경의 site-packages 경로 찾기
    site_packages = None
    for path in sys.path:
        if 'site-packages' in path and 'gpt_sovits_env' in path:
            site_packages = Path(path)
            break
    
    if not site_packages:
        print("❌ site-packages 경로를 찾을 수 없습니다.")
        return False
    
    # aifc.py 스텁 파일 생성
    aifc_stub_content = '''# aifc module stub for Python 3.13 compatibility
import wave
import struct

# aifc 모듈의 주요 클래스와 함수들을 wave 모듈로 대체
Error = wave.Error

def open(filename, mode='rb'):
    """aifc.open을 wave.open으로 대체"""
    return wave.open(filename, mode)

# 기타 필요한 상수들
NONE = 'NONE'
'''
    
    aifc_file = site_packages / 'aifc.py'
    
    try:
        with open(aifc_file, 'w', encoding='utf-8') as f:
            f.write(aifc_stub_content)
        print(f"✅ aifc 스텁 모듈 생성: {aifc_file}")
        return True
    except Exception as e:
        print(f"❌ aifc 스텁 모듈 생성 실패: {e}")
        return False

def patch_audioread():
    """audioread rawread.py 패치"""
    
    # audioread rawread.py 경로 찾기
    site_packages = None
    for path in sys.path:
        if 'site-packages' in path and 'gpt_sovits_env' in path:
            site_packages = Path(path)
            break
    
    if not site_packages:
        print("❌ site-packages 경로를 찾을 수 없습니다.")
        return False
    
    rawread_file = site_packages / 'audioread' / 'rawread.py'
    
    if not rawread_file.exists():
        print(f"❌ rawread.py 파일을 찾을 수 없습니다: {rawread_file}")
        return False
    
    try:
        # 원본 파일 백업
        backup_file = rawread_file.with_suffix('.py.backup')
        if not backup_file.exists():
            rawread_file.rename(backup_file)
            print(f"✅ 원본 파일 백업: {backup_file}")
        
        # 패치된 내용 작성
        patched_content = '''# This file is part of audioread.
# Copyright 2011, Adrian Sampson.
# Patched for Python 3.13 compatibility

"""Uses standard-library modules to read AIFF, AIFF-C, and WAV files."""
try:
    import aifc
except ImportError:
    # Python 3.13에서 aifc가 제거되었으므로 wave로 대체
    import wave as aifc
    aifc.Error = Exception

import audioop
import struct
import sunau
import wave

from .exceptions import DecodeError
from .base import AudioFile

# Produce two-byte (16-bit) output samples.
TARGET_WIDTH = 2

# Python 3.4 added support for 24-bit (3-byte) samples.
SUPPORTED_WIDTHS = (1, 2, 3, 4)


class UnsupportedError(DecodeError):
    """File is not an AIFF, WAV, or Au file."""


class BitWidthError(DecodeError):
    """The file uses an unsupported bit width."""


def byteswap(s):
    """Swaps the endianness of the bytestring s, which must be an array
    of shorts (16-bit signed integers). This is probably less efficient
    than it should be.
    """
    assert len(s) % 2 == 0
    parts = []
    for i in range(0, len(s), 2):
        chunk = s[i:i + 2]
        newchunk = struct.pack('<h', *struct.unpack('>h', chunk))
        parts.append(newchunk)
    return b''.join(parts)


class RawAudioFile(AudioFile):
    """An AIFF, WAV, or Au file that can be read by the Python standard
    library modules ``wave``, ``aifc``, and ``sunau``.
    """
    def __init__(self, filename):
        self._fh = open(filename, 'rb')

        # WAV 파일 먼저 시도 (가장 일반적)
        try:
            self._file = wave.open(self._fh)
        except wave.Error:
            self._fh.seek(0)
        else:
            self._needs_byteswap = False
            self._check()
            return

        # AIFF 파일 시도 (aifc 대신 wave 사용)
        try:
            self._file = aifc.open(self._fh)
        except (aifc.Error, Exception):
            self._fh.seek(0)
        else:
            self._needs_byteswap = True
            self._check()
            return

        # AU 파일 시도
        try:
            self._file = sunau.open(self._fh)
        except sunau.Error:
            self._fh.seek(0)
        else:
            self._needs_byteswap = True
            self._check()
            return

        # None of the three libraries could open the file.
        self._fh.close()
        raise UnsupportedError()

    def _check(self):
        """Check that the files' parameters allow us to decode it and
        raise an error otherwise.
        """
        if self._file.getsampwidth() not in SUPPORTED_WIDTHS:
            self.close()
            raise BitWidthError()

    def close(self):
        """Close the underlying file."""
        self._file.close()
        self._fh.close()

    @property
    def channels(self):
        """Number of audio channels."""
        return self._file.getnchannels()

    @property
    def samplerate(self):
        """Sample rate in Hz."""
        return self._file.getframerate()

    @property
    def duration(self):
        """Length of the audio in seconds (a float)."""
        return float(self._file.getnframes()) / self.samplerate

    def read_data(self, block_samples=1024):
        """Generates blocks of PCM data found in the file."""
        old_width = self._file.getsampwidth()

        while True:
            data = self._file.readframes(block_samples)
            if not data:
                break

            # Make sure we have the desired bitdepth and endianness.
            data = audioop.lin2lin(data, old_width, TARGET_WIDTH)
            if self._needs_byteswap and hasattr(self._file, 'getcomptype') and self._file.getcomptype() != 'sowt':
                # Big-endian data. Swap endianness.
                data = byteswap(data)
            yield data

    # Context manager.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    # Iteration.
    def __iter__(self):
        return self.read_data()
'''
        
        with open(rawread_file, 'w', encoding='utf-8') as f:
            f.write(patched_content)
        
        print(f"✅ audioread rawread.py 패치 완료: {rawread_file}")
        return True
        
    except Exception as e:
        print(f"❌ audioread 패치 실패: {e}")
        return False

def main():
    print("🔧 Python 3.13 호환성 패치 적용 중...")
    
    success = True
    
    # aifc 스텁 모듈 생성
    if not create_aifc_stub():
        success = False
    
    # audioread 패치
    if not patch_audioread():
        success = False
    
    if success:
        print("✅ 모든 패치가 성공적으로 적용되었습니다!")
        print("이제 GPT-SoVITS를 다시 실행해보세요.")
    else:
        print("❌ 일부 패치가 실패했습니다.")

if __name__ == "__main__":
    main() 