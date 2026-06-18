from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)


class ConversationMemory:

    def __init__(self):
        self.messages = []

    def add_user_message(
        self,
        content: str,
    ):
        self.messages.append(
            HumanMessage(content=content)
        )

    def add_ai_message(
        self,
        content: str,
    ):
        self.messages.append(
            AIMessage(content=content)
        )

    def get_messages(
        self,
        window_size: int = 20,
    ):
        return self.messages[-window_size:]

    def clear(self):
        self.messages = []