from llama_index.core import SimpleDirectoryReader

from llama_index.core import VectorStoreIndex, StorageContext,load_index_from_storage
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.schema import ImageDocument
# from llama_index.llms import OpenAI
from pathlib import Path
from django.conf import settings
import os
from .models import Collection, DataSource

# import torch
# from llama_index.llms import HuggingFaceLLM
# from llama_index.prompts import PromptTemplate
# SYSTEM_PROMPT = """You are an AI assistant that answers questions in a friendly manner, based on the given source documents. Here are some rules you always follow:
# - Generate human readable output, avoid creating output with gibberish text.
# - Generate only the requested output, don't include any other language before or after the requested output.
# - Never say thank you, that you are happy to help, that you are an AI agent, etc. Just answer directly.
# - Generate professional language typically used in business documents in North America.
# - Never generate offensive or foul language.
# """

# query_wrapper_prompt = PromptTemplate(
#     "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "



def load_collection(collection_id):
    num_outputs = 512

    collection = Collection.objects.get(id=collection_id)
    data = DataSource.objects.filter(collection=collection)
    print(data[0].document_folder_name)
    
    collect_data = Path(settings.BASE_DIR)/f"collections/{data[0].document_folder_name}/data"
    # check if the index file exist
    print(collect_data)    

    if not collect_data.exists():
        ## create the index 
        print('not existing')
        directory_path =f'{settings.BASE_DIR}/collections/{data[0].document_folder_name}/'
        docs = SimpleDirectoryReader(directory_path).load_data()
        index = VectorStoreIndex.from_documents(docs)
        index.storage_context.persist(persist_dir=f"{settings.BASE_DIR}/collections/{data[0].document_folder_name}/data")
    else:
        storage_context = StorageContext.from_defaults(persist_dir=collect_data)
        index = load_index_from_storage(storage_context)
        
    return index


def chatbot(input_text, collection_id):
    index = load_collection(collection_id)
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response
   
