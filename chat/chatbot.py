from llama_index.core import SimpleDirectoryReader

from llama_index.core import VectorStoreIndex, StorageContext,load_index_from_storage
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.schema import ImageDocument
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import PromptTemplate
import chromadb
from llama_index.core import Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from pathlib import Path
from django.conf import settings

import os
from .models import Collection, DataSource


# Settings.embed_model = GeminiEmbedding(
#         model_name="models/embedding-001", api_key=gemini_key
#     )
# import torch
from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate
qa_prompt_tmpl_str = """\
Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, \
answer the query asking about citations over different topics.
Please provide your answer with proper html format containing: code tag when generating code snippets \
avoid using words like based on context data or words that reference context data.
you are assistant built to help answer questions.
Query: {query_str}
Answer: \
"""

query_wrapper_prompt = PromptTemplate(qa_prompt_tmpl_str)



def load_collection(collection_id):
    num_outputs = 512
    collection = Collection.objects.get(id=collection_id)
    data = DataSource.objects.filter(collection=collection)
    collect_data = Path(settings.BASE_DIR)/f"collections/{data[0].document_folder_name}/data"
    gemini_model = Gemini(model="models/gemini-pro", api_key=gemini_key)
    Settings.llm = gemini_model
    directory_path =f'{settings.BASE_DIR}/collections/{data[0].document_folder_name}/'
    print(collect_data)    

    if not collect_data.exists():
        ## create the index 
        print('not existing')
       
        docs = SimpleDirectoryReader(directory_path).load_data()
        saved_vectors = chromadb.PersistentClient(path=f'{directory_path}/chromadb')
        text_collection = saved_vectors.get_or_create_collection('text_collection')
        text_store = ChromaVectorStore(chroma_collection=text_collection)
        storage_context = StorageContext.from_defaults(vector_store=text_store)
        index = VectorStoreIndex.from_documents(documents=docs, storage_context=storage_context)

        index.storage_context.persist(persist_dir=f"{settings.BASE_DIR}/collections/{data[0].document_folder_name}/data")
        query_engine = index.as_query_engine(text_qa_template=query_wrapper_prompt)

        return query_engine
    else:
        saved_vectors = chromadb.PersistentClient(path=f'{directory_path}/chromadb')
        text_collection = saved_vectors.get_collection('text_collection')
        text_store = ChromaVectorStore(chroma_collection=text_collection)
        storage_context = StorageContext.from_defaults(persist_dir=collect_data, vector_store=text_store)
        index = load_index_from_storage(storage_context)
        query_engine = index.as_query_engine(text_qa_template=query_wrapper_prompt)
    
    return query_engine


def chatbot(input_text, collection_id):
    query_engine = load_collection(collection_id)
    
    # query_engine.update_prompts({"response_synthesizer:summary_template": query_wrapper_prompt})

    response = query_engine.query(input_text)
    print(response)
    return response.response
   
