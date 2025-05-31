#!/usr/bin/env python3
"""
Melanoma Detection Model Downloader
==================================

This script downloads the pre-trained melanoma detection model from Hugging Face Hub.
Run this script after installing the requirements to set up the AI model.

Usage:
    python download_model.py

Requirements:
    - huggingface_hub (pip install huggingface_hub)
"""

import os
import sys
from pathlib import Path

def main():
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("❌ Error: huggingface_hub is not installed.")
        print("📦 Installing huggingface_hub...")
        os.system(f"{sys.executable} -m pip install huggingface_hub")
        from huggingface_hub import hf_hub_download

    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_file = models_dir / "melanoma_model.h5"
    
    # Check if model already exists
    if model_file.exists():
        file_size = model_file.stat().st_size / (1024 * 1024)  # Convert to MB
        print(f"✅ Model already exists at: {model_file}")
        print(f"📊 File size: {file_size:.1f} MB")
        
        response = input("🔄 Do you want to re-download the model? (y/N): ").lower()
        if response not in ['y', 'yes']:
            print("✨ Using existing model file.")
            return
    
    print("🚀 Downloading melanoma detection model from Hugging Face...")
    print("📁 Repository: likhith-u28/melanoma-detection-model")
    print("📄 File: melanoma_model.h5 (~508MB)")
    print("⏳ This may take a few minutes depending on your internet connection...")
    
    try:
        # Download the model
        downloaded_path = hf_hub_download(
            repo_id="likhith-u28/melanoma-detection-model",
            filename="melanoma_model.h5",
            local_dir="models",
            local_dir_use_symlinks=False  # Download actual file, not symlink
        )
        
        # Verify download
        if Path(downloaded_path).exists():
            file_size = Path(downloaded_path).stat().st_size / (1024 * 1024)
            print(f"✅ Model downloaded successfully!")
            print(f"📁 Location: {downloaded_path}")
            print(f"📊 File size: {file_size:.1f} MB")
            print("🎯 You can now run the Flask application with 'python backend/app.py'")
        else:
            print("❌ Download verification failed.")
            
    except Exception as e:
        print(f"❌ Error downloading model: {str(e)}")
        print("\n🔧 Alternative download methods:")
        print("1. Visit: https://huggingface.co/likhith-u28/melanoma-detection-model")
        print("2. Download melanoma_model.h5 manually")
        print("3. Place it in the 'models/' directory")
        sys.exit(1)

if __name__ == "__main__":
    print("🩺 AI Melanoma Detection System - Model Downloader")
    print("=" * 50)
    main()
