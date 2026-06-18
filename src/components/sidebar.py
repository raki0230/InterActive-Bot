import streamlit as st


def render_sidebar(db):

    with st.sidebar:

        st.title("Chats")

        # -----------------------------
        # New Chat Button
        # -----------------------------
        if st.button(
            "➕ New Chat",
            use_container_width=True
        ):

            session_id = db.create_session(
                "Untitled Chat"
            )

            st.session_state.current_session = (
                session_id
            )

            st.session_state.messages = []

            if "memory" in st.session_state:
                st.session_state.memory.clear()

            # Clear feedback state
            st.session_state.last_message_id = None
            st.session_state.feedback_submitted = {}

            st.rerun()

        st.divider()

        # -----------------------------
        # Existing Chats
        # -----------------------------
        sessions = db.get_sessions()

        for session_id, title in sessions:

            col1, col2 = st.columns([5, 1])

            # Chat Button
            with col1:

                if st.button(
                    title,
                    key=f"session_{session_id}",
                    use_container_width=True,
                ):

                    st.session_state.current_session = (
                        session_id
                    )

                    # Reset feedback state
                    st.session_state.last_message_id = None
                    st.session_state.feedback_submitted = {}

                    st.rerun()

            # Delete Button
            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{session_id}",
                    help="Delete Chat"
                ):

                    db.delete_session(
                        session_id
                    )

                    # Deleted active session
                    if (
                        st.session_state.current_session
                        == session_id
                    ):

                        remaining_sessions = (
                            db.get_sessions()
                        )

                        if remaining_sessions:

                            st.session_state.current_session = (
                                remaining_sessions[0][0]
                            )

                        else:

                            new_session = (
                                db.create_session(
                                    "Untitled Chat"
                                )
                            )

                            st.session_state.current_session = (
                                new_session
                            )

                        st.session_state.messages = []

                        if "memory" in st.session_state:
                            st.session_state.memory.clear()

                        # Reset feedback state
                        st.session_state.last_message_id = None
                        st.session_state.feedback_submitted = {}

                    st.rerun()

        st.divider()

        # -----------------------------
        # Settings
        # -----------------------------
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
        )

        clear_chat = st.button(
            "🗑️ Clear Current Chat",
            use_container_width=True,
        )

        return (
            temperature,
            clear_chat,
        )