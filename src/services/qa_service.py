from typing import List

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_openai import ChatOpenAI

from langsmith import traceable

from src.models.qa_response import (
    QAResponse,
)


class SmartQABot:

    def __init__(
        self,
        model_name="gpt-4o-mini",
        temperature=0.3,
    ):

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
        ).with_structured_output(
            QAResponse
        )

        self.streaming_llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            streaming=True,
        )

        self.prompt = (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are a knowledgeable Q&A assistant.

Rules:
- Answer accurately
- Explain reasoning
- Suggest follow-up questions
- Mention uncertainty
- Mention if sources are needed
                        """,
                    ),
                    MessagesPlaceholder(
                        variable_name="chat_history"
                    ),
                    (
                        "human",
                        "{question}",
                    ),
                ]
            )
        )

        self.chain = (
            self.prompt
            | self.llm
        )

    @traceable(
        name="ask_question",
        run_type="chain",
    )
    def ask(self, question: str, chat_history: List,):

        try:

            response = self.chain.invoke(
                {
                    "question": question,
                    "chat_history": chat_history,
                }
            )

            return response

        except Exception as e:

            return QAResponse(
                answer="Something went wrong.",
                confidence="low",
                reasoning=str(e),
                follow_up_questions=[],
                sources_needed=True,
            )
        
    def stream_answer(self, question: str, chat_history: List,):

        messages = (
            self.prompt.format_messages(
                question=question,
                chat_history=chat_history,
            )
        )

        for chunk in self.streaming_llm.stream(
            messages
        ):

            if chunk.content:
                yield chunk.content    