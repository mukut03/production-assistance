from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

#keys
from constants import openai_key

api_key = openai_key
if api_key is None:
    print("API key not found in environment variables.")
else:
    print("API key:", api_key)


#manual_load and split
def ls_(path):

    loader = PyPDFLoader(path)
    pages = loader.load()

    text_splitter = CharacterTextSplitter(
        separator=".",
        chunk_size=3500,
        chunk_overlap=200,
        length_function=len
    )

    return text_splitter.split_documents(pages)


def store(docs, file):
    embedding = OpenAIEmbeddings(openai_api_key = api_key)

    #TODO: VINTAI-17
    persist_directory = os.path.join('docs/chroma/', file)

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_directory
    )
    if vectordb:
        return persist_directory
    return "vector storage error"
