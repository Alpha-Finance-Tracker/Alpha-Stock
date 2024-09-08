from abc import ABC,abstractmethod


class Service(ABC):

    @abstractmethod
    async def service(self):
        raise NotImplementedError
