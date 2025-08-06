#!/usr/bin/env python3
"""
Script to fix flash attention import issues in scGPT.
This script will modify the necessary files to handle missing flash_attn gracefully.
"""

import os
import sys
import re

def fix_huggingface_model():
    """Fix the huggingface_model.py file to handle missing flash_attn."""
    file_path = "scgpt/model/huggingface_model.py"
    
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Please run this script from the scGPT root directory.")
        return False
    
    # Read the current file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the fix is already applied
    if "try:\n    from flash_attn.flash_attention import FlashMHA" in content:
        print("✓ huggingface_model.py already has the flash attention fix applied.")
        return True
    
    # Apply the fix
    old_import = "from flash_attn.flash_attention import FlashMHA\nfrom .flash_layers import FlashscGPTLayer, FlashscGPTGenerator"
    new_import = """try:
    from flash_attn.flash_attention import FlashMHA
    from .flash_layers import FlashscGPTLayer, FlashscGPTGenerator
    FLASH_ATTN_AVAILABLE = True
except ImportError:
    import warnings
    warnings.warn("flash_attn is not installed")
    FLASH_ATTN_AVAILABLE = False
    FlashMHA = None
    FlashscGPTLayer = None
    FlashscGPTGenerator = None"""
    
    content = content.replace(old_import, new_import)
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Fixed huggingface_model.py")
    return True

def fix_flash_layers():
    """Fix the flash_layers.py file to handle missing flash_attn."""
    file_path = "scgpt/model/flash_layers.py"
    
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Please run this script from the scGPT root directory.")
        return False
    
    # Read the current file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the fix is already applied
    if "try:\n    from flash_attn.flash_attn_interface import flash_attn_unpadded_qkvpacked_func" in content:
        print("✓ flash_layers.py already has the flash attention fix applied.")
        return True
    
    # Apply the fix
    old_import = """from flash_attn.flash_attn_interface import flash_attn_unpadded_qkvpacked_func
from flash_attn.bert_padding import unpad_input, pad_input
from flash_attn.flash_attention import FlashAttention
from flash_attn.modules.mha import FlashCrossAttention"""
    
    new_import = """try:
    from flash_attn.flash_attn_interface import flash_attn_unpadded_qkvpacked_func
    from flash_attn.bert_padding import unpad_input, pad_input
    from flash_attn.flash_attention import FlashAttention
    from flash_attn.modules.mha import FlashCrossAttention
    FLASH_ATTN_AVAILABLE = True
except ImportError:
    import warnings
    warnings.warn("flash_attn is not installed")
    FLASH_ATTN_AVAILABLE = False
    flash_attn_unpadded_qkvpacked_func = None
    unpad_input = None
    pad_input = None
    FlashAttention = None
    FlashCrossAttention = None"""
    
    content = content.replace(old_import, new_import)
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Fixed flash_layers.py")
    return True

def create_fixed_pretrain_script():
    """Create a fixed pretrain script that disables fast transformer."""
    script_content = """#!/bin/bash

# Load conda environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

# Run pretrain with fast transformer disabled to avoid flash_attn dependency
python ~/scGPT/examples/pretrain.py \\
  --data-source    ~/scGPT/data/cellxgene/kidney.scb \\
  --vocab-path     ~/scGPT/scgpt/tokenizer/default_census_vocab.json \\
  --save-dir       ~/scGPT/examples/pretrain_kidney \\
  --batch-size     16 \\
  --eval-batch-size 32 \\
  --epochs         1 \\
  --lr             1e-4 \\
  --warmup-ratio-or-step 0.1 \\
  --log-interval   100 \\
  --max-seq-len    1024 \\
  --trunc-by-sample \\
  --no-cls \\
  --no-cce \\
  --fp16 \\
  --fast-transformer False
"""
    
    with open("examples/run_pretrain_fixed.sh", 'w') as f:
        f.write(script_content)
    
    # Make it executable
    os.chmod("examples/run_pretrain_fixed.sh", 0o755)
    print("✓ Created examples/run_pretrain_fixed.sh")

def main():
    print("Fixing flash attention issues in scGPT...")
    print("=" * 50)
    
    success = True
    success &= fix_huggingface_model()
    success &= fix_flash_layers()
    create_fixed_pretrain_script()
    
    print("=" * 50)
    if success:
        print("✓ All fixes applied successfully!")
        print("\nTo run pretrain without flash attention, use:")
        print("  ./examples/run_pretrain_fixed.sh")
        print("\nOr run with fast transformer disabled:")
        print("  python ~/scGPT/examples/pretrain.py --fast-transformer False [other args]")
    else:
        print("✗ Some fixes failed. Please check the error messages above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())