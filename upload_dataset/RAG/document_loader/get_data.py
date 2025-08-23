from langchain.document_loaders import DirectoryLoader, PyPDFLoader, Docx2txtLoader
from typing import List

class get_data:
    def __init__(self, path_folder: str) -> None:
        """
        path_folder : đường dẫn đến folder chứa file pdf và word
        """
        self.__path_folder: str = path_folder
    
    # hàm đọc file pdf và word trong folder chuyển về dạng list
    @property
    def read(self) -> List[str]:
        documents = []
        
        # Đọc file PDF
        pdf_loader = DirectoryLoader(
            path=self.__path_folder,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        pdf_docs = pdf_loader.load()
        documents.extend(pdf_docs)
        
        # Đọc file Word (.docx)
        docx_loader = DirectoryLoader(
            path=self.__path_folder,
            glob="**/*.docx",
            loader_cls=Docx2txtLoader,
            show_progress=True
        )
        docx_docs = docx_loader.load()
        documents.extend(docx_docs)
        
        # Đọc file Word (.doc)
        try:
            doc_loader = DirectoryLoader(
                path=self.__path_folder,
                glob="**/*.doc",
                loader_cls=Docx2txtLoader,
                show_progress=True
            )
            doc_docs = doc_loader.load()
            documents.extend(doc_docs)
        except Exception as e:
            print(f"Không thể đọc file .doc: {e}")
        
        return documents