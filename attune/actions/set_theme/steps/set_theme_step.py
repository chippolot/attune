from abc import ABC, abstractmethod


class SetThemeStep(ABC):
    @abstractmethod
    def run(self, theme_name):
        pass
