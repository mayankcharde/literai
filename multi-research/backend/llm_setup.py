from langchain_mistralai import ChatMistralAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_mistral_llm(temperature: float = 0.7, model: str = "mistral-small-latest"):
    """Initialize Mistral LLM"""
    return ChatMistralAI(
        model=model,
        temperature=temperature,
        api_key=os.getenv("MISTRAL_API_KEY"),
        max_retries=2
    )