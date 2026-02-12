## Software & Environment Setup

### เครื่องมือที่ใช้

| Category      | Category     | 
|-----------------|----------------|
| Language   | Python 3.10+        |
| Deep Learning    | PyTorch  |
| Pose Extraction       | MediaPipe |
| Data Processing    | NumPy, Pandas |
| Visualization    | Matplotlib |
| Dev Tool   | VS Code  |

## Installation / Setup

### สร้าง Python Virtual Environment

```git bash
    python -m venv venv
    source venv/bin/activate # macOS / Linux
    venv\\Scripts\\activate # Windows
```

<p>อัปเดต pip</p>

```git bash
    pip install --upgrade pip
```

### ติดตั้ง Library ที่จำเป็น

```git bash
    pip install numpy pandas scikit-learn matplotlib tqdm
    pip install torch torchvision torchaudio
    pip install mediapipe opencv-python
```

<p>ตรวจสอบการติดตั้ง</p>

```git bash
   python -c "import torch, mediapipe; print('OK')"
```