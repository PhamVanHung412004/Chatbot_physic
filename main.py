# """
# Hệ thống giải quyết bài tập vật lý - Main Entry Point

# Module này cung cấp giao diện dòng lệnh để tương tác với hệ thống AI
# giải quyết bài tập vật lý. Người dùng có thể nhập câu hỏi và nhận
# câu trả lời từ hệ thống.

# Author: Physics Problem Solving System Team
# Version: 1.0.0
# """

# # from src import (
# #     Respone

# # )

# from Flow_splitter_agent import (
#     classify_physics_question
# )

# def result_check(user_query : str) -> str:
#     result : str = classify_physics_question(user_query)
#     if (result == "THEORY"):
#         ...
#     elif (result == "PRACTICE"):
#         ...
#     else:
#         ...

# # def main():
# #     """
# #     Hàm chính để chạy hệ thống giải quyết bài tập vật lý.
    
# #     Tạo một vòng lặp vô hạn để nhận câu hỏi từ người dùng và
# #     trả về câu trả lời từ hệ thống AI. Người dùng có thể thoát
# #     bằng cách nhấn Ctrl+C.
    
# #     Returns:
# #         None
        
# #     Raises:
# #         KeyboardInterrupt: Khi người dùng nhấn Ctrl+C để thoát
# #     """
# #     result_check : str = classify_physics_question("Định luật Newton thứ nhất là gì?")
# #     print(result_check)   
# # if __name__ == "__main__":
# #     main()
from upload_dataset import Create_VectorDB_Update_Dataset

path_folder = "dataset_test"
Create_VectorDB_Update_Dataset(path_folder,"dataset/dataset_theory").run



