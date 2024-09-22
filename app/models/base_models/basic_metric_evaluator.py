from abc import ABC, abstractmethod


class BasicMetricEvaluator(ABC):
    @abstractmethod
    def evaluate(self,**kwargs):
        raise NotImplementedError
