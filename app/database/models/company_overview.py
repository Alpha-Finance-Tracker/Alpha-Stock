from sqlalchemy import Column, Integer, String, Date, Numeric, select
from app.database.database import Base, get_db


class CompanyOverview(Base):
    __tablename__ = 'company_overview'

    quarter_symbol_id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    asset_type = Column(String(50), default=None)
    quarter = Column(Date, default=None)
    market_capitalization = Column(Numeric(20, 3), default=None)
    ebitda = Column(Numeric(20, 3), default=None)
    pe_ratio = Column(Numeric(20, 3), default=None)
    peg_ratio = Column(Numeric(20, 3), default=None)
    book_value = Column(Numeric(20, 3), default=None)
    dividend_per_share = Column(Numeric(20, 3), default=None)
    dividend_yield = Column(Numeric(20, 3), default=None)
    eps = Column(Numeric(20, 3), default=None)
    revenue_per_share = Column(Numeric(20, 3), default=None)
    profit_margin = Column(Numeric(20, 3), default=None)
    operating_margin = Column(Numeric(20, 3), default=None)
    return_on_asset = Column(Numeric(20, 3), default=None)
    return_on_equity = Column(Numeric(20, 3), default=None)
    revenue = Column(Numeric(20, 3), default=None)
    gross_profit = Column(Numeric(20, 3), default=None)
    diluted_eps = Column(Numeric(20, 3), default=None)
    quarterly_earnings_growth = Column(Numeric(20, 3), default=None)
    quarterly_revenue_growth = Column(Numeric(20, 3), default=None)
    analyst_target_price = Column(Numeric(20, 3), default=None)
    analyst_rating_strong_buy = Column(Numeric(20, 3), default=None)
    analyst_rating_buy = Column(Numeric(20, 3), default=None)
    analyst_rating_hold = Column(Numeric(20, 3), default=None)
    analyst_rating_sell = Column(Numeric(20, 3), default=None)
    analyst_rating_strong_sell = Column(Numeric(20, 3), default=None)
    trailing_pe = Column(Numeric(20, 3), default=None)
    forward_pe = Column(Numeric(20, 3), default=None)
    price_to_sales_ratio = Column(Numeric(20, 3), default=None)
    price_to_book_ratio = Column(Numeric(20, 3), default=None)
    ev_to_revenue = Column(Numeric(20, 3), default=None)
    ev_to_ebitda = Column(Numeric(20, 3), default=None)
    beta = Column(Numeric(20, 3), default=None)
    Year52WeekHigh = Column(Numeric(20, 3), default=None)
    Year52WeekLow = Column(Numeric(20, 3), default=None)
    MovingAverage50Day = Column(Numeric(20, 3), default=None)
    MovingAverage200Day = Column(Numeric(20, 3), default=None)
    shares_outstanding = Column(Numeric(20, 3), default=None)

    @classmethod
    async def view(cls,symbol):
        async with get_db() as db:
            stmt = select(CompanyOverview).filter(CompanyOverview.Symbol == symbol)
            result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def add(cls,information):

        async with get_db as db:
            db.add(information)
            db.commit()
