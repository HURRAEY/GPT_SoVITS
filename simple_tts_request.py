#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import os

def test_tts_api():
    """TTS API 테스트 및 요청"""
    
    print("🎭 TTS API 요청 테스트 🎭\n")
    
    # 가능한 TTS API 엔드포인트들
    possible_endpoints = [
        "http://localhost:9880/tts",
        "http://localhost:9880/",
        "http://localhost:9871/tts", 
        "http://localhost:9872/tts",
        "http://localhost:9873/tts",
        "http://localhost:9881/tts",
        "http://127.0.0.1:9880/tts",
        "http://127.0.0.1:9871/tts"
    ]
    
    # 테스트 데이터
    test_data = {
        "text": "안녕하세요, 회전초밥 먹으러 갈래요?",
        "text_lang": "ko",
        "ref_audio_path": "TDM_LLJ/PTD/J.LJJ15m.wav",
        "aux_ref_audio_paths": [],
        "prompt_text": "안녕하세요",
        "prompt_lang": "ko",
        "top_k": 15,
        "top_p": 1.0,
        "temperature": 1.0,
        "text_split_method": "cut5",
        "batch_size": 1,
        "batch_threshold": 0.75,
        "split_bucket": True,
        "speed_factor": 1.0,
        "fragment_interval": 0.3,
        "seed": -1,
        "media_type": "wav",
        "streaming_mode": False
    }
    
    working_endpoint = None
    
    # 각 엔드포인트 테스트
    for endpoint in possible_endpoints:
        try:
            print(f"🔍 테스트 중: {endpoint}")
            
            # 연결 테스트
            response = requests.get(endpoint.replace('/tts', ''), timeout=3)
            print(f"   📡 연결 성공 (상태: {response.status_code})")
            
            # TTS 요청 테스트
            tts_response = requests.post(endpoint, json=test_data, timeout=15)
            
            if tts_response.status_code == 200:
                print(f"   ✅ TTS 성공! 길이: {len(tts_response.content)} bytes")
                
                # 파일 저장
                output_file = "api_test_tts.wav"
                with open(output_file, 'wb') as f:
                    f.write(tts_response.content)
                
                print(f"   💾 저장: {output_file}")
                working_endpoint = endpoint
                break
            else:
                print(f"   ❌ TTS 실패 (상태: {tts_response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ 연결 실패")
        except requests.exceptions.Timeout:
            print(f"   ⏰ 타임아웃")
        except Exception as e:
            print(f"   ❌ 오류: {e}")
        
        print()
    
    if working_endpoint:
        print(f"🎉 작동하는 엔드포인트 발견: {working_endpoint}")
        return working_endpoint
    else:
        print("❌ 작동하는 TTS API를 찾을 수 없습니다.")
        print("💡 브라우저에서 TTS Inference WebUI 창을 확인하고")
        print("   'Start TTS Inference Server' 버튼이 있다면 클릭해주세요.")
        return None

def generate_dialogue_tts(endpoint):
    """대화 스크립트 전체 TTS 생성"""
    
    if not endpoint:
        return
    
    print(f"\n🎭 대화 TTS 자동 생성 시작! 🎭")
    print(f"🔗 사용 엔드포인트: {endpoint}\n")
    
    # 회전초밥 대화 스크립트 (처음 10개)
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
        ("김환석", "어사출도가 대서양까지 진출했네.", "amazed")
    ]
    
    # 출력 디렉토리
    output_dir = "api_generated_tts_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 출력 폴더: {output_dir}")
    print(f"🎯 {len(dialogue)}개 대화 생성\n")
    
    success_count = 0
    
    for i, (character, text, emotion) in enumerate(dialogue, 1):
        try:
            print(f"🎤 {i:2d}. {character} ({emotion})")
            print(f"    💬 \"{text}\"")
            
            # TTS 요청 데이터
            tts_data = {
                "text": text,
                "text_lang": "ko",
                "ref_audio_path": "TDM_LLJ/PTD/J.LJJ15m.wav",
                "aux_ref_audio_paths": [],
                "prompt_text": "안녕하세요",
                "prompt_lang": "ko",
                "top_k": 15,
                "top_p": 1.0,
                "temperature": 1.0,
                "text_split_method": "cut5",
                "batch_size": 1,
                "speed_factor": 1.0,
                "seed": -1,
                "media_type": "wav"
            }
            
            # TTS 생성
            response = requests.post(endpoint, json=tts_data, timeout=20)
            
            if response.status_code == 200:
                filename = f"{output_dir}/{i:02d}_{character}_{emotion}.wav"
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                size = os.path.getsize(filename)
                print(f"    ✅ 저장: {filename} ({size:,} bytes)")
                success_count += 1
            else:
                print(f"    ❌ TTS 실패 (상태: {response.status_code})")
                
        except Exception as e:
            print(f"    ❌ 오류: {e}")
        
        print()
        time.sleep(1)  # API 부하 방지
    
    print(f"🎉 대화 TTS 생성 완료!")
    print(f"✅ 성공: {success_count}/{len(dialogue)}개")
    
    if success_count > 0:
        first_file = f"{output_dir}/01_현정_confident.wav"
        if os.path.exists(first_file):
            print(f"\n🎵 첫 번째 파일 재생:")
            print(f"   afplay {first_file}")

if __name__ == "__main__":
    # 1. API 테스트
    working_endpoint = test_tts_api()
    
    # 2. 대화 TTS 생성
    if working_endpoint:
        generate_dialogue_tts(working_endpoint)
