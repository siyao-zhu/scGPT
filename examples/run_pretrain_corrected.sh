#!/bin/bash

# Load conda environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

# Check PyTorch version and upgrade if needed
echo "Checking PyTorch version..."
PYTORCH_VERSION=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "not installed")

if [[ "$PYTORCH_VERSION" == "not installed" ]] || [[ "${PYTORCH_VERSION%%.*}" -lt 2 ]]; then
    echo "PyTorch version $PYTORCH_VERSION is too old. Upgrading to 2.1+..."
    pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install --upgrade torchmetrics pytorch-lightning
fi

echo "Running pretrain with fast transformer disabled..."
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