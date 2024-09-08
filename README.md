![Build Status](https://img.shields.io/github/actions/workflow/status/Alpha-Finance-Tracker/Alpha-Stock-Service/main.yml)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows-blue)
[![Coverage Status](https://coveralls.io/repos/github/Alpha-Finance-Tracker/Alpha-Stock-Service/badge.svg?branch=main)](https://coveralls.io/github/Alpha-Finance-Tracker/Alpha-Stock-Service?branch=main)



Alpha Stock API

This API is a part of a microservices based project, it provides a set of endpoints to calculate stock values, analyze company financial performance, and fetch related news and company information. 

The API utilizes token-based authentication (via the HTTPBearer mechanism) to secure the routes and integrates various services for stock prediction, intrinsic value calculation, and more.

The API is in continuous development. 

## Features
- Stock Valuation: Calculate intrinsic and fair value of stocks.
- Stock Prediction: Predict future stock prices.
- Company Financial Performance: Fetch and display key financial data for a company.
- Company Overview: Get general information and performance metrics about a company.
- Company News: Retrieve the latest news about a specific stock or company.
- Token Verification: Secures all routes through token-based authorization.


## Installation

To set up this FastAPI service, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Alpha-Finance-Tracker/Auth-Service.git

2. **Install the dependencies:**
   ```bash
     pip install -r requirements.txt

3. **Run the application:**
    ```bash
      uvicorn main:app --reload

Build with docker:
  ```bash
  docker build -t alpha_stock_app .
  
