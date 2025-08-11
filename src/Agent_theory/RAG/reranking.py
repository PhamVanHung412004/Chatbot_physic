"""
Module reranking cho hệ thống RAG.

Module này chịu trách nhiệm:
- Sắp xếp lại kết quả tìm kiếm từ vector database
- Sử dụng FlagReranker để cải thiện độ chính xác
- Kết hợp similarity search và reranking
- Trả về kết quả có độ liên quan cao nhất

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

from FlagEmbedding import FlagReranker
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Tuple, Optional
from langchain.schema import Document
import logging
from typing import (
    List,
    Dict
)

# Setup logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Reranking:
    """
    Class thực hiện reranking cho kết quả tìm kiếm.
    
    Class này chịu trách nhiệm:
    - Lấy kết quả ban đầu từ vector database
    - Sắp xếp lại kết quả sử dụng FlagReranker
    - Kết hợp similarity search và reranking
    - Trả về kết quả có độ liên quan cao nhất
    """
    
    def __init__(self, user_query: str) -> None:
        """
        Initialize Reranking với user query
        
        Args:
            user_query: Câu hỏi của người dùng
        """
        self.__user_query: str = user_query

    def get_initial_results(self, vectordb : FAISS , k: int = 10) -> List[Document]:
        """
        Lấy kết quả ban đầu từ FAISS
        
        Args:
            vectordb: Vector database FAISS
            k: Số lượng documents cần retrieve
            
        Returns:
            List các documents
        """
        return vectordb.similarity_search(self.__user_query, k=k)
    
    def rerank_results(
        self, 
        reranker : FlagReranker,
        initial_results: List[Document], 
        top_n: int = 3
    ) -> List[Tuple[Document, float]]:
        """
        Rerank các kết quả sử dụng FlagReranker
        
        Args:
            reranker: Model FlagReranker để tính điểm
            initial_results: Danh sách documents ban đầu
            top_n: Số lượng kết quả top cần giữ lại
            
        Returns:
            List các tuples (document, score) đã được sắp xếp
        """
        # Chuẩn bị pairs cho reranker
        pairs: List[List[str]] = [
            [self.__user_query, doc.page_content] 
            for doc in initial_results
        ]
        
        # Compute scores
        scores = reranker.compute_score(pairs)
        
        # Sắp xếp theo điểm
        ranked_results = sorted(
            zip(initial_results, scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        return ranked_results
    
    def search_with_reranking(
        self, 
        VectorDB : FAISS,
        reranker : FlagReranker,
        initial_k: int = 10, 
        top_n: int = 3,
        return_scores: bool = True
    ) -> List[Tuple[Document, float]] | List[Document]:
        """
        Thực hiện search với reranking
        
        Quy trình:
        1. Lấy kết quả ban đầu từ vector database
        2. Sắp xếp lại kết quả sử dụng reranker
        3. Trả về top_n kết quả có điểm cao nhất
        
        Args:
            VectorDB: Vector database FAISS
            reranker: Model FlagReranker
            initial_k: Số documents ban đầu để retrieve
            top_n: Số documents sau reranking
            return_scores: Có trả về scores hay không
            
        Returns:
            List documents hoặc list tuples (document, score)
        """
        # Bước 1: Retrieve
        initial_results = self.get_initial_results(vectordb=VectorDB,k=initial_k)
        
        # Bước 2: Rerank
        ranked_results = self.rerank_results(reranker,initial_results, top_n=top_n)
        
        if return_scores:
            return ranked_results
        else:
            return [doc for doc, _ in ranked_results]
    

def get_information(user_query : str, VectorDB : FAISS, reranking : FlagReranker, dataset_dict : Dict[str, str]) -> str:
    """
    Hàm chính để lấy thông tin liên quan từ vector database.
    
    Thực hiện quá trình:
    1. Tìm kiếm với reranking
    2. Lấy nội dung từ dataset dictionary
    3. Kết hợp thành một chuỗi text
    
    Args:
        user_query: Câu hỏi của người dùng
        VectorDB: Vector database FAISS
        reranking: Model FlagReranker
        dataset_dict: Dictionary chứa mapping từ câu hỏi sang nội dung
        
    Returns:
        String chứa nội dung liên quan được kết hợp
    """
    array_result = Reranking(user_query).search_with_reranking(
        VectorDB,
        reranking,
        initial_k=15, 
        top_n=5,
        return_scores=True
    )

    array_text_result : List[str] = [dataset_dict[doc.page_content] for doc, score in array_result]
    
    return "\n".join(array_text_result)
        
