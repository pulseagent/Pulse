from abc import ABC


class AbstractAgent(ABC):

    async def arun(self, query: str, conversation_id: str):
        raise NotImplementedError("arun is not implemented")