# voice-agent

A voice-based AI assistant built with Python, Streamlit, and Groq, integrating speech-to-text, LLM inference, text-to-speech, and persistent conversation sessions.

## Technologies

* Python
* Streamlit
* Groq API
* Whisper Large V3 Turbo
* GPT-OSS 20B
* Orpheus TTS
* audio_recorder_streamlit
* python-dotenv
* JSON

## Features

i) Voice input through the browser microphone
ii) Speech-to-text using Whisper Large V3 Turbo
iii) AI responses using GPT-OSS 20B
iv) Text-to-speech using Orpheus TTS
v) Multi-turn conversation context
vi) Persistent conversation sessions
vii) Multiple saved conversations
viii) Custom Streamlit interface

## Architecture

The application follows a voice-to-voice pipeline:

```text
Voice Input
    ↓
Whisper Speech-to-Text
    ↓
GPT-OSS 20B
    ↓
Orpheus Text-to-Speech
    ↓
Audio Response
```

## Implementation

### Speech-to-Text

Recorded audio is processed using Groq's `whisper-large-v3-turbo` model and converted into text.

### LLM

The transcribed text and conversation history are sent to `openai/gpt-oss-20b` through the Groq API to generate the assistant response.

### Text-to-Speech

The generated response is converted into WAV audio using `canopylabs/orpheus-v1-english`.

### Session Management

Conversation sessions are stored locally in `sessions.json`. Each session maintains the user's messages and assistant responses, allowing previous conversations to be reopened.

## Setup

i) Install dependencies:

```bash
pip install streamlit audio_recorder_streamlit groq python-dotenv
```

ii) Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

iii) Run the application:

```bash
streamlit run app.py
```

## Project Structure

```text
voice-agent/
├── app.py
├── api.py
├── README.md
└── .env
```

## Purpose

This project demonstrates the implementation of an end-to-end AI voice assistant, covering speech recognition, LLM integration, text-to-speech, conversational context, API integration, and session management.


## Steps:

i) Install necessary libraries

```bash
pip install streamlit audio_recorder_streamlit groq python-dotenv

Features:
Speech to text using Whisper
AI responses using Groq
Text to speech
Voice-based conversation
Conversation history
Saved sessions
New conversations
