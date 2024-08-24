from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI()

def fetch_competitors(symbol, sector):
    try:
        # Make a request to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the correct model name
            messages=[
                {"role": "user",
                 "content": f"Please provide a JSON list containing only the tickers of the top 20 competitors of {symbol} in the {sector} sector. No additional text or explanations, just the JSON list."}
            ]
        )

        # Extract and return the response content
        result = response.choices[0].message.content
        cleaned =  result.strip('```json\n').strip('\n```')
        parsed_data = json.loads(cleaned)
        return parsed_data


    except Exception as e:
        print(f"An error occurred: {e}")
        return None