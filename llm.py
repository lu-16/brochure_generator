import os
from dotenv import load_dotenv
from openai import AzureOpenAI


def get_secrets(key: str, default=None) -> str:
    try:
        import streamlit as st

        if key in st.secrets:
            return st.secrets[key]
    except ImportError:
        pass
    return os.getenv(key, default)


load_dotenv(override=True)
api_key = get_secrets("OPENAI_KEY")
endpoint = get_secrets("OPENAI_ENDPOINT")
model = get_secrets("OPENAI_MODEL")


class LLM:
    def __init__(self, api_key=api_key, endpoint=endpoint, model=model):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.client = self.get_client()

    def get_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self.api_key, api_version="2023-05-15", azure_endpoint=self.endpoint
        )
