"""
Module khởi tạo model LLM cho phân loại câu hỏi.

Module này chịu trách nhiệm:
- Khởi tạo model LLM để phân loại câu hỏi
- Xử lý câu hỏi và trả về kết quả phân loại
- Cung cấp interface để tương tác với model LLM

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

class Model_LLM:
    """
    Class khởi tạo và quản lý model LLM.
    
    Class này chịu trách nhiệm:
    - Nhận câu hỏi từ người dùng
    - Khởi tạo model LLM
    - Trả về kết quả phân loại từ model
    """
    
    def __init__(self, user_query : str) -> None:
        """
        Khởi tạo Model_LLM với câu hỏi của người dùng.
        
        Args:
            user_query: Câu hỏi cần phân loại
        """
        self.user_query : str = user_query
    
    @property
    def client_model_llm(self) -> None:
        """
        Gọi model LLM để phân loại câu hỏi.
        
        Returns:
            Kết quả phân loại từ model LLM
        """
        ...
