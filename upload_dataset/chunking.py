from langchain_huggingface import HuggingFaceEmbeddings
from typing import (
    List,
    Dict
)
from dataclasses import dataclass
import yaml
from pathlib import Path

from .RAG import (
    get_data,
    Chunking_Data,
    create_vectorstore_with_progress
)


path_file_config : str = (Path(__file__).parent.parent / "config_information_model_llm.yaml")

with open(path_file_config, "r") as file:
    data_config : Dict[str, str] = yaml.safe_load(file)


MODEL_NAME_EMBEDDING : str = data_config["model_embedding"]  

def document_loader(path_data_pdf : str) -> List[str]: 
    documents : List[str] = get_data(path_data_pdf).read
    return documents

def chunking(documents) -> List[str]:
    data_split : List[str] = Chunking_Data(documents,MODEL_NAME_EMBEDDING).run
    return data_split

class Create_VectorDB_Update_Dataset:
    def __init__(self, path_folder : str, path_save_vector_DB : str) -> None:
        self.__path_folder : str = path_folder
        self.__path_save_vector_DB : str = path_save_vector_DB
    
    @property
    def run(self) -> None:
        documents : List[str] = document_loader(self.__path_folder)        
        data_split : List[str] = chunking(documents)
        create_vectorstore_with_progress(
            documents=data_split,
            embeddings=MODEL_NAME_EMBEDDING,
            persist_directory=self.__path_save_vector_DB,
            batch_size=100
        )
