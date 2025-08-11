"""
Module RAG (Retrieval-Augmented Generation) cho hệ thống vật lý.

Module này chứa các thành phần chính của hệ thống RAG:
- convert_embedding: Chuyển đổi embedding thành định dạng numpy
- gen: Tạo câu trả lời từ context và câu hỏi
- reranking: Sắp xếp lại kết quả tìm kiếm
- Input: Xử lý input từ người dùng
- add_path: Quản lý đường dẫn

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

from .convert_embedding import Embedding_To_Numpy
from .gen import *
from .reranking import *