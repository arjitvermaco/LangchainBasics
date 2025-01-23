import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


# Define the directory containing the text file and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data", "facts.txt")
persistent_dir = os.path.join(current_dir, "db", "chroma_db")

if not os.path.exists(persistent_dir):
    print("Creating persistent directory")
    
     # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )
    
    loader = TextLoader(file_path)
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

        # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")
    print(f"Sample chunk:\n{docs[0].page_content}\n")
    
    print("Creating Embeddings")
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    
    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=persistent_dir
    )
    
    db.persist()
    print("Embeddings created and persisted")

else:
    print("Vector Store already exists")

