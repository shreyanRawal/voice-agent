# importing libraries
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from groq import Groq
from api import API_KEY
import base64
import json
import os
import uuid
from datetime import datetime


# page configuration
st.set_page_config(
    page_title="Ultimate AI Agent",
    page_icon="🎙️",
    layout="wide"
)


# custom css
st.markdown("""
<style>

    .stApp {
        background: #f7f9fc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8ecf2;
    }

    [data-testid="stSidebar"] > div {
        padding-top: 25px;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #17202a;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #718096;
        font-size: 16px;
        margin-bottom: 18px;
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #ffffff;
        border: 1px solid #e3e8ef;
        padding: 7px 13px;
        border-radius: 20px;
        color: #667085;
        font-size: 13px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #18b878;
        border-radius: 50%;
        display: inline-block;
    }

    .recording-box {
        background: #ffffff;
        border: 1px solid #e7ebf0;
        border-radius: 22px;
        padding: 22px;
        margin-top: 20px;
        text-align: center;
        box-shadow: 0 6px 25px rgba(31, 41, 55, 0.04);
    }

    .sidebar-logo {
        color: #17202a;
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 3px;
    }

    .sidebar-subtitle {
        color: #8a94a3;
        font-size: 13px;
        margin-bottom: 22px;
    }

    .conversation-label {
        color: #98a2b3;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.7px;
        margin: 22px 0 10px 0;
    }

    .stButton > button {
        border-radius: 11px;
        border: 1px solid #e4e9ef;
        background: #ffffff;
        color: #344054;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #18b878;
        color: #129965;
        background: #f2fcf8;
    }

    .stChatMessage {
        background: #ffffff;
        border: 1px solid #e8ecf1;
        border-radius: 16px;
        margin-bottom: 10px;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# load saved sessions
def load_sessions():

    if os.path.exists("sessions.json"):

        try:

            with open(
                "sessions.json",
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except:

            return {}

    return {}


# save sessions
def save_sessions(sessions):

    with open(
        "sessions.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sessions,
            file,
            indent=4,
            ensure_ascii=False
        )


# create new session
def create_session():

    return {
        "title": "New Conversation",
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "messages": []
    }


# initialise Groq client
def setup_client(api_key):

    return Groq(
        api_key=api_key
    )


# audio to text
def transcribe_audio(client, audio_path):

    with open(
        audio_path,
        "rb"
    ) as audio_file:

        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            response_format="json"
        )

    return transcript.text


# llm response
def fetch_ai_response(client, messages):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content


# text to speech
def text_to_speech(client, text):

    text = text[:200]

    response = client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice="troy",
        input=text,
        response_format="wav"
    )

    return response.read()


# play audio
def play_audio(audio_bytes):

    audio_base64 = base64.b64encode(
        audio_bytes
    ).decode()

    audio_id = str(
        uuid.uuid4()
    )

    audio_html = f"""
    <audio
        id="{audio_id}"
        autoplay
        controls
        style="width:100%;"
    >
        <source
            src="data:audio/wav;base64,{audio_base64}"
            type="audio/wav"
        >
    </audio>

    <script>

        const audio = document.getElementById("{audio_id}");

        audio.load();

        audio.play().catch(function(error) {{
            console.log("Autoplay prevented:", error);
        }});

    </script>
    """

    st.components.v1.html(
        audio_html,
        height=60
    )


# initialise application state
def initialize_state():

    if "sessions" not in st.session_state:

        st.session_state.sessions = load_sessions()

    if "current_session" not in st.session_state:

        st.session_state.current_session = None


# create new conversation
def new_conversation():

    session_id = str(
        uuid.uuid4()
    )

    st.session_state.sessions[session_id] = create_session()

    st.session_state.current_session = session_id

    save_sessions(
        st.session_state.sessions
    )

    st.rerun()


# get current session
def get_current_session():

    session_id = st.session_state.current_session

    if session_id is None:

        return None

    return st.session_state.sessions.get(
        session_id
    )


# show sidebar
def show_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-logo">
                🎙️ Ultimate AI
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="sidebar-subtitle">
                Your personal voice assistant
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "＋  New conversation",
            use_container_width=True
        ):

            new_conversation()

        st.markdown(
            """
            <div class="conversation-label">
                CONVERSATIONS
            </div>
            """,
            unsafe_allow_html=True
        )

        sessions = st.session_state.sessions

        saved_sessions = [
            (session_id, session)
            for session_id, session in sessions.items()
            if len(
                session.get("messages", [])
            ) > 0
        ]

        saved_sessions.reverse()

        if not saved_sessions:

            st.markdown(
                """
                <div style="
                    color:#98a2b3;
                    font-size:13px;
                    padding:10px 2px;
                ">
                    No conversations yet.
                </div>
                """,
                unsafe_allow_html=True
            )

        for session_id, session in saved_sessions:

            title = session.get(
                "title",
                "Conversation"
            )

            if len(title) > 30:

                title = title[:30] + "..."

            if st.button(
                title,
                key=f"session_{session_id}",
                use_container_width=True
            ):

                st.session_state.current_session = session_id

                st.rerun()


# show messages
def show_messages(session):

    messages = session.get(
        "messages",
        []
    )

    for message in messages:

        if message["role"] == "user":

            with st.chat_message("user"):

                st.write(
                    message["content"]
                )

        elif message["role"] == "assistant":

            with st.chat_message("assistant"):

                st.write(
                    message["content"]
                )


# main
def main():

    initialize_state()

    show_sidebar()

    client = setup_client(
        API_KEY
    )

    session = get_current_session()

    # header
    st.markdown(
        """
        <h1 style="
            color:#17202a;
            font-size:38px;
            margin-bottom:4px;
        ">
            Ultimate AI Agent
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            color:#718096;
            font-size:16px;
            margin-bottom:18px;
        ">
            Talk naturally. Ask anything.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="status">
            <span class="status-dot"></span>
            AI Agent Online
        </div>
        """,
        unsafe_allow_html=True
    )

    # no conversation
    if session is None:

        st.markdown(
            "<div style='height:70px'></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:60px;
                margin-bottom:15px;
            ">
                🎙️
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h2 style="
                text-align:center;
                color:#17202a;
                font-size:27px;
            ">
                Start a conversation
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style="
                text-align:center;
                color:#8490a0;
                font-size:15px;
            ">
                Create a new conversation and start talking with your AI assistant.
            </p>
            """,
            unsafe_allow_html=True
        )

        return

    messages = session.get(
        "messages",
        []
    )

    # conversation
    if messages:

        show_messages(
            session
        )

    else:

        st.markdown(
            "<div style='height:45px'></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:55px;
                margin-bottom:10px;
            ">
                🎙️
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h2 style="
                text-align:center;
                color:#17202a;
                font-size:27px;
            ">
                What can I help you with?
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style="
                text-align:center;
                color:#8490a0;
                font-size:15px;
            ">
                Press the microphone below and start talking.
            </p>
            """,
            unsafe_allow_html=True
        )

    # microphone
    st.markdown(
        """
        <div class="recording-box">
        """,
        unsafe_allow_html=True
    )

    recorded_audio = audio_recorder()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # process recording
    if recorded_audio:

        audio_path = "recorded_audio.wav"

        with open(
            audio_path,
            "wb"
        ) as audio_file:

            audio_file.write(
                recorded_audio
            )

        with st.spinner(
            "Listening..."
        ):

            transcript = transcribe_audio(
                client,
                audio_path
            )

        if not transcript.strip():

            st.warning(
                "I couldn't understand the recording."
            )

            return

        session["messages"].append({
            "role": "user",
            "content": transcript
        })

        if len(
            session["messages"]
        ) == 1:

            session["title"] = transcript[:40]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI voice assistant. "
                    "Give clear, natural and concise answers. "
                    "Remember the conversation context."
                )
            }
        ]

        for message in session["messages"]:

            messages.append({
                "role": message["role"],
                "content": message["content"]
            })

        with st.spinner(
            "Thinking..."
        ):

            ai_response = fetch_ai_response(
                client,
                messages
            )

        session["messages"].append({
            "role": "assistant",
            "content": ai_response
        })

        save_sessions(
            st.session_state.sessions
        )

        with st.chat_message("user"):

            st.write(
                transcript
            )

        with st.chat_message("assistant"):

            st.write(
                ai_response
            )

        with st.spinner(
            "Speaking..."
        ):

            audio_response = text_to_speech(
                client,
                ai_response
            )

        play_audio(
            audio_response
        )


if __name__ == "__main__":

    main()