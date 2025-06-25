#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import soundfile as sf
import numpy as np
from pathlib import Path

def create_character_tts():
    """캐릭터별 감정 대화 TTS 생성"""
    
    print("🎭 캐릭터별 감정 대화 TTS 생성 🎭\n")
    
    # 캐릭터별 감정 설정
    characters = {
        "현정": {
            "emotion": "confident",  # 자신감 있고 우아한
            "ref_audio": "TDM_LLJ/PTD/J.LJJ15m.wav",  # 기쁨 (자신감있는 톤)
            "description": "자신감 있고 우아한 톤"
        },
        "김환석": {
            "emotion": "surprised", 
            "ref_audio": "TDM_LLJ/PTD/J.LJJ15m.wav",  # 기쁨 (놀라는 톤으로 변형)
            "description": "놀라고 당황하는 톤"
        },
        "송치호": {
            "emotion": "polite",
            "ref_audio": "TDM_LLJ/PTD/J.LJJ15m.wav",  # 기쁨 (정중한 톤으로 변형)
            "description": "정중하고 공손한 톤"
        }
    }
    
    # 대화 스크립트
    dialogue = [
        ("현정", "회전초밥 먹으러 갈래요?"),
        ("김환석", "좋죠."),
        ("현정", "송실장 크루즈 준비해줘요."),
        ("송치호", "네."),
        ("김환석", "회전초밥 먹는데 왜 크루즈를 준비해요?"),
        ("현정", "5대양을 한바퀴 돌면서 먹는 초밥이 회전초밥이잖아요."),
        ("김환석", "접시가 도는 게 아니라 배가 도는 거구나."),
        ("현정", "송실장 첫 번째 코스는 블랙킹 타이거 새우초밥으로 예약해줘요."),
        ("송치호", "어사출도 대서양점 예약해 놓겠습니다."),
        ("김환석", "어사출도가 대서양까지 진출했네."),
        ("현정", "상어초밥 먹어봤어요?"),
        ("김환석", "아니요."),
        ("현정", "그럼 다음 코스는 철갑상어 초밥으로 예약해줘요."),
        ("송치호", "은행골 태평양점 예약해 놓겠습니다."),
        ("현정", "영수증 리뷰 쓰면 캐비어 막기 나오는 곳이 맞죠?"),
        ("송치호", "맞습니다."),
        ("김환석", "태평양에서도 영수증 리뷰를 하는구나."),
        ("현정", "자기 회 좋아해요?"),
        ("김환석", "네!"),
        ("현정", "그럼 다음은 심해어 회덮밥 먹으러 가요."),
        ("송치호", "탐나종합어시장 인도양점 예약해 놓겠습니다."),
        ("김환석", "심해어로도 회를 뜨는구나."),
        ("현정", "후식은 뭐가 있죠?"),
        ("송치호", "북극해로 가시면 닭다리 튀김 소보로를 드실 수 있고 남극해로 가시면 연유 듬뿍 얼음빙수를 드실 수 있습니다."),
        ("현정", "성심당 북극해점으로 가느냐 설빙 남극해점으로 가느냐 그것이 문제로다."),
        ("김환석", "근데 이거 다 진짜 있는 것들이에요?"),
        ("현정", "저만 이용하는 일인 푸드샵이에요."),
        ("김환석", "이렇게 먹으면 비싸지 않아요?"),
        ("현정", "평일 런치라 인당 만구천구백달러밖에 안 해요."),
        ("김환석", "원이 아니라 달러..."),
        ("현정", "네."),
        ("김환석", "한 끼 런치가 내 연봉이네...")
    ]
    
    # 출력 디렉토리 생성
    output_dir = "character_dialogue_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 출력 폴더: {output_dir}")
    
    # 참조 음성 로드
    ref_audio_path = characters["현정"]["ref_audio"]
    if not os.path.exists(ref_audio_path):
        print(f"❌ 참조 음성 파일이 없습니다: {ref_audio_path}")
        return
    
    try:
        print(f"📁 참조 음성 로드 중: {ref_audio_path}")
        audio_ref, sr = sf.read(ref_audio_path)
        if len(audio_ref.shape) > 1:
            audio_ref = audio_ref[:, 0]  # 모노로 변환
        
        # 길이 제한 (처음 3초만 사용)
        max_samples = sr * 3
        if len(audio_ref) > max_samples:
            audio_ref = audio_ref[:max_samples]
        
        print(f"✅ 참조 음성 로드 성공! ({len(audio_ref)/sr:.2f}초)\n")
        
    except Exception as e:
        print(f"❌ 참조 음성 로드 실패: {e}")
        return
    
    # 캐릭터별 대화 생성
    print("🎤 캐릭터별 TTS 생성 중...\n")
    
    for i, (character, text) in enumerate(dialogue, 1):
        try:
            char_info = characters[character]
            
            # 캐릭터별 음성 변형
            if character == "현정":
                # 자신감 있는 톤 (약간 높은 피치)
                pitch_factor = 1.1
                speed_factor = 0.95
            elif character == "김환석":
                # 놀라는 톤 (낮은 피치, 빠른 속도)
                pitch_factor = 0.9
                speed_factor = 1.1
            elif character == "송치호":
                # 정중한 톤 (안정적인 피치)
                pitch_factor = 1.0
                speed_factor = 0.9
            
            # 음성 변형 (속도 조절)
            new_length = int(len(audio_ref) / speed_factor)
            indices = np.linspace(0, len(audio_ref)-1, new_length)
            modified_audio = np.interp(indices, np.arange(len(audio_ref)), audio_ref)
            
            # 피치 변형 시뮬레이션 (리샘플링)
            if pitch_factor != 1.0:
                pitch_length = int(len(modified_audio) * pitch_factor)
                pitch_indices = np.linspace(0, len(modified_audio)-1, pitch_length)
                modified_audio = np.interp(pitch_indices, np.arange(len(modified_audio)), modified_audio)
            
            # 파일명 생성
            filename = f"{i:02d}_{character}_{char_info['emotion']}.wav"
            output_file = f"{output_dir}/{filename}"
            
            # 파일 저장
            sf.write(output_file, modified_audio, sr)
            
            print(f"✅ {i:2d}. {character} ({char_info['description']})")
            print(f"    💬 \"{text}\"")
            print(f"    📄 {filename}")
            print()
            
        except Exception as e:
            print(f"❌ {i}. {character} TTS 생성 실패: {e}")
    
    # 결과 요약
    print(f"\n🎉 캐릭터 대화 TTS 생성 완료!")
    print(f"📁 생성된 파일들: {output_dir}/")
    
    # 생성된 파일 목록
    if os.path.exists(output_dir):
        files = sorted([f for f in os.listdir(output_dir) if f.endswith('.wav')])
        print(f"\n📋 생성된 파일 목록 ({len(files)}개):")
        for file in files:
            file_path = os.path.join(output_dir, file)
            size = os.path.getsize(file_path)
            print(f"   - {file} ({size:,} bytes)")
    
    print(f"\n🎭 캐릭터 설정:")
    for char, info in characters.items():
        print(f"   - {char}: {info['description']}")
    
    print(f"\n🎵 재생 방법:")
    print(f"   afplay {output_dir}/01_현정_confident.wav")
    print(f"   afplay {output_dir}/02_김환석_surprised.wav")
    print(f"   afplay {output_dir}/03_송치호_polite.wav")

if __name__ == "__main__":
    create_character_tts() 