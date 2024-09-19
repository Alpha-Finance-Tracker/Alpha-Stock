from abc import ABC,abstractmethod




class BasicMetricEvaluator(ABC):
    @abstractmethod
    def evaluate(self):
        raise NotImplementedError