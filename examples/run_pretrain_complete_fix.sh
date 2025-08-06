#!/bin/bash

echo "Running complete compatibility fix and pretrain..."

# Load conda environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

# Check and fix PyTorch version
echo "Checking PyTorch version..."
PYTORCH_VERSION=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "not installed")

if [[ "$PYTORCH_VERSION" == "not installed" ]] || [[ "${PYTORCH_VERSION%%.*}" -lt 2 ]]; then
    echo "PyTorch version $PYTORCH_VERSION is too old. Upgrading to 2.1+..."
    pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install --upgrade torchmetrics pytorch-lightning
fi

# Fix torchtext compatibility
echo "Fixing torchtext compatibility..."
pip uninstall torchtext -y 2>/dev/null || true
pip install torchtext==0.15.2

# Test imports
echo "Testing imports..."
python -c "
import torch
import torchtext
import scgpt
print(f'PyTorch version: {torch.__version__}')
print(f'torchtext version: {torchtext.__version__}')
print('✓ All imports successful!')
"

if [ $? -eq 0 ]; then
    echo "✓ All compatibility issues fixed!"
    echo "Running pretrain..."
    
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
else
    echo "✗ Import test failed. Please check the error messages above."
    exit 1
fi