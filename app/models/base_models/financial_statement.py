from abc import ABC, abstractmethod


class FinancialStatement(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError

