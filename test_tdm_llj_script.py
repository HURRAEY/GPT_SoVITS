#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS를 사용하여 TDM_LLJ 음성으로 대화 스크립트 테스트
"""

import os
import sys
import requests
import json
import time
from pathlib import Path

# GPT-SoVITS API 설정 (실제 API 포트)
API_BASE_URL = "http://127.0.0.1:9880"

# 테스트할 대화 스크립트
SCRIPT_LINES = [
    # 한국어 대화
    {"speaker": "현정", "text": "이런 곳에 사는군요.", "lang": "ko"},
    {"speaker": "김환석", "text": "네.", "lang": "ko"},
    {"speaker": "현정", "text": "근데 싱크대랑 침대가 왜 같은 공간에 있어요?", "lang": "ko"},
    {"speaker": "김환석", "text": "네?", "lang": "ko"},
    {"speaker": "현정", "text": "아하! 가사도우미분들 휴게실이군요.", "lang": "ko"},
    {"speaker": "김환석", "text": "휴게실이 아닌데요.", "lang": "ko"},
    {"speaker": "현정", "text": "그럼요?", "lang": "ko"},
    {"speaker": "김환석", "text": "원룸이에요.", "lang": "ko"},
    {"speaker": "현정", "text": "원룸. 그래요. 원룸. 첫 번째 룸은 잘 봤어요. 두 번째 룸 보여줘요.", "lang": "ko"},
    {"speaker": "김환석", "text": "이게 다인데요?", "lang": "ko"},
    
    # 영어 대화
    {"speaker": "현정", "text": "So, this is home for you.", "lang": "en"},
    {"speaker": "김환석", "text": "Yes.", "lang": "en"},
    {"speaker": "현정", "text": "But, why are the sink and bed in the same space?", "lang": "en"},
    {"speaker": "김환석", "text": "What?", "lang": "en"},
    {"speaker": "현정", "text": "Aha! This must be the staff's break room.", "lang": "en"},
    {"speaker": "김환석", "text": "It's not a break room.", "lang": "en"},
    
    # 일본어 대화
    {"speaker": "현정", "text": "回転寿司食べに行きます？", "lang": "ja"},
    {"speaker": "김환석", "text": "良いですね。", "lang": "ja"},
    {"speaker": "현정", "text": "ソン室長、クルーズの準備しなさい", "lang": "ja"},
    {"speaker": "김환석", "text": "回転寿司食べるのになんでクルーズなんですか？", "lang": "ja"},
]

def check_api_status():
    """GPT-SoVITS API 상태 확인"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        # 400 또는 422 응답도 서버가 실행 중임을 의미
        return response.status_code in [400, 422, 500]
    except requests.exceptions.RequestException:
        return False

def find_reference_audio():
    """참조 음성 파일 찾기"""
    base_path = Path("GPT-SoVITS/TDM_LLJ")
    
    # 기쁨 감정의 영어 음성 파일들 확인
    audio_files = []
    
    # 영어 폴더에서 wav/mp3 파일 찾기
    for emotion in ["기쁨", "슬픔", "화남", "우울"]:
        emotion_path = base_path / "영어" / emotion
        if emotion_path.exists():
            for file in emotion_path.rglob("*.wav"):
                audio_files.append(str(file))
            for file in emotion_path.rglob("*.mp3"):
                audio_files.append(str(file))
    
    # 일어 폴더에서도 찾기
    ja_path = base_path / "일어"
    if ja_path.exists():
        for file in ja_path.rglob("*.wav"):
            audio_files.append(str(file))
        for file in ja_path.rglob("*.mp3"):
            audio_files.append(str(file))
    
    # PTD 폴더에서도 찾기
    ptd_path = base_path / "PTD"
    if ptd_path.exists():
        for file in ptd_path.rglob("*.wav"):
            audio_files.append(str(file))
        for file in ptd_path.rglob("*.mp3"):
            audio_files.append(str(file))
    
    return audio_files

def generate_tts(text, ref_audio_path, language="auto", output_path=None):
    """TTS 생성 - GPT-SoVITS API 사용"""
    try:
        # 언어 코드 변환
        lang_map = {
            "ko": "韩文",
            "en": "英文", 
            "ja": "日文",
            "zh": "中文"
        }
        
        api_lang = lang_map.get(language, "中文")
        
        # API 요청 데이터
        data = {
            "refer_wav_path": ref_audio_path,
            "prompt_text": "안녕하세요.",  # 기본 프롬프트 텍스트
            "prompt_language": api_lang,
            "text": text,
            "text_language": api_lang,
            "top_k": 15,
            "top_p": 1.0,
            "temperature": 1.0,
            "speed": 1.0
        }
        
        response = requests.post(f"{API_BASE_URL}/", json=data)
        
        if response.status_code == 200:
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return output_path
            else:
                return response.content
        else:
            print(f"TTS 생성 실패: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"TTS 생성 중 오류: {e}")
        return None

def main():
    print("🎤 GPT-SoVITS TDM_LLJ 스크립트 테스트 시작")
    
    # API 상태 확인
    print("📡 API 상태 확인 중...")
    if not check_api_status():
        print("❌ GPT-SoVITS API가 실행되지 않았습니다.")
        print("   API 서버를 실행해주세요:")
        print("   python api.py -dr 'GPT-SoVITS/TDM_LLJ/PTD/J.LJJ15m.wav' -dt '안녕하세요' -dl '韩文'")
        return
    
    print("✅ API 연결 성공")
    
    # 참조 음성 파일 찾기
    print("🔍 참조 음성 파일 검색 중...")
    audio_files = find_reference_audio()
    
    if not audio_files:
        print("❌ 참조 음성 파일을 찾을 수 없습니다.")
        print("   TDM_LLJ 폴더에 .wav 또는 .mp3 파일이 있는지 확인해주세요.")
        return
    
    print(f"✅ {len(audio_files)}개의 참조 음성 파일 발견")
    for i, file in enumerate(audio_files[:5]):  # 처음 5개만 표시
        print(f"   {i+1}. {file}")
    
    # 첫 번째 참조 음성 사용
    ref_audio = audio_files[0]
    print(f"🎵 참조 음성: {ref_audio}")
    
    # 출력 디렉토리 생성
    output_dir = Path("generated_audio")
    output_dir.mkdir(exist_ok=True)
    
    # 스크립트 각 라인에 대해 TTS 생성
    print("\n🎬 스크립트 TTS 생성 시작...")
    
    for i, line in enumerate(SCRIPT_LINES):
        print(f"\n📝 {i+1:02d}. [{line['speaker']}] {line['text'][:50]}...")
        
        output_file = output_dir / f"{i+1:02d}_{line['speaker']}_{line['lang']}.wav"
        
        result = generate_tts(
            text=line['text'],
            ref_audio_path=ref_audio,
            language=line['lang'],
            output_path=str(output_file)
        )
        
        if result:
            print(f"✅ 생성 완료: {output_file}")
        else:
            print(f"❌ 생성 실패")
        
        # API 부하 방지를 위한 대기
        time.sleep(2)
    
    print(f"\n🎉 테스트 완료! 생성된 파일들은 {output_dir} 폴더에 있습니다.")

if __name__ == "__main__":
    main() 