from internal.langchain_.dochandler import ls_, store
from internal.langchain_.reqhandler import get_dict
import os

def get_response(prompt, vs):
    new_response = get_dict(vs, prompt)
    return new_response

def embed(scriptID, filename):
    pdf_path = os.path.join(filename)
    vector_store = store(ls_(pdf_path), scriptID)
    return vector_store
