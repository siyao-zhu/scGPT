#!/bin/bash

echo "Upgrading PyTorch from 2.0.1 to 2.1+..."

# Activate conda environment
module load conda/miniforge3/24.11.3-0
source "${HOME}/.bashrc"
conda activate scgpt-env

echo "Current PyTorch version:"
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

echo "Uninstalling current PyTorch packages..."
pip uninstall torch torchvision torchaudio -y

echo "Installing PyTorch 2.1+..."
pip install torch>=2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo "Upgrading related packages..."
pip install --upgrade torchmetrics pytorch-lightning

echo "New PyTorch version:"
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

echo "Testing imports..."
python -c "
import torch
import torchvision
import torchmetrics
import pytorch_lightning
print('✓ All imports successful!')
"

echo "PyTorch upgrade completed!"