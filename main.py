import streamlit as st
from internal.llmresponse import get_response, embed
from internal.langchain_.pormpts import req_template
import os
import uuid

import os
import time

def wait_for_file(file_path, timeout=10, check_interval=0.5):
    """
    Wait for a file to be fully written.

    :param file_path: Path to the file.
    :param timeout: Maximum time to wait in seconds.
    :param check_interval: Time interval between checks in seconds.
    :return: True if the file is ready, False if timeout is reached.
    """
    start_time = time.time()
    last_size = -1

    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)

            if current_size == last_size:
                # File size hasn't changed, assume it's ready
                return True
            else:
                last_size = current_size

        time.sleep(check_interval)

    # Timeout reached, file may not be ready
    return False


# Title of the application
st.title('PDF Information Extractor')

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    save_path = os.getcwd()
    file_name = uploaded_file.name
    complete_path = os.path.join(save_path, file_name)

    # Write the contents of the uploaded file to a new file in the directory
    with open(complete_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    pdf_id = str(uuid.uuid4())

    print(file_name)

    # Now you can pass the complete_path to your embed function
    embedded_pdf = embed('pdf_id', file_name)

    time.sleep(2)

    if wait_for_file(embedded_pdf):
    # Getting response with extracted information
        response = get_response(req_template, embedded_pdf)

    # Displaying the results
    st.subheader("Summary")
    st.write(response.get("summary", "No summary available"))

    st.subheader("Characters")
    st.write(response.get("characters", "No characters information available"))

    st.subheader("Props")
    st.write(response.get("props", "No props information available"))

