from dotenv import load_dotenv
from openai import OpenAI
import json

from app.models.data_stream.yahoo_finance_data import YahooFinance

load_dotenv()
client = OpenAI()


class OpenAIData:

    def __init__(self, symbol):
        self.symbol = symbol

    async def competitors_price_to_earnings_ratio(self, sector):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user",
                     "content": f"Please provide a JSON list containing only the tickers of the top 20 competitors of {self.symbol} in the {sector} sector. No additional text or explanations, just the JSON list."}
                ]
            )

            # Extract and return the response content
            result = response.choices[0].message.content
            cleaned = result.strip('```json\n').strip('\n```')
            competitors_list = json.loads(cleaned)

            competitors_pe_ratio = []
            for company in competitors_list:
                try:
                    pe_ratio = YahooFinance(company).info['forwardPE']
                    if pe_ratio:
                        competitors_pe_ratio.append(pe_ratio)

                except Exception as e:
                    print(e)

            return competitors_pe_ratio

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
