#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS WebUI를 통한 TTS 테스트
"""

import sys
import os
import torch
import torchaudio
from pathlib import Path

# GPT-SoVITS 모듈 경로 추가
sys.path.append("GPT-SoVITS")
sys.path.append("GPT-SoVITS/GPT_SoVITS")

def test_direct_inference():
    """직접 추론을 통한 TTS 테스트"""
    
    try:
        # GPT-SoVITS 모듈 임포트
        from GPT_SoVITS.TTS_infer_pack.TTS import TTS, TTS_Config
        from GPT_SoVITS.TTS_infer_pack.text_segmentation_method import get_method
        
        print("✅ GPT-SoVITS 모듈 임포트 성공")
        
        # 설정
        ref_audio_path = "GPT-SoVITS/TDM_LLJ/PTD/J.LJJ15m.wav"
        ref_text = "안녕하세요"
        target_text = "이런 곳에 사는군요."
        
        print(f"참조 음성: {ref_audio_path}")
        print(f"참조 텍스트: {ref_text}")
        print(f"생성할 텍스트: {target_text}")
        
        # TTS 설정
        config = TTS_Config(
            device="cpu",  # CPU 사용
            is_half=False,
            gpt_path="GPT-SoVITS/GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt",
            sovits_path="GPT-SoVITS/GPT_SoVITS/pretrained_models/s2G488k.pth",
            cnhubert_base_path="GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-hubert-base",
            bert_path="GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
            version="v1"
        )
        
        # TTS 객체 생성
        tts = TTS(config)
        
        print("✅ TTS 객체 생성 성공")
        
        # TTS 생성
        result = tts.inference(
            text=target_text,
            text_lang="ko",
            ref_audio_path=ref_audio_path,
            aux_ref_audio_paths=[],
            prompt_text=ref_text,
            prompt_lang="ko",
            top_k=15,
            top_p=1.0,
            temperature=1.0,
            text_split_method="cut5",
            batch_size=1,
            speed_factor=1.0,
            split_bucket=True,
            return_fragment=False,
            fragment_interval=0.3
        )
        
        if result:
            # 결과 저장
            output_file = "webui_test_output.wav"
            torchaudio.save(output_file, torch.tensor(result[1]).unsqueeze(0), result[0])
            print(f"✅ TTS 생성 성공! 파일 저장: {output_file}")
        else:
            print("❌ TTS 생성 실패")
            
    except ImportError as e:
        print(f"❌ 모듈 임포트 실패: {e}")
        print("WebUI가 실행되고 있는지 확인하고, 브라우저에서 직접 테스트해보세요.")
        print("WebUI 주소: http://0.0.0.0:9874")
        
    except Exception as e:
        print(f"❌ TTS 생성 중 오류: {e}")

def print_webui_instructions():
    """WebUI 사용 방법 안내"""
    print("\n🌐 GPT-SoVITS WebUI 사용 방법:")
    print("1. 브라우저에서 http://localhost:9874 또는 http://0.0.0.0:9874 접속")
    print("2. '推理' 탭 선택")
    print("3. 참조 음성 업로드:")
    print("   - 파일: GPT-SoVITS/TDM_LLJ/PTD/J.LJJ15m.wav")
    print("4. 참조 텍스트 입력: '안녕하세요'")
    print("5. 생성할 텍스트 입력:")
    
    test_texts = [
        "이런 곳에 사는군요.",
        "근데 싱크대랑 침대가 왜 같은 공간에 있어요?",
        "So, this is home for you.",
        "But, why are the sink and bed in the same space?",
        "回転寿司食べに行きます？",
        "良いですね。"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"   {i}. {text}")
    
    print("6. 언어 설정 (한국어/영어/일본어)")
    print("7. '生成音频' 버튼 클릭")
    print("\n🎵 다양한 감정의 참조 음성들:")
    
    emotion_files = [
        "GPT-SoVITS/TDM_LLJ/영어/기쁨/PTD/J.LJJ.EN30m.wav (기쁨)",
        "GPT-SoVITS/TDM_LLJ/영어/슬픔/PTD/S.LJJ.EN30m.wav (슬픔)", 
        "GPT-SoVITS/TDM_LLJ/영어/화남/PTD/A.LJJ.EN30m.wav (화남)",
        "GPT-SoVITS/TDM_LLJ/영어/우울/PTD/B.LJJ.EN30m.wav (우울)",
        "GPT-SoVITS/TDM_LLJ/일어/기쁨/PTD/J.LJJ.JP30m.wav (일본어 기쁨)"
    ]
    
    for emotion_file in emotion_files:
        print(f"   - {emotion_file}")

if __name__ == "__main__":
    print("🎤 GPT-SoVITS WebUI TTS 테스트")
    
    # 직접 추론 시도
    test_direct_inference()
    
    # WebUI 사용 방법 안내
    print_webui_instructions() 