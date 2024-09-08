from abc import ABC, abstractmethod


class FinancialStatement(ABC):
    @abstractmethod
    def info(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError
