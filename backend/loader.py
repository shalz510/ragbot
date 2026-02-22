from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(file_path):
    """
    Load PDF, TXT, DOCX documents and return chunked LangChain Documents
    """

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        documents = loader.load()

    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()

    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
        documents = loader.load()

    else:
        raise ValueError("Unsupported file format")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return text_splitter.split_documents(documents)
