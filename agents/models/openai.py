import os

from langchain_community.chat_models.openai import ChatOpenAI

from agents.models.model import Model


class ChatGPT(Model):
    """Chat GPT model"""
    use_model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4",)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_model(self):
        return self.use_model



openai = ChatGPT()