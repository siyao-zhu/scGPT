# PyTorch Compatibility Fix for scGPT

## Problem Description

You're encountering a PyTorch version compatibility issue:

```
ModuleNotFoundError: No module named 'torch._custom_ops'
```

This error occurs because:
1. Your PyTorch version (1.11.0) is too old
2. The newer torchvision/torchmetrics packages require PyTorch 2.1+
3. The `torch._custom_ops` module was introduced in PyTorch 2.0+

## Root Cause

The scGPT environment has incompatible package versions:
- PyTorch: 1.11.0 (too old)
- torchvision: newer version (requires PyTorch 2.1+)
- torchmetrics: newer version (requires PyTorch 2.1+)

## Solutions

### Solution 1: Upgrade PyTorch (Recommended)

Run the PyTorch upgrade script:

```bash
# Make the script executable
chmod +x fix_pytorch.sh

# Run the upgrade
./fix_pytorch.sh
```

Or manually upgrade:

```bash
# Activate your conda environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

# Upgrade PyTorch to 2.1+
pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Upgrade related packages
pip install --upgrade torchmetrics pytorch-lightning
```

### Solution 2: Use the Corrected Script

I've created a corrected pretrain script that handles the PyTorch version automatically:

```bash
# Make it executable
chmod +x examples/run_pretrain_corrected.sh

# Run it
./examples/run_pretrain_corrected.sh
```

### Solution 3: Manual Command

After upgrading PyTorch, run pretrain with:

```bash
# Activate environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

# Run pretrain
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

## Verification

After upgrading, verify the fix:

```bash
python -c "
import torch
import torchvision
import torchmetrics
import pytorch_lightning
print(f'PyTorch version: {torch.__version__}')
print('✓ All imports successful!')
"
```

## Expected Output

You should see:
```
PyTorch version: 2.1.x
✓ All imports successful!
```

## Alternative: Create New Environment

If the upgrade causes issues, you can create a fresh environment:

```bash
# Create new environment
conda create -n scgpt-env-new python=3.9
conda activate scgpt-env-new

# Install PyTorch 2.1+
pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install scGPT dependencies
pip install -e ~/scGPT

# Install other required packages
pip install scanpy anndata transformers datasets
```

## Files Created

1. `fix_pytorch.sh` - Script to upgrade PyTorch
2. `examples/run_pretrain_corrected.sh` - Corrected pretrain script
3. `PYTORCH_COMPATIBILITY_FIX.md` - This documentation

## Next Steps

1. Run `./fix_pytorch.sh` to upgrade PyTorch
2. Test with `./examples/run_pretrain_corrected.sh`
3. If successful, you can use the original pretrain command with `--fast-transformer False`

## Troubleshooting

If you encounter issues:

1. **CUDA version mismatch**: Use CPU-only PyTorch:
   ```bash
   pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

2. **Memory issues**: Reduce batch size:
   ```bash
   --batch-size 8 --eval-batch-size 16
   ```

3. **Package conflicts**: Create fresh environment as shown above