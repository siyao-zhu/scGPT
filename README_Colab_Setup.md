# scGPT Pretraining Setup for Google Colab

This guide will help you set up scGPT for pretraining on Google Colab.

## Prerequisites

- Google Colab account
- GPU runtime enabled (recommended)
- Your dataset ready for pretraining

## Step 1: Enable GPU Runtime

1. Go to Google Colab
2. Create a new notebook
3. Go to **Runtime** → **Change runtime type**
4. Set **Hardware accelerator** to **GPU**
5. Click **Save**

## Step 2: Install Dependencies

Run the following cells in your Colab notebook:

### Cell 1: Check GPU
```python
!nvidia-smi
```

### Cell 2: Install System Dependencies
```python
!apt-get update
!apt-get install -y git wget curl
```

### Cell 3: Install PyTorch
```python
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Cell 4: Install Python Dependencies
```python
dependencies = [
    "pandas==1.3.5",
    "scvi-tools==0.16.0",
    "llvmlite==0.38.0",
    "scanpy==1.9.1",
    "torchtext",
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
    !pip install {dep}
```

### Cell 5: Install Flash-Attention (Optional)
```python
try:
    !pip install flash-attn==1.0.1
    print("✅ Flash-attention installed successfully")
except:
    print("⚠️ Flash-attention installation failed. This is common and the model will still work.")
    print("   You can try installing it manually later if needed.")
```

## Step 3: Clone and Install scGPT

### Cell 6: Clone Repository
```python
!git clone https://github.com/bowang-lab/scGPT.git
%cd scGPT
```

### Cell 7: Install scGPT
```python
!pip install -e .
```

### Cell 8: Create Directories
```python
!mkdir -p save checkpoints data
print("✅ Created directories: save, checkpoints, data")
```

## Step 4: Verify Setup

### Cell 9: Test Imports
```python
import sys
sys.path.insert(0, "/content/scGPT")

try:
    import scgpt
    print("✅ scGPT imported successfully")
    print(f"scGPT version: {scgpt.__version__}")
except Exception as e:
    print(f"❌ Error importing scGPT: {e}")

try:
    import torch
    print(f"✅ PyTorch version: {torch.__version__}")
    if torch.cuda.is_available():
        print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
        print(f"   GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("❌ No GPU available")
except Exception as e:
    print(f"❌ Error importing PyTorch: {e}")
```

## Step 5: Prepare Your Dataset

### Supported Dataset Formats

1. **SCB format** (recommended): Single-cell binary format
2. **H5AD format**: AnnData files
3. **CSV format**: Gene expression matrices
4. **10X format**: 10X Genomics data

### Cell 10: Upload Dataset
```python
from google.colab import files

print("📁 Upload your dataset file:")
uploaded = files.upload()

# Move uploaded file to data directory
import shutil
for filename in uploaded.keys():
    shutil.move(filename, f"data/{filename}")
    print(f"✅ Moved {filename} to data/ directory")
```

### Cell 11: Convert to SCB Format (if needed)
```python
import scanpy as sc
import scgpt as scg

# Load your data (modify path as needed)
adata = sc.read_h5ad('data/your_data.h5ad')

# Convert to SCB format
scg.scbank.DataBank.save_adata(adata, 'data/your_data.scb')
print("✅ Converted dataset to SCB format")
```

## Step 6: Start Pretraining

### Cell 12: Basic Pretraining
```python
# Basic pretraining parameters
DATASET = "data/your_dataset.scb"  # CHANGE THIS TO YOUR DATASET PATH
SAVE_DIR = "./save/pretrain_run"
MAX_SEQ_LEN = 600
BATCH_SIZE = 32  # Adjust based on your GPU memory
EPOCHS = 10
LEARNING_RATE = 0.0001

# Run pretraining
!python examples/pretrain.py \
    --data-source {DATASET} \
    --save-dir {SAVE_DIR} \
    --max-seq-len {MAX_SEQ_LEN} \
    --batch-size {BATCH_SIZE} \
    --eval-batch-size {BATCH_SIZE * 2} \
    --epochs {EPOCHS} \
    --lr {LEARNING_RATE} \
    --warmup-ratio-or-step 0.1 \
    --log-interval 100 \
    --trunc-by-sample \
    --no-cls \
    --no-cce \
    --fp16
```

### Cell 13: Advanced Pretraining (Optional)
```python
# Advanced pretraining with more options
DATASET = "data/your_dataset.scb"  # CHANGE THIS TO YOUR DATASET PATH
SAVE_DIR = "./save/advanced_pretrain"
MAX_SEQ_LEN = 800
BATCH_SIZE = 16  # Smaller batch size for larger sequences
EPOCHS = 20
LEARNING_RATE = 0.00005

!python examples/pretrain.py \
    --data-source {DATASET} \
    --save-dir {SAVE_DIR} \
    --max-seq-len {MAX_SEQ_LEN} \
    --batch-size {BATCH_SIZE} \
    --eval-batch-size {BATCH_SIZE * 2} \
    --epochs {EPOCHS} \
    --lr {LEARNING_RATE} \
    --warmup-ratio-or-step 0.1 \
    --log-interval 50 \
    --trunc-by-sample \
    --no-cls \
    --no-cce \
    --fp16 \
    --gradient-accumulation-steps 2 \
    --save-interval 1000
```

## Step 7: Monitor Training

### Cell 14: Start TensorBoard
```python
# Start TensorBoard to monitor training
!tensorboard --logdir=./save --port=6006 --host=0.0.0.0 &

# Get the public URL for TensorBoard
from google.colab import output
output.eval_js('google.colab.kernel.proxyPort(6006)')
```

## Step 8: Download Results

### Cell 15: Download Trained Model
```python
from google.colab import files

# Download the trained model
!zip -r model_checkpoint.zip save/
files.download('model_checkpoint.zip')
```

## Important Parameters

### Model Parameters
- `--max-seq-len`: Maximum sequence length (default: 600)
- `--batch-size`: Training batch size (adjust based on GPU memory)
- `--epochs`: Number of training epochs
- `--lr`: Learning rate

### Training Parameters
- `--fp16`: Use mixed precision training (faster, less memory)
- `--gradient-accumulation-steps`: Accumulate gradients over multiple steps
- `--save-interval`: Save checkpoint every N steps
- `--log-interval`: Log training progress every N steps

### Data Parameters
- `--trunc-by-sample`: Truncate sequences by sample
- `--no-cls`: Don't use CLS token
- `--no-cce`: Don't use cross-entropy loss

## Troubleshooting

### Common Issues:

1. **Out of Memory (OOM)**:
   - Reduce batch size
   - Reduce max sequence length
   - Use gradient accumulation

2. **Flash-attention installation fails**:
   - This is normal, the model will still work
   - You can try installing manually later

3. **Dataset format issues**:
   - Make sure your data is in the correct format
   - Convert to SCB format if needed

4. **GPU not available**:
   - Make sure you're using GPU runtime in Colab
   - Check `!nvidia-smi` output

### Getting Help:

- Check the [scGPT documentation](https://scgpt.readthedocs.io/en/latest/)
- Visit the [GitHub repository](https://github.com/bowang-lab/scGPT)
- Check the [examples directory](examples/) for more usage examples

## Example Dataset Preparation

If you have gene expression data in CSV format:

```python
import pandas as pd
import scanpy as sc
import scgpt as scg

# Load your gene expression data
df = pd.read_csv('your_expression_data.csv', index_col=0)

# Convert to AnnData
adata = sc.AnnData(X=df.T)  # Transpose if genes are columns
adata.var_names = df.index  # Gene names
adata.obs_names = df.columns  # Cell names

# Save as SCB format
scg.scbank.DataBank.save_adata(adata, 'your_data.scb')
```

## Next Steps

After pretraining, you can:

1. **Fine-tune** the model for specific tasks
2. **Evaluate** the model performance
3. **Use** the model for downstream analysis
4. **Share** your trained model

For more examples, see the `examples/` directory in the scGPT repository.