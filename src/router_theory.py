"""
Module định tuyến câu hỏi và xử lý phản hồi cho hệ thống vật lý.

Module này chịu trách nhiệm:
- Khởi tạo các model embedding và reranking
- Tải vector database đã được lưu trước
- Xử lý câu hỏi của người dùng và trả về câu trả lời
- Quản lý cấu hình từ file YAML

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

from dataclasses import dataclass, field
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from FlagEmbedding import FlagReranker
import json

from typing import (
    List,
    Dict
)

from src.Agent_theory.RAG.reranking import get_information
from src.Agent_theory.RAG.gen import Answer_Question_From_Documents
import yaml
from pathlib import Path


path_config_information_model_llm : str = Path(__file__).parent.parent / "config_information_model_llm.yaml"    

with open(path_config_information_model_llm, "r") as file:
    information_rag : Dict[str, str] = yaml.safe_load(file) 


MODEL_NAME_EMBEDDING : str = information_rag["model_embedding"]  
MODEL_NAME_RERANKING : str = information_rag["model_reranking"] 

device : str = information_rag["device"]  
encode_kwargs : str = information_rag["encode_kwargs"]  
path_save_VectorDB : str = information_rag["path_save_VectorDB"] 
path_dataset_file_json : str = information_rag["path_dataset_file_json"] 


@dataclass
class Call_Model:
    """
    Dataclass chứa các model cần thiết cho hệ thống RAG.
    
    Attributes:
        model_embedding: Model HuggingFace để tạo embedding
        vectorDB: Vector database FAISS đã được lưu trước
        reranking: Model FlagReranker để sắp xếp lại kết quả
    """
    model_embedding : HuggingFaceEmbeddings = field(default_factory=lambda: HuggingFaceEmbeddings(
        model_name=MODEL_NAME_EMBEDDING,
        model_kwargs={'device': device}
    ))

    vectorDB : FAISS = field(default_factory=lambda: FAISS.load_local(
        path_save_VectorDB, 
        HuggingFaceEmbeddings(
            model_name=MODEL_NAME_EMBEDDING,
            model_kwargs={'device': device}
        ),  
        allow_dangerous_deserialization=True
    ))
    reranking : FlagReranker = field(default_factory=lambda: FlagReranker(
        MODEL_NAME_RERANKING, 
        use_fp16=True
    ))

call_model : dataclass = Call_Model()

class Respone:
    """
    Class chính để xử lý câu hỏi và trả về câu trả lời.
    
    Class này chịu trách nhiệm:
    - Nhận câu hỏi từ người dùng
    - Tìm kiếm thông tin liên quan từ vector database
    - Tạo câu trả lời dựa trên thông tin tìm được
    """
    
    def __init__(self, user_query : str) -> None:
        """
        Khởi tạo Respone với câu hỏi của người dùng.
        
        Args:
            user_query: Câu hỏi của người dùng
        """
        self.user_query : str = user_query

    @property
    def get_informatin_json(self) -> str:
        """
        Đọc file JSON chứa thông tin dataset.
        
        Returns:
            Dict chứa thông tin từ file JSON
        """
        with open(path_dataset_file_json, "r", encoding="utf-8") as file:
            return json.load(file)

    @property
    def get_context(self) -> str:
        """
        Lấy context liên quan đến câu hỏi từ vector database.
        
        Returns:
            String chứa context liên quan
        """
        return get_information(self.user_query,call_model.vectorDB, call_model.reranking,self.get_informatin_json)

    @property
    def get_respone(self) -> str:
        """
        Tạo câu trả lời dựa trên câu hỏi và context.
        
        Returns:
            String chứa câu trả lời từ AI
        """
        return Answer_Question_From_Documents(self.user_query,self.get_context).run

