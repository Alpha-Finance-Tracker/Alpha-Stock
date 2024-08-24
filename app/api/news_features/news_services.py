from app.data.requests.news_fetches import fetch_news_from_alpha_vantage


def alpha_vantage_news(symbol:str):
    try:
        data = fetch_news_from_alpha_vantage(symbol)
        times = [(x[0:4] + " " + x[4:6] + "." + x[6:8]) for x in data['time_published']]
        news = {'Title':data['title'],
                'Url':data['url'],
                'Time':times,
                'Image':data['banner_image']}

        return news
    except Exception as e:
        return f'Error with parsing data from AV, probably fetch limit related {e}'
