"""
Module lưu trữ và khởi tạo Vector Database cho hệ thống RAG.

Module này chịu trách nhiệm:
- Đọc dataset từ file CSV
- Chuyển đổi embedding thành định dạng numpy
- Khởi tạo và lưu trữ vector database FAISS
- Quản lý việc tạo và lưu trữ vector embeddings

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import pandas
from typing import (
    List
) 

from RAG import Embedding_To_Numpy
from read_file import Read_File_CSV


class INIT_VectorDB:
    """
    Class khởi tạo và lưu trữ Vector Database.
    
    Class này chịu trách nhiệm:
    - Đọc dataset từ file CSV
    - Chuyển đổi embedding thành định dạng phù hợp
    - Tạo và lưu trữ vector database FAISS
    """
    
    def __init__(self, Model_Embeding : HuggingFaceEmbeddings) -> None:
        """
        Khởi tạo INIT_VectorDB với model embedding.
        
        Args:
            Model_Embeding: Model HuggingFace để tạo embedding
        """
        self.__Model_Embedding : HuggingFaceEmbeddings = Model_Embeding

    @property
    def run(self) -> None:
        """
        Thực hiện quá trình khởi tạo và lưu trữ vector database.
        
        Quy trình:
        1. Đọc dataset từ file CSV
        2. Chuyển đổi embedding thành định dạng numpy
        3. Tạo vector database FAISS
        4. Lưu trữ vào thư mục VectorDB_physic_theory
        """
        # Đọc dataset dưới dạng pandas
        dataset : pandas = Read_File_CSV("dataset.csv").Read

        # # Văn bản lưu trong list
        documents : List[str] = list(dataset["Cau_hoi"])

        # # Embeding của từng văn bản trong danh sách
        vector_embeddings : List[list[float]] = list(Embedding_To_Numpy(dataset["Embedding"]).convert_to_numpy) 
        vector_embeddings_new = [list(i) for i in vector_embeddings]

        # Khởi tạo VectorDB với FAISS trong langchain
        VectorDB : FAISS = FAISS.from_embeddings(
            text_embeddings=vector_embeddings_new, 
            documents=documents, 
            embedding=self.__Model_Embedding
        )
        VectorDB.save_local("VectorDB_physic_theory")

def main() -> None:
    """
    Hàm chính để chạy quá trình khởi tạo vector database.
    
    Khởi tạo model embedding và chạy quá trình tạo vector database.
    """
    model_embeding : HuggingFaceEmbeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    INIT_VectorDB(model_embeding).run

if __name__ == '__main__':
    main()
