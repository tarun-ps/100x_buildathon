from dotenv import load_dotenv
import os

load_dotenv("dev.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_O1_PREVIEW_MODEL = os.getenv("OPENAI_O1_PREVIEW_MODEL")
OPENAI_GPT4_O_MODEL = os.getenv("OPENAI_GPT4_O_MODEL")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL")
OPENAI_API_COMPLETION_URL = os.getenv("OPENAI_API_COMPLETION_URL")
PRELIMINARY_ANALYSE_SYSTEM_PROMPT = os.getenv("PRELIMINARY_ANALYSE_SYSTEM_PROMPT")
PRELIMINARY_ANALYSE_USER_PROMPT = os.getenv("PRELIMINARY_ANALYSE_USER_PROMPT")
GENERATE_QUESTIONS_SYSTEM_PROMPT = os.getenv("GENERATE_QUESTIONS_SYSTEM_PROMPT")
GENERATE_QUESTIONS_USER_PROMPT = os.getenv("GENERATE_QUESTIONS_USER_PROMPT")
PICK_GRAPH_TYPE_SYSTEM_PROMPT = os.getenv("PICK_GRAPH_TYPE_SYSTEM_PROMPT")
PICK_GRAPH_TYPE_USER_PROMPT = os.getenv("PICK_GRAPH_TYPE_USER_PROMPT")
GENERATE_CODE_SYSTEM_PROMPT = os.getenv("GENERATE_CODE_SYSTEM_PROMPT")
GENERATE_CODE_USER_PROMPT = os.getenv("GENERATE_CODE_USER_PROMPT")