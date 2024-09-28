from app.utilities.responses import AlphaVantageNoData, AlphaVantageAPIKey


class AlphaVantageValidator:

    def __init__(self,data):
        self.data = data

    def validate(self):
        print('Validator was used')
        if len(self.data) == 0:
            raise AlphaVantageNoData()

        if 'Information' in self.data:
            raise AlphaVantageAPIKey()

