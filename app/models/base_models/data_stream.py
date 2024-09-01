from abc import ABC, abstractmethod


class DataStream(ABC):
    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def unload(self):
        raise NotImplementedError
