from app.models.base_models.service import Service
from app.models.calculators.valuation.fair_value_calculator import FairValue


class FairValueService(Service):

    def __init__(self,symbol):
        self.symbol = symbol

    async def service(self):
        return await FairValue(self.symbol).calculate()
