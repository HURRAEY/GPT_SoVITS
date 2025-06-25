#!/usr/bin/env python3
import os
import requests
from huggingface_hub import hf_hub_download, snapshot_download
from tqdm import tqdm
import zipfile
import tarfile

def download_file_with_progress(url, local_path):
    """진행률 표시와 함께 파일 다운로드"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f, tqdm(
            desc=os.path.basename(local_path),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        return True
    except Exception as e:
        print(f"❌ {local_path} 다운로드 실패: {e}")
        return False

def download_huggingface_model(repo_id, filename, local_dir):
    """HuggingFace에서 모델 다운로드"""
    try:
        print(f"📥 {repo_id}에서 {filename} 다운로드 중...")
        local_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"✅ 다운로드 완료: {local_path}")
        return True
    except Exception as e:
        print(f"❌ {filename} 다운로드 실패: {e}")
        return False

def main():
    print("=== GPT-SoVITS 누락 모델 다운로드 ===")
    
    base_dir = "GPT_SoVITS/pretrained_models"
    os.makedirs(base_dir, exist_ok=True)
    
    # 다운로드할 모델들
    models_to_download = [
        {
            "name": "s2G488k.pth (v1 VITS 모델)",
            "repo_id": "lj1995/GPT-SoVITS",
            "filename": "s2G488k.pth",
            "local_dir": base_dir
        },
        {
            "name": "s2G2333k.pth (v2 VITS 모델)",
            "repo_id": "lj1995/GPT-SoVITS",
            "filename": "s2G2333k.pth", 
            "local_dir": base_dir
        },
        {
            "name": "s2Gv3.pth (v3 VITS 모델)",
            "repo_id": "lj1995/GPT-SoVITS",
            "filename": "s2Gv3.pth",
            "local_dir": base_dir
        },
        {
            "name": "s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt (v1 T2S 모델)",
            "repo_id": "lj1995/GPT-SoVITS", 
            "filename": "s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt",
            "local_dir": base_dir
        }
    ]
    
    # 추가 시도할 리포지토리들
    alternative_repos = [
        "XXXXRT/GPT-SoVITS-Pretrained",
        "svc-develop-team/so-vits-svc-models",
        "fishaudio/GPT-SoVITS"
    ]
    
    success_count = 0
    
    for model_info in models_to_download:
        print(f"\n📦 {model_info['name']} 다운로드 시도...")
        
        # 기본 리포지토리에서 시도
        if download_huggingface_model(
            model_info['repo_id'], 
            model_info['filename'], 
            model_info['local_dir']
        ):
            success_count += 1
            continue
            
        # 대체 리포지토리들에서 시도
        downloaded = False
        for alt_repo in alternative_repos:
            print(f"  대체 리포지토리 시도: {alt_repo}")
            if download_huggingface_model(alt_repo, model_info['filename'], model_info['local_dir']):
                success_count += 1
                downloaded = True
                break
                
        if not downloaded:
            print(f"  ⚠️ {model_info['filename']} 다운로드 실패 - 모든 소스 시도함")
    
    # G2PW 모델 다운로드 (중국어 발음 처리용)
    print(f"\n📦 G2PW 모델 다운로드 시도...")
    g2pw_dir = "GPT_SoVITS/text/G2PWModel"
    try:
        snapshot_download(
            repo_id="Artrajz/G2PWModel",
            local_dir=g2pw_dir,
            local_dir_use_symlinks=False
        )
        print("✅ G2PW 모델 다운로드 완료")
        success_count += 1
    except Exception as e:
        print(f"❌ G2PW 모델 다운로드 실패: {e}")
    
    print(f"\n=== 다운로드 완료 ===")
    print(f"성공: {success_count}개 모델")
    print(f"실패: {len(models_to_download) + 1 - success_count}개 모델")
    
    # 현재 모델 상태 확인
    print(f"\n=== 현재 모델 상태 ===")
    model_files = [
        "s1v3.ckpt",
        "s2G488k.pth", 
        "s2G2333k.pth",
        "s2Gv3.pth",
        "s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt"
    ]
    
    for model_file in model_files:
        path = os.path.join(base_dir, model_file)
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024*1024)
            print(f"✅ {model_file} ({size:.1f}MB)")
        else:
            print(f"❌ {model_file} (누락)")

if __name__ == "__main__":
    main() 