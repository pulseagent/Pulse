import json
from abc import ABC
from typing import Union


class MemoryObject:
    input: str
    output: Union[str, dict]

    def __init__(self, input: str = None, output: Union[str, dict] =None):
        self.input = input
        self.output = output

    def get_input(self) -> str:
        return self.input

    def get_output_to_string(self) -> str:
        if isinstance(self.output, str):
            return self.output
        else:
            return json.dumps(self.output, ensure_ascii=False)

class MemoryManager(ABC):
    memory_size: int = 10

    def __init__(self, memory_size: int = 10):
        self.memory_size = memory_size

    def get_memory_by_conversation_id(self, conversation_id: str) -> list[MemoryObject]:
        pass

    def save_memory(self, conversation_id: str, memory: MemoryObject):
        pass