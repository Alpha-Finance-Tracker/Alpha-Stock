from app.data.database import read_query


def quarterly_overview(overview):
    info = read_query('SELECT * from company_overview WHERE Symbol = %s AND LatestQuarter = %s',
               (overview['Symbol'], overview['LatestQuarter']))
    if info:
        return info
    else:
        pass
        # co = await fetch_overview(symbol.lower())
