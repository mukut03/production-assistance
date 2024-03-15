from openai import OpenAI
from constants import openai_key
import os
os.environ["OPENAI_API_KEY"] = openai_key
client = OpenAI()

def image_generator(prompt):
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )
    return response