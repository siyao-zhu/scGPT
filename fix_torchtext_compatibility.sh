#!/bin/bash

echo "Fixing torchtext compatibility issues..."

# Activate conda environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

echo "Current PyTorch version:"
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

echo "Current torchtext version:"
python -c "import torchtext; print(f'torchtext version: {torchtext.__version__}')" 2>/dev/null || echo "torchtext not installed"

echo "Uninstalling incompatible torchtext..."
pip uninstall torchtext -y

echo "Installing compatible torchtext version..."
# Install torchtext version compatible with PyTorch 2.1+
pip install torchtext==0.15.2

echo "Testing torchtext import..."
python -c "
import torch
import torchtext
print(f'PyTorch version: {torch.__version__}')
print(f'torchtext version: {torchtext.__version__}')
print('✓ torchtext import successful!')
"

echo "Testing scGPT import..."
python -c "
import scgpt
print('✓ scGPT import successful!')
"

echo "torchtext compatibility fix completed!"