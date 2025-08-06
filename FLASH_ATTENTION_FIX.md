# Flash Attention Fix for scGPT

## Problem Description

When trying to run the scGPT pretrain script, you encountered the following error:

```
ModuleNotFoundError: No module named 'flash_attn'
```

This error occurs because the scGPT codebase uses Flash Attention for improved performance, but the `flash_attn` package is not installed in your conda environment.

## Root Cause

The issue is in the following files:
1. `scgpt/model/huggingface_model.py` - imports `flash_attn` without proper error handling
2. `scgpt/model/flash_layers.py` - imports `flash_attn` without proper error handling

While `scgpt/model/model.py` already had proper try-except handling, the other files did not.

## Solutions Implemented

### Solution 1: Code Fixes (Recommended)

I've modified the following files to handle missing `flash_attn` gracefully:

1. **`scgpt/model/huggingface_model.py`**:
   - Added try-except block around flash_attn imports
   - Added fallback to standard `nn.MultiheadAttention` when flash_attn is not available
   - Updated attention calls to work with both flash and standard attention

2. **`scgpt/model/flash_layers.py`**:
   - Added try-except block around flash_attn imports
   - Added fallback mechanisms for when flash_attn is not available

### Solution 2: Disable Fast Transformer (Quick Fix)

The easiest immediate solution is to disable fast transformer, which avoids using flash attention:

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

I've created a modified script `examples/run_pretrain_fixed.sh` with this configuration.

### Solution 3: Install Flash Attention (Performance Option)

If you want to use flash attention for better performance, you can install it:

```bash
# Activate your conda environment
conda activate scgpt-env

# Install flash attention (this may take a while and requires CUDA)
pip install flash-attn --no-build-isolation
```

**Note**: Flash attention installation can be complex and may require specific CUDA versions and build tools.

## Testing the Fix

I've created test scripts to verify the fix works:

1. `test_flash_attn_fix.py` - Full test (requires PyTorch)
2. `test_import_only.py` - Import structure test

## Usage

### Option 1: Use the Fixed Script
```bash
chmod +x examples/run_pretrain_fixed.sh
./examples/run_pretrain_fixed.sh
```

### Option 2: Run with Fast Transformer Disabled
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

## Performance Impact

- **With flash attention**: Faster training, lower memory usage
- **Without flash attention**: Slower training, higher memory usage, but still functional

The model will work correctly in both cases, but flash attention provides performance benefits.

## Files Modified

1. `scgpt/model/huggingface_model.py` - Added flash attention fallback
2. `scgpt/model/flash_layers.py` - Added flash attention fallback
3. `examples/run_pretrain_fixed.sh` - Created fixed pretrain script
4. `test_flash_attn_fix.py` - Created test script
5. `test_import_only.py` - Created import test script

## Next Steps

1. Try running the fixed script: `./examples/run_pretrain_fixed.sh`
2. If you encounter other issues, they will likely be related to missing data files or other dependencies
3. Consider installing flash attention if you need better performance