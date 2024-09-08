import asyncio

from app.database import insert_query, read_query


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

    check_existence = await read_query('SELECT symbol FROM company_overview WHERE symbol = %s AND quarter = %s',
                                       (symbol, company_overview['LatestQuarter']))

    if check_existence == []:
        await insert_query("""INSERT INTO company_overview (
                        Symbol, asset_type, quarter, market_capitalization, ebitda, 
                        pe_ratio, peg_ratio, book_value, dividend_per_share, dividend_yield, 
                        eps, revenue_per_share, profit_margin, operating_margin, 
                        return_on_asset, return_on_equity, revenue, gross_profit, 
                        diluted_eps, quarterly_earnings_growth, quarterly_revenue_growth, 
                        analyst_target_price, analyst_rating_strong_buy, analyst_rating_buy, 
                        analyst_rating_hold, analyst_rating_sell, analyst_rating_strong_sell, 
                        trailing_pe, forward_pe, price_to_sales_ratio, price_to_book_ratio, 
                        ev_to_revenue, ev_to_ebitda, beta, Year52WeekHigh, Year52WeekLow, 
                        MovingAverage50Day, MovingAverage200Day, shares_outstanding
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s
                    )""",

                           (company_overview['Symbol'], company_overview['AssetType'],
                            company_overview['LatestQuarter'], company_overview['MarketCapitalization'],
                            company_overview['EBITDA'], company_overview['PERatio'],
                            company_overview['PEGRatio'], company_overview['BookValue'],
                            company_overview['DividendPerShare'], company_overview['DividendYield'],
                            company_overview['EPS'], company_overview['RevenuePerShareTTM'],
                            company_overview['ProfitMargin'], company_overview['OperatingMarginTTM'],
                            company_overview['ReturnOnAssetsTTM'], company_overview['ReturnOnEquityTTM'],
                            company_overview['RevenueTTM'], company_overview['GrossProfitTTM'],
                            company_overview['DilutedEPSTTM'], company_overview['QuarterlyEarningsGrowthYOY'],
                            company_overview['QuarterlyRevenueGrowthYOY'], company_overview['AnalystTargetPrice'],
                            company_overview['AnalystRatingStrongBuy'], company_overview['AnalystRatingBuy'],
                            company_overview['AnalystRatingHold'], company_overview['AnalystRatingSell'],
                            company_overview['AnalystRatingStrongSell'], company_overview['TrailingPE'],
                            company_overview['ForwardPE'], company_overview['PriceToSalesRatioTTM'],
                            company_overview['PriceToBookRatio'], company_overview['EVToRevenue'],
                            company_overview['EVToEBITDA'], company_overview['Beta'], company_overview['52WeekHigh'],
                            company_overview['52WeekLow'], company_overview['50DayMovingAverage'],
                            company_overview['200DayMovingAverage'],
                            company_overview['SharesOutstanding']))

    return "success"
