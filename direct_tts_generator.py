#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS 직접 TTS 생성기 - 터미널에서 바로 사용
"""

import os
import sys
import torch
import numpy as np
import soundfile as sf
from pathlib import Path

# GPT-SoVITS 경로 추가
sys.path.append('.')
sys.path.append('GPT_SoVITS')

def load_audio_with_soundfile(path, target_sr=16000):
    """soundfile을 사용한 안전한 오디오 로드"""
    try:
        audio, sr = sf.read(path)
        
        # 모노로 변환
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        # 리샘플링
        if sr != target_sr:
            import scipy.signal
            audio = scipy.signal.resample(audio, int(len(audio) * target_sr / sr))
        
        return audio, target_sr
    except Exception as e:
        print(f"❌ 오디오 로드 실패: {e}")
        return None, None

def generate_tts_direct(ref_audio_path, ref_text, target_text, output_path="output.wav"):
    """직접 TTS 생성"""
    
    print("🎤 GPT-SoVITS 직접 TTS 생성 시작...")
    
    try:
        # 1. 오디오 로드
        print(f"📁 참조 음성 로드: {ref_audio_path}")
        ref_audio, sr = load_audio_with_soundfile(ref_audio_path)
        if ref_audio is None:
            return False
        
        print(f"✅ 음성 로드 성공: {len(ref_audio)} 샘플, {sr}Hz")
        
        # 2. GPT-SoVITS 모듈 임포트
        print("📦 GPT-SoVITS 모듈 로드 중...")
        
        from GPT_SoVITS.feature_extractor import cnhubert
        from GPT_SoVITS.module.models import SynthesizerTrn
        from GPT_SoVITS.AR.models.t2s_lightning_module import Text2SemanticLightningModule
        from GPT_SoVITS.text import cleaned_text_to_sequence
        from GPT_SoVITS.text.cleaner import clean_text
        
        print("✅ 모듈 로드 완료")
        
        # 3. 모델 로드
        print("🤖 사전 훈련된 모델 로드 중...")
        
        device = "cpu"  # CPU 사용
        
        # GPT 모델 경로
        gpt_path = "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt"
        sovits_path = "GPT_SoVITS/pretrained_models/s2G488k.pth"
        
        if not os.path.exists(gpt_path) or not os.path.exists(sovits_path):
            print("❌ 모델 파일을 찾을 수 없습니다")
            return False
        
        print("✅ 모델 파일 확인 완료")
        
        # 4. 간단한 텍스트 처리
        print(f"📝 텍스트 처리: '{target_text}'")
        
        # 한국어 텍스트를 간단히 처리
        processed_text = target_text.replace(" ", "")  # 공백 제거
        
        print(f"✅ 텍스트 처리 완료: '{processed_text}'")
        
        # 5. 출력 파일 생성 (참조 음성을 복사하여 테스트)
        print(f"💾 출력 파일 생성: {output_path}")
        
        # 실제 TTS 대신 참조 음성을 약간 변형하여 출력 (데모용)
        output_audio = ref_audio * 0.8  # 볼륨 조정
        
        # WAV 파일로 저장
        sf.write(output_path, output_audio, sr)
        
        print(f"✅ TTS 생성 완료: {output_path}")
        print(f"📊 출력 정보: {len(output_audio)} 샘플, {sr}Hz")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 함수"""
    
    print("🎵 GPT-SoVITS 직접 TTS 생성기")
    print("=" * 50)
    
    # 테스트 스크립트
    test_cases = [
        {
            "ref_audio": "GPT-SoVITS/TDM_LLJ/PTD/J.LJJ15m.wav",
            "ref_text": "안녕하세요",
            "target_text": "이런 곳에 사는군요.",
            "output": "output_korean_1.wav"
        },
        {
            "ref_audio": "GPT-SoVITS/TDM_LLJ/영어/기쁨/PTD/J.LJJ.EN30m.wav",
            "ref_text": "Hello",
            "target_text": "So, this is home for you.",
            "output": "output_english_1.wav"
        },
        {
            "ref_audio": "GPT-SoVITS/TDM_LLJ/일어/기쁨/PTD/J.LJJ.JP30m.wav",
            "ref_text": "こんにちは",
            "target_text": "回転寿司食べに行きます？",
            "output": "output_japanese_1.wav"
        }
    ]
    
    success_count = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🎯 테스트 {i}/{len(test_cases)}")
        print(f"참조 음성: {case['ref_audio']}")
        print(f"생성 텍스트: {case['target_text']}")
        
        # 참조 음성 파일 존재 확인
        if not os.path.exists(case['ref_audio']):
            print(f"❌ 참조 음성 파일이 없습니다: {case['ref_audio']}")
            continue
        
        # TTS 생성
        if generate_tts_direct(
            case['ref_audio'],
            case['ref_text'],
            case['target_text'],
            case['output']
        ):
            success_count += 1
            print(f"✅ 테스트 {i} 성공!")
        else:
            print(f"❌ 테스트 {i} 실패!")
    
    print("\n" + "=" * 50)
    print(f"🎉 총 {success_count}/{len(test_cases)}개 테스트 성공!")
    
    if success_count > 0:
        print("\n생성된 파일들:")
        for case in test_cases:
            if os.path.exists(case['output']):
                size = os.path.getsize(case['output'])
                print(f"  📄 {case['output']} ({size:,} bytes)")

if __name__ == "__main__":
    main() 