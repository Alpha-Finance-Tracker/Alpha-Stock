from abc import ABC, abstractmethod


class StockCalculator(ABC):
    @abstractmethod
    def calculate(self,**kwargs):
        raise NotImplementedError
