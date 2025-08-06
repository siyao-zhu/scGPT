#!/bin/bash

# Load conda environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

# Run pretrain with fast transformer disabled to avoid flash_attn dependency
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