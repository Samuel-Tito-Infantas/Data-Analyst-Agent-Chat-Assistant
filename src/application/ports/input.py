from abc import ABC, abstractmethod
from typing import List

class ChatUseCase(ABC):
    @abstractmethod
    def start_conversation(self, question:str):
        pass


class ChargeTextDataBase(ABC):
    @abstractmethod
    def insert_text_database(self, texts:List[str]):
        pass