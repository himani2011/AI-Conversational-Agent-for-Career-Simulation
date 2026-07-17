from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load text file
loader = TextLoader("rag/career_knowledge.txt")
documents = loader.load()

# Split into chunks
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs = text_splitter.split_documents(documents)

# ✅ FREE LOCAL EMBEDDINGS (no OpenAI needed)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS vector DB
vectorstore = FAISS.from_documents(docs, embeddings)

# Save DB locally
vectorstore.save_local("rag/vector_db")

print("Vector database created successfully (FREE version)!")