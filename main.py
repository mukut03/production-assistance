import pandas as pd
import streamlit as st
from internal.llmresponse import get_response, embed
from internal.ghostDarkness import *
import uuid

import os
import time


st.set_page_config(layout="wide")  # Use the full page width




st.title('AI Assistant for Film Scripts')
st.markdown("""
    Extracts characters, locations, and props from film script PDFs. Generates scenes from the film script. 
""")

#/NM edit
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




# File uploader widget
uploaded_file = st.file_uploader("Choose a script you want to analyze", type="pdf")
if uploaded_file is not None:
    save_path = os.getcwd()
    file_name = uploaded_file.name
    complete_path = os.path.join(save_path, file_name)

    # Write the contents of the uploaded file to a new file in the directory
    with open(complete_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    pdf_id = str(uuid.uuid4())

    print(file_name)

    # Show loading message and spinner
    with st.spinner('Embedding PDF and running inference...'):
        time.sleep(5)

    # Now you can pass the complete_path to your embed function
    embedded_pdf = embed(pdf_id, file_name)

    # call get_response(prompt, vs) to get live responses from llm


    total1,total2,total3 = st.columns(3,gap='large')

    with total1:
        st.image('images/artist.png',use_column_width=True)
        st.metric(label = 'Number of Characters', value=num_char)

    with total2:
        st.image('images/prop.png',use_column_width=True)
        st.metric(label='Number of Props', value=num_prop)

    with total3:
        st.image('images/location.png',use_column_width=True)
        st.metric(label= 'Number of Locations',value=num_loc)

    with st.spinner('Loading summary statistics...'):
        time.sleep(3)


    def dict_to_dataframe(dict):
        return pd.DataFrame(list(dict.items()), columns=['Name', 'Description'])


    char_df = dict_to_dataframe(char_sum)
    prop_df = dict_to_dataframe(prop_sum)
    loc_df = dict_to_dataframe(loc_sum)

    # Display your DataFrames as tables in Streamlit
    with st.expander("Summary of Characters"):
        st.table(char_df)

    with st.expander("Summary of Props"):
        st.table(prop_df)

    with st.expander("Summary of Locations"):
        st.table(loc_df)

    with st.expander("Script Summary"):
        st.write(sum_)

    with st.spinner('Loading possible scene depictions...'):
        time.sleep(10)

    st.markdown("## Scene Depictions")

    st.image('internal/g&dimg/patterson_office.webp', caption='Opening scene introducing Patterson in England', use_column_width=True)
    st.image('internal/g&dimg/meeting.webp', caption='Patterson meeting with Beaumont who tasks him with the Kenya assignment', use_column_width=True)
    st.image('internal/g&dimg/desert_storm.webp', caption='Patterson and Co. helping the stuck train out of a desert storm', use_column_width=True)
    st.image('internal/g&dimg/patterson_africa.webp', caption='Patterson marvelling at the beauty of Africa, as he had previously imagined', use_column_width=True)
    st.image('internal/g&dimg/train_arriving.webp', caption='The train arriving at the Tsavo River Site. The place is surrounded by countless worker camps', use_column_width=True)
    st.image('internal/g&dimg/building_bridge.webp', caption="Patterson's assignment is revealed to the audience visually for the first time: a railway bridge over the Tsavo River", use_column_width=True)
    st.image('internal/g&dimg/lion_entry.webp', caption='The main plot of the movie begins with the introduction of the man-eating Lion lurking in the tall grass', use_column_width=True)

