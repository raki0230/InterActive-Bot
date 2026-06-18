import streamlit as st


def initialize_chat():

    if "messages" not in st.session_state:

        st.session_state.messages = []


def display_chat_history():

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and message.get("follow_up_questions")
            ):

                st.markdown(
                    "#### Suggested Follow-up Questions"
                )

                for question in message[
                    "follow_up_questions"
                ]:

                    st.markdown(
                        f"- {question}"
                    )


def add_user_message(content):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": content,
        }
    )


def add_assistant_message(
    content,
    message_id=None,
    follow_up_questions=None,
):

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": content,
            "message_id": message_id,
            "follow_up_questions":
                follow_up_questions or [],
        }
    )