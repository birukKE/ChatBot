
import pypdf
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
import os
import re
import uuid
import config
from load_pubmed import query_pubmed

class VectorDatabase():
    def __init__(self):
        embedding = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
        self.vector_db = Chroma(collection_name = "response_docs", 
                                embedding_function=embedding, 
                                persist_directory = '../chroma_db')

    def create_db(self, title, text):
        text_splitter = RecursiveCharacterTextSplitter(
                            # separator='\n\n',
                            chunk_size = config.chunk_size,
                            chunk_overlap=config.chunk_overlap,
                            length_function = len,
                            is_separator_regex= False
                            )
        text_documents = text_splitter.create_documents(texts=[text], metadatas=[{"title": title}])
        self.vector_db.add_documents(text_documents, 
                                            ids = [str(uuid.uuid4()) for _ in range(len(text_documents))])


    def create_pubmed_db(self, user_query):
        documents = query_pubmed(user_query)
        # Meaning if the query didnt lead to any matches
        if documents == None:
            return
        for k, v in documents.items():
            self.create_db(k, v)
            

def load_all_docs(directory_path, filetype, vd_object):
    """Get each of the downloaded files and call load_a_doc on them"""
    for e in os.scandir(directory_path):
        if e.is_file():
            documents = load_a_doc(e.path, e.name, filetype)
            vd_object.vector_db.add_documents(documents, 
                                    ids = [str(uuid.uuid4()) for _ in range(len(documents))])

def load_a_doc(filepath, filename, filetype):
    read_text = ""
    with open(filepath, 'rb') as pdf:
        reader = pypdf.PdfReader(pdf)
        for page in reader.pages:
            read_text += page.extract_text()
    text_splitter = RecursiveCharacterTextSplitter(
                    # separator='\n\n',
                    chunk_size = config.chunk_size,
                    chunk_overlap=config.chunk_overlap,
                    length_function = len,
                    is_separator_regex= False
                    )
    filename = re.split('.' + filetype, filename)[0]
    text_documents = text_splitter.create_documents(texts=[read_text], metadatas=[{"title": filename}])
    
    return text_documents
