"""
Module chuyển đổi embedding thành định dạng numpy.

Module này chịu trách nhiệm:
- Chuyển đổi embedding từ string sang numpy array
- Xử lý dữ liệu embedding từ pandas Series
- Cung cấp interface để convert embedding cho vector database

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

from .add_path import add
add()

from package import (
    ast,
    pandas as pd,
    numpy as np,
    NDArray
)

class Embedding_To_Numpy:
    """
    Class chuyển đổi embedding từ pandas Series sang numpy array.
    
    Class này chịu trách nhiệm:
    - Nhận embedding dưới dạng pandas Series
    - Chuyển đổi từ string representation sang numpy array
    - Cung cấp interface để truy cập dữ liệu đã convert
    """
    
    def __init__(self, array_embedding : pd.core.series.Series = None) -> None:
        """
        Khởi tạo Embedding_To_Numpy với array embedding.
        
        Args:
            array_embedding: Vector embedding sau khi chunking của từng đoạn
        """
        self.__array_embedding : pd.core.series.Series = array_embedding

    @property
    def get_data(self):
        """
        Lấy dữ liệu embedding đã được parse.
        
        Chuyển đổi từ string representation sang list/array
        sử dụng ast.literal_eval.
        
        Returns:
            NDArray chứa embedding đã được parse
        """
        embedding : NDArray[np.int32] = self.__array_embedding.apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        return embedding
    
    @property
    def convert_to_numpy(self) -> NDArray[np.int32]:
        """
        Chuyển đổi embedding thành numpy array.
        
        Returns:
            NDArray chứa embedding dưới dạng numpy array
        """
        return np.array(np.array(self.get_data.tolist()))