import streamlit as st

from src.tracing.langsmith_setup import *
from src.services.qa_service import SmartQABot
from src.services.memory_service import ConversationMemory
from src.services.chat_history_service import ChatHistoryDB
from src.components.sidebar import render_sidebar
from src.components.chat import (
    initialize_chat,
    display_chat_history,
    add_user_message,
    add_assistant_message,
)
from src.components.metrics import render_metrics


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Q&A Bot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Smart Q&A Bot")
st.caption("Memory + SQLite + LangSmith")

# --------------------------------------------------
# Initialize Chat UI
# --------------------------------------------------

initialize_chat()

# --------------------------------------------------
# Database
# --------------------------------------------------

if "db" not in st.session_state:
    st.session_state.db = ChatHistoryDB()

# --------------------------------------------------
# Current Session
# --------------------------------------------------

if "current_session" not in st.session_state:

    sessions = st.session_state.db.get_sessions()

    if sessions:

        st.session_state.current_session = (
            sessions[0][0]
        )

    else:

        st.session_state.current_session = (
            st.session_state.db.create_session(
                "Untitled Chat"
            )
        )

# --------------------------------------------------
# Memory
# --------------------------------------------------

if "memory" not in st.session_state:
    st.session_state.memory = (
        ConversationMemory()
    )

if "last_message_id" not in st.session_state:
    st.session_state.last_message_id = None   

if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = {}     

# --------------------------------------------------
# Load Messages When Session Changes
# --------------------------------------------------

if (
    "loaded_session" not in st.session_state
    or
    st.session_state.loaded_session
    != st.session_state.current_session
):

    st.session_state.messages = []

    st.session_state.memory.clear()

    history = (
        st.session_state.db.get_session_messages(
            st.session_state.current_session
        )
    )

    for role, content in history:

        st.session_state.messages.append(
            {
                "role": role,
                "content": content,
                "follow_up_questions": [],
            }
        )

        if role == "user":

            st.session_state.memory.add_user_message(
                content
            )

        else:

            st.session_state.memory.add_ai_message(
                content
            )

    st.session_state.loaded_session = (
        st.session_state.current_session
    )

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

temperature, clear_chat = render_sidebar(
    st.session_state.db
)

# --------------------------------------------------
# Clear Current Chat
# --------------------------------------------------

if clear_chat:

    st.session_state.messages = []

    st.session_state.memory.clear()

    # Requires clear_session()
    st.session_state.db.clear_session(
        st.session_state.current_session
    )

    st.rerun()

# --------------------------------------------------
# Display Existing Messages
# --------------------------------------------------

display_chat_history()

# --------------------------------------------------
# Create / Update Bot
# --------------------------------------------------

if ("bot" not in st.session_state
    or "bot_temperature" not in st.session_state
    or st.session_state.bot_temperature != temperature):

    st.session_state.bot = SmartQABot(
        temperature=temperature
    )

    st.session_state.bot_temperature = temperature

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input(
    "Ask me anything..."
)

# --------------------------------------------------
# New User Message
# --------------------------------------------------

if prompt:

    add_user_message(prompt)

    # Auto rename untitled chat
    current_title = (
        st.session_state.db.get_session_title(
            st.session_state.current_session
        )
    )

    if current_title == "Untitled Chat":

        generated_title = (
            prompt[:30].strip()
        )

        st.session_state.db.update_session_title(
            st.session_state.current_session,
            generated_title,
        )

    st.session_state.memory.add_user_message(
        prompt
    )

    st.session_state.db.save_message(
        st.session_state.current_session,
        "user",
        prompt,
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ----------------------------------------------
    # Assistant Response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = (
                st.session_state.bot.ask(
                    question=prompt,
                    chat_history=(
                        st.session_state.memory.get_messages()
                    ),
                )
            )

        st.markdown(response.answer)

        # Save assistant message ONCE
        message_id = (
            st.session_state.db.save_message(
                st.session_state.current_session,
                "assistant",
                response.answer,
            )
        )



    # ----------------------------------------------
    # Update Memory + UI
    # ----------------------------------------------

    add_assistant_message(
        response.answer,
        message_id,
        response.follow_up_questions,
    )

    st.session_state.memory.add_ai_message(
        response.answer
    )

    st.session_state.last_message_id = (
        message_id
    )


# --------------------------------------------------
# Feedback Section
# --------------------------------------------------

if st.session_state.last_message_id:

    message_id = (
        st.session_state.last_message_id
    )

    if (
        message_id
        not in st.session_state.feedback_submitted
    ):

        feedback = st.radio(
            "Was the last response helpful?",
            options=[
                "👍 Helpful",
                "👎 Not Helpful",
            ],
            index=None,
            key=f"feedback_{message_id}",
        )

        if feedback:

            rating = (
                "positive"
                if feedback == "👍 Helpful"
                else "negative"
            )

            st.session_state.db.save_feedback(
                message_id,
                rating,
            )

            st.session_state.feedback_submitted[
                message_id
            ] = rating

            st.success(
                "Feedback saved!"
            )

            st.rerun()

    else:

        saved_rating = (
            st.session_state.feedback_submitted[
                message_id
            ]
        )

        st.info(
            f"Feedback submitted: {saved_rating}"
        )