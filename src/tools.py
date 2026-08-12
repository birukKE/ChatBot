import time
import cProfile
import re
import pypdf

start_time = time.time()
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
print(f'{time.time() - start_time} seconds taken to import chroma')



def load_doc():
    read_text = ""
    with open('../sample_data/Demographic_Attributes_Prediction_from_Speech.pdf', 'rb') as pdf:
        reader = pypdf.PdfReader(pdf)

        for page in reader.pages:
            read_text += page.extract_text()
    text_splitter = RecursiveCharacterTextSplitter(
                                            # separator='\n\n',
                                            chunk_size = 1000,
                                            chunk_overlap=100,
                                            length_function = len,
                                            is_separator_regex= False
                                            )
    text_documents = text_splitter.create_documents([read_text])
    return text_documents



def embedding():
    embed_model = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2',
                                        )
    vec_store = Chroma(collection_name = 'my_files',
                           embedding_function = embed_model)
    documents = load_doc()
    # print("The len = ", documents[0])
    doc_ids = [str(i) for i in range(0, len(documents))]
    vec_store.add_documents(documents, ids = doc_ids)

    return vec_store

