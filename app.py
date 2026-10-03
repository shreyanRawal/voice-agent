#importing libraries
import streamlit as st 
from audio_recorder_streamlit import audio_recorder
import openai
import base64

#initialise openai client
def setup_openai_client(api_key):
    return openai.OpenAI(api_key= api_key)

#audio to text
def transcribe_audio(client, audio_path):
    with open(audio_path, "rb") as audio_file:
        transcipt = client.audio.transcriptions.create(model="Whisper-1",file=audio_file)
        return transcipt.text

#llm response
def fetch_ai_response(client, input_text):
    messages=[{"role": "user", "content": input_text}]
    response = client.chat.completions.create(model="gpt-4o-mini")

def main():
    st.sidebar.title("API KEY CONFIGURATION")
    api_key = st.sidebar.text_input("Enter your OpenAI api key here", type="password")
    st.title("Ultimate AI Agent")
    st.write("Click on the recorder to talk with the ultimate ai agent ")
    recorded_audio = audio_recorder()


if __name__ == "__main__":
    main()