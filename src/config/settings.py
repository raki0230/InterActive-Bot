from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "Smart Q&A Bot Project",
)