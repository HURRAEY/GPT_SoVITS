#!/usr/bin/env python3
import os
from huggingface_hub import hf_hub_download, snapshot_download
import shutil

def download_models():
    """GPT-SoVITS 필수 모델들을 다운로드합니다"""
    
    # 모델 저장 경로 설정
    base_path = "GPT_SoVITS/pretrained_models"
    os.makedirs(base_path, exist_ok=True)
    os.makedirs(f"{base_path}/v2Pro", exist_ok=True)
    
    print("GPT-SoVITS 사전 훈련된 모델들을 다운로드 중...")
    
    try:
        # GPT-SoVITS v2Pro 모델들 다운로드
        print("1. s2Gv2Pro.pth 다운로드 중...")
        hf_hub_download(
            repo_id="lj1995/GPT-SoVITS",
            filename="s2Gv2Pro.pth",
            local_dir=f"{base_path}/v2Pro",
            local_dir_use_symlinks=False
        )
        
        print("2. s2Dv2Pro.pth 다운로드 중...")
        hf_hub_download(
            repo_id="lj1995/GPT-SoVITS",
            filename="s2Dv2Pro.pth",
            local_dir=f"{base_path}/v2Pro",
            local_dir_use_symlinks=False
        )
        
        print("3. s1v3.ckpt 다운로드 중...")
        hf_hub_download(
            repo_id="lj1995/GPT-SoVITS",
            filename="s1v3.ckpt",
            local_dir=base_path,
            local_dir_use_symlinks=False
        )
        
        print("4. chinese-roberta-wwm-ext-large 다운로드 중...")
        snapshot_download(
            repo_id="hfl/chinese-roberta-wwm-ext-large",
            local_dir=f"{base_path}/chinese-roberta-wwm-ext-large",
            local_dir_use_symlinks=False
        )
        
        print("5. chinese-hubert-base 다운로드 중...")
        snapshot_download(
            repo_id="TencentGameMate/chinese-hubert-base",
            local_dir=f"{base_path}/chinese-hubert-base",
            local_dir_use_symlinks=False
        )
        
        print("모든 모델 다운로드가 완료되었습니다!")
        
    except Exception as e:
        print(f"모델 다운로드 중 오류 발생: {e}")
        print("일부 모델이 누락되어도 기본 기능은 작동할 수 있습니다.")

if __name__ == "__main__":
    download_models() 