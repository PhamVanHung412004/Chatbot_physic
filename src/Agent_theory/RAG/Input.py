"""
Module xử lý input cho hệ thống RAG.

Module này chịu trách nhiệm:
- Khởi tạo và quản lý input từ người dùng
- Xử lý các tham số đầu vào cho hệ thống
- Cung cấp interface để truy cập input parameters

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

class Init_Input:
    """
    Class khởi tạo và quản lý input cho hệ thống.
    
    Class này chịu trách nhiệm:
    - Lưu trữ câu hỏi của người dùng
    - Quản lý tham số top_k cho tìm kiếm
    - Cung cấp interface để truy cập input
    """
    
    def __init__(self, use_query : str = None, top_k : int = None) -> None:
        """
        Khởi tạo Init_Input với câu hỏi và tham số tìm kiếm.
        
        Args:
            use_query: Câu hỏi của người dùng
            top_k: Số lượng kết quả top cần lấy
        """
        self.use_query : str = use_query
        self.top_k : int = top_k