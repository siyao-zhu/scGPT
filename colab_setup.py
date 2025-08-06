#!/usr/bin/env python3
"""
Google Colab Setup Script for scGPT Pretraining
This script will help you set up scGPT for pretraining on Google Colab.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and print output"""
    print(f"\n{'='*50}")
    print(f"Running: {description or command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("stdout:", e.stdout)
        if e.stderr:
            print("stderr:", e.stderr)
        return False

def check_gpu():
    """Check if GPU is available"""
    print("\n🔍 Checking GPU availability...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
            return True
        else:
            print("❌ No GPU available")
            return False
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def setup_scgpt():
    """Main setup function"""
    print("🚀 Setting up scGPT for Google Colab...")
    
    # Check if we're in a Colab environment
    try:
        import google.colab
        print("✅ Running in Google Colab")
    except ImportError:
        print("⚠️  Not running in Google Colab - some features may not work")
    
    # Step 1: Install system dependencies
    print("\n📦 Installing system dependencies...")
    run_command("apt-get update", "Updating package list")
    run_command("apt-get install -y git wget curl", "Installing basic tools")
    
    # Step 2: Install Python dependencies
    print("\n🐍 Installing Python dependencies...")
    
    # Install PyTorch with CUDA support
    run_command("pip install torch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 --index-url https://download.pytorch.org/whl/cu116", 
                "Installing PyTorch with CUDA 11.6")
    
    # Install other dependencies
    dependencies = [
        "pandas==1.3.5",
        "scvi-tools==0.16.0",
        "llvmlite==0.38.0",
        "scanpy==1.9.1",
        "torchtext==0.14.0",
        "transformers==4.18.0",
        "numba==0.55.1",
        "scikit-misc==0.1.4",
        "umap-learn==0.5.3",
        "leidenalg==0.8.10",
        "datasets==2.3.0",
        "typing-extensions==4.2.0",
        "scib==1.0.3",
        "wandb",
        "tensorboard",
        "plotly==5.3.1"
    ]
    
    for dep in dependencies:
        run_command(f"pip install {dep}", f"Installing {dep}")
    
    # Step 3: Install flash-attention (may fail, that's okay)
    print("\n⚡ Installing flash-attention...")
    flash_attn_success = run_command("pip install flash-attn==1.0.1", "Installing flash-attention")
    if not flash_attn_success:
        print("⚠️  Flash-attention installation failed. This is common and the model will still work.")
        print("   You can try installing it manually later if needed.")
    
    # Step 4: Clone scGPT repository (if not already present)
    if not os.path.exists("scGPT"):
        print("\n📥 Cloning scGPT repository...")
        run_command("git clone https://github.com/bowang-lab/scGPT.git", "Cloning scGPT repository")
        run_command("cd scGPT", "Changing to scGPT directory")
    else:
        print("✅ scGPT repository already exists")
        run_command("cd scGPT", "Changing to scGPT directory")
    
    # Step 5: Install scGPT in development mode
    print("\n🔧 Installing scGPT in development mode...")
    run_command("pip install -e .", "Installing scGPT package")
    
    # Step 6: Create necessary directories
    print("\n📁 Creating necessary directories...")
    run_command("mkdir -p save checkpoints data", "Creating directories")
    
    # Step 7: Check GPU again
    check_gpu()
    
    print("\n🎉 Setup complete! You can now start pretraining.")
    print("\n📋 Next steps:")
    print("1. Prepare your dataset")
    print("2. Configure your pretraining parameters")
    print("3. Run the pretraining script")
    
    return True

def create_pretrain_script():
    """Create a sample pretraining script"""
    script_content = '''#!/usr/bin/env python3
"""
Sample scGPT Pretraining Script for Google Colab
"""

import os
import sys
from pathlib import Path

# Add scGPT to path
sys.path.insert(0, "/content/scGPT")

# Example pretraining command
# You can modify these parameters based on your needs

# Basic pretraining parameters
DATA_SOURCE = "your_dataset_path"  # Replace with your dataset path
SAVE_DIR = "./save/pretrain_run"
MAX_SEQ_LEN = 600
BATCH_SIZE = 32  # Adjust based on your GPU memory
EPOCHS = 10
LEARNING_RATE = 0.0001

# Construct the pretraining command
pretrain_cmd = f'''
python examples/pretrain.py \\
    --data-source {DATA_SOURCE} \\
    --save-dir {SAVE_DIR} \\
    --max-seq-len {MAX_SEQ_LEN} \\
    --batch-size {BATCH_SIZE} \\
    --eval-batch-size {BATCH_SIZE * 2} \\
    --epochs {EPOCHS} \\
    --lr {LEARNING_RATE} \\
    --warmup-ratio-or-step 0.1 \\
    --log-interval 100 \\
    --trunc-by-sample \\
    --no-cls \\
    --no-cce \\
    --fp16
'''

print("🚀 Starting scGPT pretraining...")
print(f"Command: {pretrain_cmd}")

# Uncomment the line below to actually run the pretraining
# os.system(pretrain_cmd)
'''
    
    with open("sample_pretrain.py", "w") as f:
        f.write(script_content)
    
    print("✅ Created sample_pretrain.py with example configuration")

if __name__ == "__main__":
    print("🔧 scGPT Google Colab Setup")
    print("=" * 50)
    
    success = setup_scgpt()
    
    if success:
        create_pretrain_script()
        print("\n✅ Setup completed successfully!")
        print("\n📖 To start pretraining:")
        print("1. Edit sample_pretrain.py with your dataset path")
        print("2. Run: python sample_pretrain.py")
        print("3. Or run the pretraining command directly from examples/pretrain.py")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")