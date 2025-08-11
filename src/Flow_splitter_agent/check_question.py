"""
Module kiểm tra và phân loại câu hỏi vật lý.

Module này chịu trách nhiệm:
- Phân loại câu hỏi vật lý theo loại
- Sử dụng model LLM để xác định loại câu hỏi
- Định tuyến câu hỏi đến agent phù hợp
- Xử lý logic phân loại câu hỏi

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

from check_question import Model_LLM


class Check:
    """
    Class kiểm tra và phân loại câu hỏi vật lý.
    
    Class này chịu trách nhiệm:
    - Nhận câu hỏi từ người dùng
    - Sử dụng model LLM để phân loại
    - Trả về loại câu hỏi được xác định
    """
    
    def __init__(self, user_query : str) -> None:
        """
        Khởi tạo Check với câu hỏi của người dùng.
        
        Args:
            user_query: Câu hỏi vật lý của người dùng
        """
        self.user_query : str = user_query
    
    # hàm kiểm tra xem câu hỏi thuộc loại nào
    def Model_LLM_Check(self) -> str:
        """
        Sử dụng model LLM để kiểm tra và phân loại câu hỏi.
        
        Returns:
            String chứa loại câu hỏi được xác định
        """
        text_result = Model_LLM(self.user_query).client_model_llm
        ...