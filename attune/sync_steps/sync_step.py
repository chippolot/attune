from abc import ABC, abstractmethod


class SyncStep(ABC):
    @abstractmethod
    def run(self):
        pass
