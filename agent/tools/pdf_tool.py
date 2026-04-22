import os
from langchain_core.tools import tool
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTORSTORE_PATH = "vectorstore/"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_pdf(pdf_path: str) -> str:
    """Call this to index a PDF into FAISS vectorstore."""
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_PATH)
    return f"Successfully indexed {len(chunks)} chunks from {pdf_path}"

@tool
def search_pdf(query: str) -> str:
    """Search through uploaded research papers or study notes.
    Use this when the user asks about content from their documents."""
    if not os.path.exists(VECTORSTORE_PATH):
        return "No documents uploaded yet. Please upload a PDF first."
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    results = vectorstore.similarity_search(query, k=4)
    if not results:
        return "No relevant content found in the document."
    return "\n\n---\n\n".join([r.page_content for r in results])