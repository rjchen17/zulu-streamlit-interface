import streamlit as st
import os
from code_editor import code_editor

head = st.container()
body = st.container()

aws_access_key_id = os.getenv("aws-key-id")
aws_secret_access_key = os.getenv("aws-secret-key")

with open("app/data/ids.txt") as id_file:
    lines = id_file.readlines()
    user_to_files = {line.split(':')[0]: line.split(':')[1].split(',') for line in lines}
user_authenticated = False

with head:
    st.title("Zulu clause embedding text editor")
    st.text("After entering your user ID below, you will be able to select a file to edit. The editor will\n"
            "prompt you for an audio end time before saving/submitting. This ensures that the audio will\n"
            "start where you left off.")
    user_id = st.text_input("Enter your user ID. ")
    try:
        int(user_id)
    except ValueError:
        st.text("Please enter a valid user ID. ")
    if user_id in user_to_files:
        user_authenticated = True
if user_authenticated:
    with body:
        st.header("Welcome. ")
        st.text("Please choose a file from the following list:")
        file_choice = st.text_input(", ".join(user_to_files[user_id]))
        if file_choice in user_to_files[user_id]:
            st.text("This is a placeholder audio player. ")
            st.text("Edit your code below. Press ctrl+enter to save (cmd+enter on Mac). \n"
                    "Please save before submitting.")
            editor = code_editor("This is a placeholder text file. ", lang="plain_text")

            if st.button("Save to File"):
                if editor["text"] == "":
                    st.write("File is blank. Please save beforehand. ")
                else:
                    st.download_button(label="Download", data=editor["text"], file_name="output.txt")
                    st.success("File saved successfully!")

