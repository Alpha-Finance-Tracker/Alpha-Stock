from app.utilities.responses import AlphaVantageNoData, AlphaVantageAPIKey


class AlphaVantageValidator:

    def __init__(self,data):
        self.data = data

    async def validate(self):
        if len(self.data) == 0:
            raise AlphaVantageNoData()

        if 'Information' in self.data:
            raise AlphaVantageAPIKey()

