import os

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI


load_dotenv()


class MistralModel:

    def __init__(self):

        api_key = os.getenv(
            "MISTRAL_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "MISTRAL_API_KEY not found. "
                "Add it to your .env file."
            )

        self.model = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0
        )

    def generate(self, prompt):

        response = self.model.invoke(
            prompt
        )

        return response.content