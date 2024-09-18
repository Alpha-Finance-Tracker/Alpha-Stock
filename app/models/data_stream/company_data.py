import asyncio

from app.database.database import custom_query
from app.database.models.company_overview import CompanyOverview


async def send_parameters_towards_the_database(revenue_growth, net_income, eps, roe,
                                               net_profit_margin, debt_level, cash_flow, symbol):
    await asyncio.gather(
        initiate_years(revenue_growth, symbol),
        update_company('revenue_growth', revenue_growth['growth_rate'], revenue_growth['fiscalDateEnding'], symbol),
        update_company('net_income', net_income['netIncome'], net_income['fiscalDateEnding'], symbol),
        update_company('eps', eps['reportedEPS'], eps['fiscalDateEnding'], symbol),
        update_company('roe', roe['roe'], roe['fiscalDateEnding'], symbol),
        update_company('debt_level', debt_level['currentDebt'], debt_level['fiscalDateEnding'], symbol),
        update_company('cash_flow', cash_flow['operatingCashflow'], cash_flow['fiscalDateEnding'], symbol))


async def check_existing_years(symbol):
    existing_years = await read_query('SELECT year FROM company WHERE symbol = %s', (symbol,))

    if existing_years:
        return set(x[0] for x in existing_years)
    else:
        return {}


async def update_company(column, mark, years, symbol):
    for x, y in zip(mark, years):
        try:
            await insert_query(f"""
            UPDATE company SET {column} = %s WHERE year = %s AND symbol = %s""", (float(x), y, symbol))
        except Exception as e:
            print(e)


#
async def initiate_years(years, symbol):
    try:
        existing_years = await check_existing_years(symbol)

        for x in years['fiscalDateEnding']:
            if x not in existing_years:
                await insert_query('INSERT INTO company(symbol, year) values (%s, %s)', (symbol, x))
    except Exception as e:
        print(f"Error with initiate_years: {e}")


async def company_overview_db_update(company_overview, symbol):
    # Q1: October 1 - December 31
    # Q2: January 1 - March 31
    # Q3: April 1 - June 30
    # Q4: July 1 - September 30

    check_existence = await custom_query('SELECT symbol FROM company_overview WHERE symbol = %s AND quarter = %s',
                                       (symbol, company_overview['LatestQuarter']),'SELECT')

    if check_existence == []:
        information = await CompanyOverview(
            symbol=company_overview['Symbol'],
            asset_type=company_overview['AssetType'],
            quarter=company_overview['LatestQuarter'],
            market_capitalization=company_overview['MarketCapitalization'],
            ebitda=company_overview['EBITDA'],
            pe_ratio = company_overview['PERatio'],
            peg_ratio=company_overview['PEGRatio'],
            book_value=company_overview['BookValue'],
            dividend_per_share=company_overview['DividendPerShare'],
            dividend_yield=company_overview['DividendYield'],
            eps=company_overview['EPS'],
            revenue_per_share=company_overview['RevenuePerShareTTM'],
            profit_margin=company_overview['ProfitMargin'],
            operating_margin=company_overview['OperatingMarginTTM'],
            return_on_asset=company_overview['ReturnOnAssetsTTM'],
            return_on_equity=company_overview['ReturnOnEquityTTM'],
            revenue=company_overview['RevenueTTM'],
            gross_profit=company_overview['GrossProfitTTM'],
            diluted_eps=company_overview['DilutedEPSTTM'],
            quarterly_earnings_growth=company_overview['QuarterlyEarningsGrowthYOY'],
            quarterly_revenue_growth=company_overview['QuarterlyRevenueGrowthYOY'],
            analyst_target_price=company_overview['AnalystTargetPrice'],
            analyst_rating_strong_buy=company_overview['AnalystRatingStrongBuy'],
            analyst_rating_buy=company_overview['AnalystRatingBuy'],
            analyst_rating_hold=company_overview['AnalystRatingHold'],
            analyst_rating_sell=company_overview['AnalystRatingSell'],
            analyst_rating_strong_sell=company_overview['AnalystRatingStrongSell'],
            trailing_pe=company_overview['TrailingPE'],
            forward_pe=company_overview['ForwardPE'],
            price_to_sales_ratio=company_overview['PriceToSalesRatioTTM'],
            price_to_book_ratio=company_overview['PriceToBookRatio'],
            ev_to_revenue=company_overview['EVToRevenue'],
            ev_to_ebitda=company_overview['EVToEBITDA'],
            beta=company_overview['Beta'],
            Year52WeekHigh=company_overview['52WeekHigh'],
            Year52WeekLow=company_overview['52WeekLow'],
            MovingAverage50Day=company_overview['50DayMovingAverage'],
            MovingAverage200Day=company_overview['200DayMovingAverage'],
            shares_outstanding=company_overview['SharesOutstanding'])

        await CompanyOverview().add(information)
        return "success"


