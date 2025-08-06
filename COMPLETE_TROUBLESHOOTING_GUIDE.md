# Complete Troubleshooting Guide for scGPT

## Issues Encountered

1. **Flash Attention Missing**: `ModuleNotFoundError: No module named 'flash_attn'`
2. **PyTorch Version Incompatibility**: `ModuleNotFoundError: No module named 'torch._custom_ops'`
3. **torchtext Compatibility**: `undefined symbol: _ZN5torch6detail10class_baseC2ERKSsS3_SsRKSt9type_infoS6_`

## Complete Solution

### Step 1: Fix All Compatibility Issues

Run the complete fix script:

```bash
cd ~/scGPT
chmod +x fix_torchtext_compatibility.sh
./fix_torchtext_compatibility.sh
```

### Step 2: Run Pretrain with Complete Fix

```bash
chmod +x examples/run_pretrain_complete_fix.sh
./examples/run_pretrain_complete_fix.sh
```

## Manual Step-by-Step Fix

If the scripts don't work, follow these steps manually:

### 1. Activate Environment
```bash
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env
```

### 2. Upgrade PyTorch
```bash
pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install --upgrade torchmetrics pytorch-lightning
```

### 3. Fix torchtext Compatibility
```bash
pip uninstall torchtext -y
pip install torchtext==0.15.2
```

### 4. Test Imports
```bash
python -c "
import torch
import torchtext
import scgpt
print(f'PyTorch version: {torch.__version__}')
print(f'torchtext version: {torchtext.__version__}')
print('✓ All imports successful!')
"
```

### 5. Run Pretrain
```bash
python ~/scGPT/examples/pretrain.py \
  --data-source    ~/scGPT/data/cellxgene/kidney.scb \
  --vocab-path     ~/scGPT/scgpt/tokenizer/default_census_vocab.json \
  --save-dir       ~/scGPT/examples/pretrain_kidney \
  --batch-size     16 \
  --eval-batch-size 32 \
  --epochs         1 \
  --lr             1e-4 \
  --warmup-ratio-or-step 0.1 \
  --log-interval   100 \
  --max-seq-len    1024 \
  --trunc-by-sample \
  --no-cls \
  --no-cce \
  --fp16 \
  --fast-transformer False
```

## Alternative: Fresh Environment

If you continue to have issues, create a fresh environment:

```bash
# Create new environment
conda create -n scgpt-env-new python=3.9
conda activate scgpt-env-new

# Install PyTorch 2.1+
pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install compatible torchtext
pip install torchtext==0.15.2

# Install scGPT
pip install -e ~/scGPT

# Install other dependencies
pip install scanpy anndata transformers datasets torchmetrics pytorch-lightning
```

## Verification Commands

### Check PyTorch Version
```bash
python -c "import torch; print(torch.__version__)"
```

### Check torchtext Version
```bash
python -c "import torchtext; print(torchtext.__version__)"
```

### Test scGPT Import
```bash
python -c "import scgpt; print('scGPT import successful')"
```

### Test Complete Import Chain
```bash
python -c "
import torch
import torchtext
import scgpt
print('✓ All imports successful!')
"
```

## Expected Versions

After the fix, you should have:
- PyTorch: 2.1.x or higher
- torchtext: 0.15.2
- All other packages compatible with PyTorch 2.1+

## Common Error Messages and Solutions

### Error: `undefined symbol: _ZN5torch6detail10class_baseC2ERKSsS3_SsRKSt9type_infoS6_`
**Solution**: Reinstall torchtext with compatible version
```bash
pip uninstall torchtext -y
pip install torchtext==0.15.2
```

### Error: `ModuleNotFoundError: No module named 'torch._custom_ops'`
**Solution**: Upgrade PyTorch to 2.1+
```bash
pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Error: `ModuleNotFoundError: No module named 'flash_attn'`
**Solution**: Use `--fast-transformer False` or install flash_attn
```bash
# Option 1: Disable fast transformer
--fast-transformer False

# Option 2: Install flash_attn (optional)
pip install flash-attn --no-build-isolation
```

## Files Created

1. `fix_torchtext_compatibility.sh` - Fixes torchtext compatibility
2. `examples/run_pretrain_complete_fix.sh` - Complete fix and pretrain script
3. `COMPLETE_TROUBLESHOOTING_GUIDE.md` - This guide

## Quick Start

For the fastest solution:

```bash
cd ~/scGPT
chmod +x examples/run_pretrain_complete_fix.sh
./examples/run_pretrain_complete_fix.sh
```

This script will:
1. Fix PyTorch version
2. Fix torchtext compatibility
3. Test all imports
4. Run pretrain with correct settings