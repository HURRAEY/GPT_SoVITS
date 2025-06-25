#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import torch
import soundfile as sf
import numpy as np
from pathlib import Path

# GPT_SoVITS 경로 추가
sys.path.append('GPT_SoVITS')

def load_audio(file_path):
    """오디오 파일 로드"""
    try:
        audio, sr = sf.read(file_path)
        if len(audio.shape) > 1:
            audio = audio[:, 0]  # 모노로 변환
        return audio, sr
    except Exception as e:
        print(f"오디오 로드 실패: {e}")
        return None, None

def test_audio_loading():
    """TDM_LLJ 오디오 파일들 테스트"""
    audio_files = [
        "TDM_LLJ/PTD/J.LJJ15m.wav",  # 기쁨
        "TDM_LLJ/SAD/J.LJJ15m.wav",  # 슬픔
        "TDM_LLJ/ANG/J.LJJ15m.wav",  # 화남
        "TDM_LLJ/DEP/J.LJJ15m.wav",  # 우울
    ]
    
    emotions = ["기쁨", "슬픔", "화남", "우울"]
    
    print("=== TDM_LLJ 감정별 음성 파일 테스트 ===")
    
    for i, (file_path, emotion) in enumerate(zip(audio_files, emotions)):
        if os.path.exists(file_path):
            audio, sr = load_audio(file_path)
            if audio is not None:
                duration = len(audio) / sr
                print(f"✅ {emotion}: {file_path}")
                print(f"   - 길이: {duration:.2f}초")
                print(f"   - 샘플레이트: {sr}Hz")
                print(f"   - 크기: {len(audio)} 샘플")
            else:
                print(f"❌ {emotion}: 로드 실패 - {file_path}")
        else:
            print(f"❌ {emotion}: 파일 없음 - {file_path}")
        print()

def test_basic_imports():
    """기본 모듈 import 테스트"""
    print("=== 기본 모듈 Import 테스트 ===")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except Exception as e:
        print(f"❌ PyTorch 로드 실패: {e}")
    
    try:
        import soundfile as sf
        print("✅ SoundFile: 정상")
    except Exception as e:
        print(f"❌ SoundFile 로드 실패: {e}")
    
    try:
        import librosa
        print(f"✅ Librosa: {librosa.__version__}")
    except Exception as e:
        print(f"❌ Librosa 로드 실패: {e}")
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except Exception as e:
        print(f"❌ Transformers 로드 실패: {e}")
    
    print()

def create_test_tts():
    """간단한 TTS 테스트 텍스트 생성"""
    test_texts = [
        "안녕하세요, 저는 GPT-SoVITS입니다.",
        "감정 표현이 가능한 음성 합성 시스템이에요.",
        "Hello, this is a test for English speech synthesis.",
        "こんにちは、日本語の音声合成テストです。"
    ]
    
    print("=== 테스트 텍스트 ===")
    for i, text in enumerate(test_texts, 1):
        print(f"{i}. {text}")
    print()

def main():
    print("🎵 GPT-SoVITS 터미널 테스트 시작 🎵\n")
    
    # 1. 기본 모듈 테스트
    test_basic_imports()
    
    # 2. 오디오 파일 테스트
    test_audio_loading()
    
    # 3. 테스트 텍스트 표시
    create_test_tts()
    
    print("=== 환경 정보 ===")
    print(f"Python 버전: {sys.version}")
    print(f"현재 디렉토리: {os.getcwd()}")
    print(f"CUDA 사용 가능: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA 디바이스: {torch.cuda.get_device_name()}")
    else:
        print("CPU 모드로 실행")
    
    print("\n🎉 테스트 완료!")
    print("WebUI는 http://localhost:9874 에서 접속 가능합니다.")

if __name__ == "__main__":
    main() 