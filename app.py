#importing libraries
import streamlit as st 
from audio_recorder_streamlit import audio_recorder
import openai
import base64



def main():
    st.sidebar.title("API KEY CONFIGURATION")
    api_key = st.sidebar.text_input("Enter your OpenAI api key here", type="password")
    st.title("Ultimate AI Agent")
    st.write("Click on the recorder to talk with the ultimate ai agent ")
    recorded_audio = audio_recorder()


if __name__ == "__main__":
    main()