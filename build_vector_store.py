
import os
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 1. Load Data
def load_data():
    # Option A: Load from the txt we extracted
    try:
        with open("pdf_content.txt", "r", encoding="utf-8") as f:
            text = f.read()
            return [Document(page_content=text, metadata={"source": "resume_pdf"})]
    except Exception as e:
        print(f"Error loading text file: {e}")
        return []

# 2. Chunk Data
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

# 3. Create Vector Store
def create_vector_store(chunks):
    # Use a small, fast, local embedding model
    print("Loading embedding model (this may take a minute first time)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Creating FAISS index...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save locally
    vector_store.save_local("faiss_index")
    print("FAISS index saved to 'faiss_index' folder.")

if __name__ == "__main__":
    print("Starting Index Build...")
    docs = load_data()
    if docs:
        chunks = split_text(docs)
        create_vector_store(chunks)
        print("Index build complete!")
    else:
        print("No documents found.")
