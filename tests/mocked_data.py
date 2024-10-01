import pandas as pd
data = {
    'Date': ['2023-09-30', '2022-09-30', '2021-09-30', '2020-09-30'],
    'Gross Profit': [1.691480e+11, 1.707820e+11, 1.528360e+11, 1.049560e+11],
    'Total Revenue': [3.832850e+11, 3.943280e+11, 3.658170e+11, 2.745150e+11],
    'Net Incomes': [9.939700e+10, 9.946500e+10, 9.942000e+10, 5.742200e+10],
    'Operating Incomes': [1.217980e+11, 1.210040e+11, 1.083810e+11, 6.623800e+10],
    'Tax Rates': [0.158, 0.162, 0.135, 0.143],
    'Net Income Common Stockholders': [9.694000e+10, 9.923900e+10, 9.948000e+10, 5.749800e+10],
    'Total Assets': [3.750000e+12, 3.738000e+12, 3.575000e+12, 3.243000e+12],
    'Stockholders Equity': [1.280000e+12, 1.300000e+12, 1.206000e+12, 1.012000e+12],
    'NOPAT': [1.018000e+11, 1.007000e+11, 8.891000e+10, 5.624000e+10],
    'Invested Capital': [1.600000e+12, 1.620000e+12, 1.540000e+12, 1.310000e+12],
    'Total Debt': [4.800000e+11, 4.900000e+11, 4.250000e+11, 3.450000e+11],
    'Cash and Cash Equivalents': [1.100000e+11, 1.300000e+11, 1.200000e+11, 9.800000e+10],
    'Current Liabilities': [1.300000e+11, 1.200000e+11, 1.100000e+11, 9.000000e+10],
    'EBIT': [1.458000e+11, 1.450000e+11, 1.250000e+11, 7.900000e+10],
    'Interest Expense': [3.210000e+10, 3.200000e+10, 2.850000e+10, 2.400000e+10],
    'Current Assets': [1.500000e+11, 1.600000e+11, 1.400000e+11, 1.200000e+11],
    'EBITDA': [1.800000e+11, 1.790000e+11, 1.600000e+11, 9.800000e+10],
    'Income Before Tax': [1.300000e+11, 1.290000e+11, 1.150000e+11, 7.200000e+10],
    'Income After Tax': [1.095000e+11, 1.082000e+11, 9.855000e+10, 6.169000e+10],
    'Invalid':[None,[],None,None],
    'Zeroes':[0,0,0,0]
}

mock_df = pd.DataFrame(data)

valid_mock_access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwiZW1haWwiOiJUZXN0QGdtYWlsLmNvbSIsInJvbGUiOiJ1c2VyIiwiZXhwIjo0ODgxMTI0NjY1fQ.pyN38WUX_zguzaAyeivC0YLv7Rsxz-nDaVdFCeEnG2w'
valid_mock_refresh_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwiZXhwIjo0ODgxMTI0NjY1fQ.EPcUZfakItrjDfHtbrnIX2d9BSLnJPSvx-Pv7U4ODkI'
invalid_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'


