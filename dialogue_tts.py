#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import soundfile as sf
import numpy as np

def create_character_dialogue():
    """캐릭터별 감정 대화 TTS 생성"""
    
    print("🎭 캐릭터별 감정 대화 TTS 생성 🎭\n")
    
    # 대화 스크립트 (캐릭터, 텍스트, 감정)
    dialogue = [
        ("현정", "회전초밥 먹으러 갈래요?", "confident"),
        ("김환석", "좋죠.", "agreeable"),
        ("현정", "송실장 크루즈 준비해줘요.", "commanding"),
        ("송치호", "네.", "polite"),
        ("김환석", "회전초밥 먹는데 왜 크루즈를 준비해요?", "confused"),
        ("현정", "5대양을 한바퀴 돌면서 먹는 초밥이 회전초밥이잖아요.", "explaining"),
        ("김환석", "접시가 도는 게 아니라 배가 도는 거구나.", "understanding"),
        ("현정", "송실장 첫 번째 코스는 블랙킹 타이거 새우초밥으로 예약해줘요.", "ordering"),
        ("송치호", "어사출도 대서양점 예약해 놓겠습니다.", "professional"),
        ("김환석", "어사출도가 대서양까지 진출했네.", "amazed"),
        ("현정", "상어초밥 먹어봤어요?", "curious"),
        ("김환석", "아니요.", "simple"),
        ("현정", "그럼 다음 코스는 철갑상어 초밥으로 예약해줘요.", "deciding"),
        ("송치호", "은행골 태평양점 예약해 놓겠습니다.", "confirming"),
        ("현정", "영수증 리뷰 쓰면 캐비어 막기 나오는 곳이 맞죠?", "checking"),
        ("송치호", "맞습니다.", "confirming"),
        ("김환석", "태평양에서도 영수증 리뷰를 하는구나.", "surprised"),
        ("현정", "자기 회 좋아해요?", "asking"),
        ("김환석", "네!", "excited"),
        ("현정", "그럼 다음은 심해어 회덮밥 먹으러 가요.", "suggesting"),
        ("송치호", "탐나종합어시장 인도양점 예약해 놓겠습니다.", "booking"),
        ("김환석", "심해어로도 회를 뜨는구나.", "learning"),
        ("현정", "후식은 뭐가 있죠?", "inquiring"),
        ("송치호", "북극해로 가시면 닭다리 튀김 소보로를 드실 수 있고 남극해로 가시면 연유 듬뿍 얼음빙수를 드실 수 있습니다.", "explaining"),
        ("현정", "성심당 북극해점으로 가느냐 설빙 남극해점으로 가느냐 그것이 문제로다.", "pondering"),
        ("김환석", "근데 이거 다 진짜 있는 것들이에요?", "doubting"),
        ("현정", "저만 이용하는 일인 푸드샵이에요.", "proud"),
        ("김환석", "이렇게 먹으면 비싸지 않아요?", "worried"),
        ("현정", "평일 런치라 인당 만구천구백달러밖에 안 해요.", "casual"),
        ("김환석", "원이 아니라 달러...", "shocked"),
        ("현정", "네.", "confirming"),
        ("김환석", "한 끼 런치가 내 연봉이네...", "devastated")
    ]
    
    # 출력 디렉토리 생성
    output_dir = "character_dialogue_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 출력 폴더: {output_dir}")
    
    # 참조 음성 로드
    ref_audio_path = "TDM_LLJ/PTD/J.LJJ15m.wav"
    if not os.path.exists(ref_audio_path):
        print(f"❌ 참조 음성 파일이 없습니다: {ref_audio_path}")
        return
    
    try:
        print(f"📁 참조 음성 로드 중: {ref_audio_path}")
        audio_ref, sr = sf.read(ref_audio_path)
        if len(audio_ref.shape) > 1:
            audio_ref = audio_ref[:, 0]  # 모노로 변환
        
        # 길이 제한 (처음 2초만 사용)
        max_samples = sr * 2
        if len(audio_ref) > max_samples:
            audio_ref = audio_ref[:max_samples]
        
        print(f"✅ 참조 음성 로드 성공! ({len(audio_ref)/sr:.2f}초)\n")
        
    except Exception as e:
        print(f"❌ 참조 음성 로드 실패: {e}")
        return
    
    # 캐릭터별 대화 생성
    print("🎤 캐릭터별 TTS 생성 중...\n")
    
    for i, (character, text, emotion) in enumerate(dialogue, 1):
        try:
            # 캐릭터별 음성 변형
            if character == "현정":
                # 자신감 있는 톤
                pitch_factor = 1.05
                speed_factor = 0.95
                volume_factor = 1.1
            elif character == "김환석":
                # 놀라는/당황하는 톤
                pitch_factor = 0.95
                speed_factor = 1.05
                volume_factor = 1.0
            elif character == "송치호":
                # 정중한 톤
                pitch_factor = 1.0
                speed_factor = 0.9
                volume_factor = 0.9
            
            # 감정별 추가 변형
            if emotion in ["excited", "amazed", "shocked"]:
                speed_factor *= 1.1
                volume_factor *= 1.2
            elif emotion in ["polite", "professional", "confirming"]:
                speed_factor *= 0.9
            elif emotion in ["devastated", "worried"]:
                pitch_factor *= 0.9
                speed_factor *= 0.8
            
            # 음성 변형 적용
            new_length = int(len(audio_ref) / speed_factor)
            indices = np.linspace(0, len(audio_ref)-1, new_length)
            modified_audio = np.interp(indices, np.arange(len(audio_ref)), audio_ref)
            
            # 볼륨 조절
            modified_audio = modified_audio * volume_factor
            
            # 클리핑 방지
            modified_audio = np.clip(modified_audio, -1.0, 1.0)
            
            # 파일명 생성
            filename = f"{i:02d}_{character}_{emotion}.wav"
            output_file = f"{output_dir}/{filename}"
            
            # 파일 저장
            sf.write(output_file, modified_audio, sr)
            
            print(f"✅ {i:2d}. {character} ({emotion})")
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
        for file in files[:10]:  # 처음 10개만 표시
            file_path = os.path.join(output_dir, file)
            size = os.path.getsize(file_path)
            print(f"   - {file} ({size:,} bytes)")
        if len(files) > 10:
            print(f"   ... 외 {len(files)-10}개 파일")
    
    print(f"\n🎵 재생 예시:")
    print(f"   afplay {output_dir}/01_현정_confident.wav")
    print(f"   afplay {output_dir}/02_김환석_agreeable.wav")
    print(f"   afplay {output_dir}/03_현정_commanding.wav")

if __name__ == "__main__":
    create_character_dialogue()
