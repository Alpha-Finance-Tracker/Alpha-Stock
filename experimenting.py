from app.database.database import custom_query
import asyncio
A =  asyncio.run(custom_query('SELECT * FROM company_overview',{},'SELECT'))

for x in range(10):
    print(A)