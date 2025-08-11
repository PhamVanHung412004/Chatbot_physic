# Hướng dẫn chạy mô hình Qwen3-0.6B với file `test_model.py` (dùng Conda)

## 1. Mô tả
File `test_model.py` cho phép bạn tương tác với mô hình ngôn ngữ Qwen3-0.6B để giải đáp các câu hỏi vật lý trắc nghiệm theo chuẩn chuyên gia, với hướng dẫn chi tiết từng bước giải.

## 2. Yêu cầu hệ thống
- Python >= 3.8
- Kết nối Internet để tải mô hình từ HuggingFace lần đầu
- RAM tối thiểu 4GB (khuyến nghị 8GB+)

## 3. Cài đặt môi trường với Conda
### a. Tạo môi trường conda mới
```bash
conda create -n testmodel python=3.11 -y
conda activate testmodel
```

### b. Cài torch bản CPU-only bằng conda
```bash
conda install pytorch==2.7.1 cpuonly -c pytorch -c conda-forge -y
```

### c. Cài đặt các thư viện Database cho môi trường ubuntu
```bash
sudo apt update
sudo apt install default-libmysqlclient-dev build-essential pkg-config
```

### d. Cài các thư viện còn lại bằng pip
- Đảm bảo đã xóa dòng `torch==...` khỏi `requirements.txt` (nếu còn).
- Sau đó cài các thư viện còn lại:
```bash
pip install -r requirements.txt
export GOOGLE_API_KEY=YOUR_API_KEY
```

**Lưu ý:**
- KHÔNG dùng pip để cài torch khi sử dụng conda, hãy luôn dùng lệnh conda như trên để tránh lỗi CUDA/NCCL.
- `transformers==4.53.3` và `accelerate==1.9.0` là các bản mới nhất đã kiểm tra tương thích.

## 4. Chạy chương trình
```bash
python test_model.py
```
- Lần đầu chạy sẽ mất thời gian tải mô hình (~1.5GB).
- Sau khi tải xong, chương trình sẽ hỏi bạn nhập câu hỏi vật lý.
- Nhập câu hỏi và nhấn Enter để nhận lời giải chi tiết.

## 5. Một số lỗi thường gặp
- **Lỗi ImportError liên quan CUDA/NCCL:**
  - Đảm bảo đã cài torch bản CPU-only bằng conda như hướng dẫn trên.
- **Lỗi thiếu accelerate:**
  - Cài đặt bằng: `pip install accelerate`
- **Lỗi thiếu transformers:**
  - Cài đặt bằng: `pip install transformers`

## 6. Tùy chỉnh prompt hệ thống
Bạn có thể chỉnh sửa biến `system` trong file `test_model.py` để thay đổi hướng dẫn cho mô hình.

## 7. Tham khảo thêm
- [Qwen3-0.6B trên HuggingFace](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Tài liệu PyTorch](https://pytorch.org/)
- [Tài liệu Transformers](https://huggingface.co/docs/transformers)

---
Nếu gặp vấn đề khi cài đặt hoặc chạy, hãy kiểm tra lại các bước trên hoặc liên hệ hỗ trợ. 