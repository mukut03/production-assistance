import os
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from internal.langchain_.pormpts import req_parser
from constants import model, openai_key

openai_api_key = openai_key

if openai_api_key is None:
    print("OpenAPI key not found")
else:
    print("OpenAI key found")
def get_dict(vs, prompt):
    persist_directory = vs
    embedding = OpenAIEmbeddings(openai_api_key = openai_api_key)
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    llm = ChatOpenAI(model_name=model, temperature=0, openai_api_key = openai_api_key)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
    )
    return req_parser.parse((qa_chain({"query":prompt})["result"]))
