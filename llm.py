import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(override=True)
api_key = os.getenv("OPENAI_KEY")
endpoint = os.getenv("OPENAI_ENDPOINT")
model = os.getenv("OPENAI_MODEL")


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
