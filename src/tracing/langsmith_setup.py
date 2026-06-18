import os

from src.config.settings import (
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
)

if LANGSMITH_API_KEY:

    os.environ["LANGSMITH_TRACING"] = "true"

    os.environ["LANGSMITH_API_KEY"] = (
        LANGSMITH_API_KEY
    )

    os.environ["LANGSMITH_PROJECT"] = (
        LANGSMITH_PROJECT
    )