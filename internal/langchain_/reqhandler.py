from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from internal.langchain_.pormpts import req_parser, image_prompt
from constants import model, openai_key
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import os
from internal.imageGen import image_generator


os.environ["OPENAI_API_KEY"] = openai_key
openai_api_key = openai_key



if openai_api_key is None:
    print("OpenAPI key not found")
else:
    print("OpenAI key found")

llm = ChatOpenAI(model_name=model, temperature=0, openai_api_key = openai_api_key)
llm_ = OpenAI(temperature=0.2)
client = OpenAI()

def get_dict(vs, prompt):
    embedding = OpenAIEmbeddings(openai_api_key = openai_api_key)
    vectordb = Chroma(persist_directory=vs, embedding_function=embedding)



    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
    )

    result = qa_chain({"query":prompt})["result"]
    print(result)
    return req_parser.parse(result)

def get_images(sceneDesc, summary, characters, props, image_prompt):
    imageChain = LLMChain(llm=llm_, prompt=image_prompt)
    imgUrl_dict = {}



    for key in sceneDesc:
        prompt_dictionary = {
            "scene_desc": sceneDesc[key],
            "summary": summary,
            "characters": characters,
            "props": props
        }
        final_image_prompt = imageChain.run(prompt_dictionary)
        print("final image prompt: ", final_image_prompt)

        response = image_generator(final_image_prompt)

        img_url = response.data[0].url
        imgUrl_dict[key] = img_url

    return imgUrl_dict

def get_image(sum):
    img_url = DallEAPIWrapper().run(sum)
    return img_url
