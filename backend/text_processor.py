from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


class TextProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "।", ".", " ", ""]
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="ai4bharat/indic-bert",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

    def split_text(self, text: str) -> List[str]:
        return self.text_splitter.split_text(text)

    def create_embeddings(self, chunks: List[str]) -> Chroma:
        return Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
