from abc import ABC, abstractmethod


class StockCalculator(ABC):
    @abstractmethod
    def calculate(self):
        raise NotImplementedError
