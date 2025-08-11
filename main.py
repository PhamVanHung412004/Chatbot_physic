"""
Hệ thống giải quyết bài tập vật lý - Main Entry Point

Module này cung cấp giao diện dòng lệnh để tương tác với hệ thống AI
giải quyết bài tập vật lý. Người dùng có thể nhập câu hỏi và nhận
câu trả lời từ hệ thống.

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

from src import Respone

def main():
    """
    Hàm chính để chạy hệ thống giải quyết bài tập vật lý.
    
    Tạo một vòng lặp vô hạn để nhận câu hỏi từ người dùng và
    trả về câu trả lời từ hệ thống AI. Người dùng có thể thoát
    bằng cách nhấn Ctrl+C.
    
    Returns:
        None
        
    Raises:
        KeyboardInterrupt: Khi người dùng nhấn Ctrl+C để thoát
    """
    # while(True):
    user_query : str = input("Câu hỏi: ")
    answers = Respone(user_query).get_respone
    print(answers)

if __name__ == "__main__":
    main()
