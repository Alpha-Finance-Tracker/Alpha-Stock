from sqlalchemy import Column, Integer, String, select, Numeric
from app.database.database import Base, get_db


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(45), nullable=False)
    year = Column(Integer, nullable=False)
    revenue_growth = Column(Numeric(20, 3), nullable=False)  # % based
    net_income = Column(Numeric(20, 3), nullable=False)
    cash_flow = Column(Numeric(20, 3), nullable=False)
    debt_level = Column(Numeric(20, 3), nullable=False)
    eps = Column(Numeric(20, 3), nullable=False)
    roe = Column(Numeric(20, 3), nullable=False)

    @classmethod
    async def view(cls, symbol):
        async with get_db() as db:
            stmt = select(Company).filter(Company.symbol == symbol)
            result = await db.execute(stmt)
        return result.scalars().all()
