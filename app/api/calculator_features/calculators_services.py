from app.data.requests.stock_fetches import fetch_market_data_yf, fetch_cash_flow_yf, fetch_company_overview_av, \
    fetch_company_income_statement_av, fetch_company_balance_sheet_av, fetch_competitors_eps_yf
from app.api.stock_and_company_features.stock_and_company_queries import company_overview_db_update
from app.models.alpha_stock import AlphaStock





async def intrinsic_value_calculator(symbol):
    market_data = fetch_market_data_yf(symbol)
    cash_flows = fetch_cash_flow_yf(symbol)
    co = fetch_company_overview_av(symbol)
    income_statement = fetch_company_income_statement_av(symbol)
    balance_sheet = fetch_company_balance_sheet_av(symbol)
    competitors_pe_ratio = fetch_competitors_eps_yf(symbol,co['Sector'])

    try:
        AS = AlphaStock(symbol=symbol,
                        cash_flows=cash_flows, co=co, market_data=market_data,
                        income_statement=income_statement, balance_sheet=balance_sheet,competitors_pe_ratio=competitors_pe_ratio)

        company_overview_db_update(co, symbol)
        dcf_ps = AS.calculate_intrinsic_value_per_share
        relative_value = AS.calculate_relative_value_per_share

        return (dcf_ps + relative_value) // 2


    except Exception as e:
        return (f"Error with {e}")


def peter_lynch_value_calculator(egr, dy, pe_ratio):
    try:
        return (float(egr) + float(dy)) / float(pe_ratio)
    except Exception as e:
        return (f"There was a problem with the injected parameters {e}")

