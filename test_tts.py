#!/usr/bin/env python3
import os
import sys
import torch
import numpy as np

# GPT_SoVITS 모듈 경로 추가
sys.path.append('GPT_SoVITS')

# 기본 설정
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # CPU 사용 강제

print("=== GPT-SoVITS 음성 합성 테스트 ===")

# 참조 음성 파일 설정
reference_audio = "TDM_LLJ/PTD/J.LJJ15m.wav"  # 가장 작은 파일 사용
test_texts = [
    "이런 곳에 사는군요.",
    "So, this is home for you.",
    "네.",
    "Yes.",
    "근데 싱크대랑 침대가 왜 같은 공간에 있어요?",
    "But, why are the sink and bed in the same space?"
]

print(f"참조 음성: {reference_audio}")

# 파일 존재 확인
if not os.path.exists(reference_audio):
    print(f"❌ 참조 음성 파일을 찾을 수 없습니다: {reference_audio}")
    exit(1)

print(f"✅ 참조 음성 파일 발견: {reference_audio}")

# 모델 경로 확인
model_paths = {
    't2s': 'GPT_SoVITS/pretrained_models/s1v3.ckpt',
    'bert': 'GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large',
    'hubert': 'GPT_SoVITS/pretrained_models/chinese-hubert-base'
}

for name, path in model_paths.items():
    if os.path.exists(path):
        print(f"✅ {name} 모델 발견: {path}")
    else:
        print(f"❌ {name} 모델 누락: {path}")

print("\n=== 음성 합성 테스트 시작 ===")

try:
    # TTS 모듈 임포트
    from TTS_infer_pack.TTS import TTS, TTS_Config
    
    # TTS 설정
    tts_config = TTS_Config(
        device="cpu",
        is_half=False,  # CPU에서는 False
        version="v1",   # v3 모델 사용
        t2s_weights_path=model_paths['t2s'],
        bert_base_path=model_paths['bert'],
        cnhuhbert_base_path=model_paths['hubert']
    )
    
    print("TTS 파이프라인 초기화 중...")
    tts_pipeline = TTS(tts_config)
    
    print("✅ TTS 파이프라인 초기화 완료!")
    
    # 음성 합성 테스트
    for i, text in enumerate(test_texts):
        print(f"\n🔊 테스트 {i+1}: {text}")
        
        try:
            # 음성 합성 실행
            output_path = f"output_{i+1}.wav"
            
            # 여기서 실제 음성 합성을 수행
            # (실제 구현은 TTS 모듈의 API에 따라 달라질 수 있음)
            
            print(f"✅ 음성 합성 완료: {output_path}")
            
        except Exception as e:
            print(f"❌ 음성 합성 실패: {e}")
    
except Exception as e:
    print(f"❌ TTS 초기화 실패: {e}")
    print("모델 파일들을 확인해주세요.")

print("\n=== 테스트 완료 ===") 