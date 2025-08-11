"""
Module đọc file cho hệ thống.

Module này chịu trách nhiệm:
- Đọc file CSV và JSON
- Quản lý đường dẫn file
- Cung cấp interface để truy cập dữ liệu từ file
- Xử lý encoding và format dữ liệu

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

import sys
import os

# thêm path thủ công 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from package import (
    pandas as pd,
    Dict,
    json
)

class Get_Path:
    """
    Class cơ sở để quản lý đường dẫn file.
    
    Class này chịu trách nhiệm:
    - Lưu trữ đường dẫn file
    - Cung cấp interface cơ sở cho các class đọc file
    """
    
    def __init__(self,path : str)->None:
        """
        Khởi tạo Get_Path với đường dẫn file.
        
        Args:
            path: Đường dẫn đầu vào
        """
        self.path = path

class Read_File_CSV(Get_Path):
    """
    Class đọc file CSV.
    
    Class này chịu trách nhiệm:
    - Đọc file CSV sử dụng pandas
    - Trả về DataFrame chứa dữ liệu
    - Kế thừa từ Get_Path để quản lý đường dẫn
    """
    
    def __init__(self, path : str) -> None:
        """
        Khởi tạo Read_File_CSV với đường dẫn file CSV.
        
        Args:
            path: Đường dẫn đến file csv
        """
        super().__init__(path)
        '''
        Kế thừa đường dẫn từ class Get_Path
        '''
        
    @property
    def Read(self)-> pd:
        """
        Đọc file CSV và trả về DataFrame.
        
        Returns:
            pandas.DataFrame chứa dữ liệu từ file CSV
        """
        return pd.read_csv(self.path)
    
class Read_File_Json(Get_Path):
    """
    Class đọc file JSON.
    
    Class này chịu trách nhiệm:
    - Đọc file JSON với encoding UTF-8
    - Trả về dữ liệu dưới dạng Python object
    - Kế thừa từ Get_Path để quản lý đường dẫn
    """
    
    def __init__(self, path : str) -> None:
        """
        Khởi tạo Read_File_Json với đường dẫn file JSON.
        
        Args:
            path: Đường dẫn đến file json
        """
        super().__init__(path)
    
    @property
    def Read(self):
        """
        Đọc file JSON và trả về dữ liệu.
        
        Returns:
            Python object chứa dữ liệu từ file JSON
        """
        with open(self.path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data
#  -> list[Dict[str, str | Dict[str, str]]]