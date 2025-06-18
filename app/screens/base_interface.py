from abc import ABC, abstractmethod


class BaseInterface(ABC):
    @abstractmethod
    def create_components(self):
        pass

    @abstractmethod
    def display_components(self):
        pass

    @abstractmethod
    def handle_submit(self):
        pass

    @abstractmethod
    def interface_configuration(self, title, width, height):
        pass
