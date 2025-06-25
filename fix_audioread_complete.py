#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audioread 패키지 완전 패치 - Python 3.13 호환성
"""

import sys
import os
from pathlib import Path

def patch_audioread_init():
    """audioread __init__.py 패치"""
    
    # audioread __init__.py 경로 찾기
    site_packages = None
    for path in sys.path:
        if 'site-packages' in path and 'gpt_sovits_env' in path:
            site_packages = Path(path)
            break
    
    if not site_packages:
        print("❌ site-packages 경로를 찾을 수 없습니다.")
        return False
    
    init_file = site_packages / 'audioread' / '__init__.py'
    
    if not init_file.exists():
        print(f"❌ __init__.py 파일을 찾을 수 없습니다: {init_file}")
        return False
    
    try:
        # 원본 파일 백업
        backup_file = init_file.with_suffix('.py.backup2')
        if not backup_file.exists():
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 원본 파일 백업: {backup_file}")
        
        # 패치된 내용 작성
        patched_content = '''# This file is part of audioread.
# Copyright 2011, Adrian Sampson.
# Patched for Python 3.13 compatibility

"""Decode audio files using whichever backend is available."""

import os
import sys

__version__ = '3.0.1'

class DecodeError(Exception):
    """Base class for all decoding errors raised by this library."""
    pass

def available_backends():
    """Get a list of available audio decoding backends."""
    backends = []
    
    # Always prefer soundfile if available
    try:
        import soundfile
        backends.append('soundfile')
    except ImportError:
        pass
    
    # Try other backends
    try:
        from . import ffdec
        backends.append('ffdec')
    except ImportError:
        pass
    
    try:
        from . import maddec
        backends.append('maddec')
    except ImportError:
        pass
    
    try:
        from . import gstdec
        backends.append('gstdec')
    except ImportError:
        pass
    
    # Only try rawread if aifc is available (skip for Python 3.13)
    try:
        import aifc
        from . import rawread
        backends.append('rawread')
    except (ImportError, ModuleNotFoundError):
        # Skip rawread for Python 3.13
        pass
    
    return tuple(backends)

def audio_open(path, backends=None):
    """Open an audio file using the first working backend."""
    if backends is None:
        backends = available_backends()
    
    if not backends:
        raise DecodeError("no audio backends available")
    
    for backend_name in backends:
        if backend_name == 'soundfile':
            try:
                import soundfile as sf
                return SoundFileAudioFile(path)
            except Exception:
                continue
        elif backend_name == 'ffdec':
            try:
                from . import ffdec
                return ffdec.FFmpegAudioFile(path)
            except Exception:
                continue
        elif backend_name == 'maddec':
            try:
                from . import maddec
                return maddec.MadAudioFile(path)
            except Exception:
                continue
        elif backend_name == 'gstdec':
            try:
                from . import gstdec
                return gstdec.GstAudioFile(path)
            except Exception:
                continue
        elif backend_name == 'rawread':
            try:
                from . import rawread
                return rawread.RawAudioFile(path)
            except Exception:
                continue
    
    raise DecodeError("no audio backends succeeded")

class SoundFileAudioFile:
    """Audio file using soundfile backend."""
    
    def __init__(self, filename):
        import soundfile as sf
        self._sf = sf
        self._file = sf.SoundFile(filename)
        
    def close(self):
        self._file.close()
        
    @property
    def channels(self):
        return self._file.channels
        
    @property
    def samplerate(self):
        return self._file.samplerate
        
    @property
    def duration(self):
        return len(self._file) / self._file.samplerate
        
    def read_data(self, block_samples=1024):
        """Generate blocks of audio data."""
        while True:
            data = self._file.read(block_samples, dtype='int16')
            if len(data) == 0:
                break
            # Convert to bytes
            yield data.tobytes()
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
        
    def __iter__(self):
        return self.read_data()

# Backwards compatibility
open = audio_open
'''
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(patched_content)
        
        print(f"✅ audioread __init__.py 패치 완료: {init_file}")
        return True
        
    except Exception as e:
        print(f"❌ audioread __init__.py 패치 실패: {e}")
        return False

def create_librosa_config():
    """librosa가 soundfile을 우선 사용하도록 설정"""
    
    try:
        import librosa
        librosa_path = Path(librosa.__file__).parent
        
        # librosa 설정 파일 생성
        config_content = '''# librosa configuration for Python 3.13 compatibility
import os
os.environ['LIBROSA_CACHE_DIR'] = '/tmp/librosa_cache'

# Force soundfile backend
import soundfile
'''
        
        config_file = librosa_path / 'librosa_config.py'
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"✅ librosa 설정 파일 생성: {config_file}")
        return True
        
    except Exception as e:
        print(f"❌ librosa 설정 실패: {e}")
        return False

def install_missing_packages():
    """누락된 패키지들 설치"""
    
    import subprocess
    
    packages = [
        'ffmpeg-python',
        'pydub',
        'resampy',
        'numba',
        'llvmlite',
        'cffi',
        'soundfile',
        'soxr'
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            print(f"✅ {package} 설치 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 설치 실패: {e}")

def main():
    print("🔧 audioread 완전 패치 적용 중...")
    
    success = True
    
    # 누락된 패키지들 설치
    print("📦 누락된 패키지들 설치 중...")
    install_missing_packages()
    
    # audioread __init__.py 패치
    if not patch_audioread_init():
        success = False
    
    # librosa 설정
    if not create_librosa_config():
        success = False
    
    if success:
        print("✅ 모든 패치가 성공적으로 적용되었습니다!")
        print("이제 최고 품질의 TTS를 사용할 수 있습니다!")
    else:
        print("❌ 일부 패치가 실패했습니다.")

if __name__ == "__main__":
    main() 