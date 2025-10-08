from typing import List
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL_NAME, TOP_K

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.store = None

    def create(self, documents: List[Document]):
        self.store = FAISS.from_documents(documents, self.embeddings)
        return self.store

    def search(self, query: str, k: int = TOP_K) -> List[Document]:
        return self.store.similarity_search(query, k=k)

    def as_retriever(self):
        return self.store.as_retriever(search_kwargs={"k": TOP_K})

