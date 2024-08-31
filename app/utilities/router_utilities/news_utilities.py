from app.models.data_stream.alpha_vantage_data import AlphaVantage
async def alpha_vantage_news(symbol:str):
    try:
        data = await AlphaVantage(symbol).news()

        times = [(x[0:4] + " " + x[4:6] + "." + x[6:8]) for x in data['time_published']]
        news = {'Title':data['title'],
                'Url':data['url'],
                'Time':times,
                'Image':data['banner_image']}

        return news
    except Exception as e:
        return f'Error with parsing data from AV, probably fetch limit related {e}'
