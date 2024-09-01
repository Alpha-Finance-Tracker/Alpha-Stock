import asyncio

from app.database import insert_query, read_query


async def send_parameters_towards_the_database(revenue, net_income, eps, roe,
                                               net_profit_margin, debt_level, cash_flows, symbol):
    await asyncio.gather(
        initiate_years(revenue, symbol),
        revenue_db_update(revenue, symbol),
        net_income_db_update(net_income, symbol),
        eps_db_update(eps, symbol),
        roe_db_update(roe, symbol),
        net_profit_margin_db_update(net_profit_margin, symbol),
        debt_level_db_update(debt_level, symbol),
        cash_flows_db_update(cash_flows, symbol), )


async def check_existing_years(symbol):
    existing_years = await read_query('SELECT year FROM company WHERE symbol = %s', (symbol,))

    if existing_years:
        return set(x[0] for x in existing_years)
    else:
        return {}


async def initiate_years(years, symbol):
    try:
        existing_years = check_existing_years(symbol)

        for x in years['fiscalDateEnding']:
            if x not in existing_years:
                await insert_query('INSERT INTO company(symbol, year) values (%s, %s)', (symbol, x))
    except Exception as e:
        print(f"Error with initiate_years: {e}")


async def eps_db_update(eps, symbol):
    for x, y in zip(eps['reportedEPS'], eps['fiscalDateEnding']):
        try:
            await insert_query('UPDATE company SET eps = %s WHERE year = %s AND symbol = %s', (float(x), y, symbol))
        except Exception as e:
            print(f"Error with eps_db_update: {e}")


async def revenue_db_update(revenue, symbol):
    for x, y in zip(revenue['growth_rate'], revenue['fiscalDateEnding']):
        try:
            await insert_query('UPDATE company SET revenue_growth = %s WHERE year = %s AND symbol = %s', (x, y, symbol))
        except Exception as e:
            print(f"Error with revenue_db_update: {e}")


async def net_income_db_update(net_income, symbol):
    for x, y in zip(net_income['netIncome'], net_income['fiscalDateEnding']):
        try:
            await insert_query('UPDATE company SET net_income = %s WHERE year = %s AND symbol = %s',
                               (int(x), y, symbol))
        except Exception as e:
            print(f"Error with net_income_db_update: {e}")


async def roe_db_update(roe, symbol):
    for x, y in zip(roe['roe'], roe['fiscalDateEnding']):
        try:
            await insert_query('UPDATE company SET roe = %s WHERE year = %s AND symbol = %s', (x, y, symbol))
        except Exception as e:
            print(f"Error with roe_db_update: {e}")


async def net_profit_margin_db_update(profit_margin, symbol):
    for x, y in zip(profit_margin['netProfitMargin'], profit_margin['fiscalDateEnding']):
        try:
            await insert_query('UPDATE company SET profit_margin = %s WHERE year = %s AND symbol = %s', (x, y, symbol))
        except Exception as e:
            print(f"Error with net_profit_margin_db_update: {e}")


async def debt_level_db_update(debt, symbol):
    for x, y in zip(debt['currentDebt'], debt['fiscalDateEnding']):
        try:
            await insert_query('UPDATE company SET debt_level = %s WHERE year = %s AND symbol = %s', (x, y, symbol))
        except Exception as e:
            print(f"Error with debt_level_db_update: {e}")


async def cash_flows_db_update(cash_flows, symbol):
    for x, y in zip(cash_flows['operatingCashflow'], cash_flows['fiscalDateEnding']):
        try:
            await insert_query('UPDATE company SET cash_flow = %s WHERE year = %s AND symbol = %s', (x, y, symbol))
        except Exception as e:
            print(f"Error with debt_level_db_update: {e}")


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
