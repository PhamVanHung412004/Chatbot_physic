from tqdm import tqdm
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import math
import os

def read_Vector_DB(path_VectorDB: str, embeddings=None):
    """
    Đọc Vector Database từ đường dẫn đã persist
    
    Args:
        path_VectorDB (str): Đường dẫn đến folder chứa Vector DB
        embeddings: Embedding function (nếu None sẽ dùng OpenAIEmbeddings)
    
    Returns:
        Chroma: Vector database đã load
    """
    try:
        # Kiểm tra đường dẫn có tồn tại không
        if not os.path.exists(path_VectorDB):
            raise FileNotFoundError(f"Đường dẫn {path_VectorDB} không tồn tại")
        
        # Nếu không có embeddings thì dùng mặc định
        if embeddings is None:
            embeddings = OpenAIEmbeddings()
        
        # Load vectorstore từ persist directory
        vectorstore = Chroma(
            persist_directory=path_VectorDB,
            embedding_function=embeddings
        )
        
        print(f"✅ Đã load Vector DB từ: {path_VectorDB}")
        
        # Kiểm tra số lượng documents trong DB
        try:
            collection = vectorstore._collection
            count = collection.count()
            print(f"📊 Số lượng documents trong DB: {count}")
        except Exception as e:
            print(f"⚠️  Không thể đếm documents: {e}")
        
        return vectorstore
        
    except Exception as e:
        print(f"❌ Lỗi khi đọc Vector DB: {e}")
        raise e

def create_vectorstore_with_progress(documents, embeddings, persist_directory, batch_size) -> Chroma:
    """Tạo vectorstore với progress bar"""
    
    # Tạo folder nếu chưa có
    os.makedirs(persist_directory, exist_ok=True)
    
    all_list = os.listdir(persist_directory)
    
    if (len(all_list) == 0):
        print("Chưa có VectorDB tôi sẽ tạo VectorDB mới")
        # Khởi tạo Chroma trống
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
    else:
        print("Đã có VectorDB bây giờ sẽ đọc và thêm dữ liệu")
        vectorstore = read_Vector_DB(persist_directory, embeddings)
    
    # Chia documents thành batches
    total_docs = len(documents)
    num_batches = math.ceil(total_docs / batch_size)
    
    print(f"📝 Tổng số documents: {total_docs}")
    print(f"📦 Số batches: {num_batches}")
    print(f"🔢 Batch size: {batch_size}")
    
    # Progress bar
    with tqdm(total=total_docs, desc="Bắt đầu embedding: ") as pbar:
        for i in range(0, total_docs, batch_size):
            # Lấy batch hiện tại
            batch = documents[i:i + batch_size]
            
            try:
                # Thêm batch vào vectorstore
                vectorstore.add_documents(documents=batch)
                
                # Update progress bar
                pbar.update(len(batch))
                
                # Optional: hiển thị thêm info
                pbar.set_postfix({
                    'batch': f"{i//batch_size + 1}/{num_batches}",
                    'total_added': i + len(batch)
                })
                
            except Exception as e:
                print(f"❌ Lỗi khi thêm batch {i//batch_size + 1}: {e}")
                continue
    
    # Persist sau khi xong
    print("💾 Persisting to disk...")
    vectorstore.persist()
    print("✅ Complete!")
    