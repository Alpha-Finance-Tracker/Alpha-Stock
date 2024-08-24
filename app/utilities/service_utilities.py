from pydantic import Field
from app.data.database import read_query
from app.utilities.responses import EmailExists, Unauthorized
import matplotlib.pyplot as plt
import numpy as np
import io


def get_user_by_id(user_id: int = Field(gt=0)):
    result = read_query("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return result


def check_existence(email):
    info = read_query('SELECT * FROM users WHERE email = %s',(email,))
    if info:
        raise EmailExists

def stop_if_guest(user):
    if user is None:
        raise Unauthorized

def display_charts(data):
    # Extract the data from the input
    years = [x[1] for x in data]
    revenue = [float(x[2]) for x in data]
    net_income = [float(x[3]) for x in data]
    cash_flow = [float(x[4]) for x in data]
    debt_level = [float(x[5]) for x in data]
    eps = [float(x[6]) for x in data]
    roe = [float(x[7]) for x in data]

    # Create a figure and a set of subplots
    fig, axs = plt.subplots(3, 2, figsize=(14, 10), facecolor='none')

    # Plot data on each subplot
    axs[0, 0].plot(years, revenue, 'b-o')
    axs[0, 0].set_title('Revenue')
    axs[0, 0].set_xlabel('Year')
    axs[0, 0].set_ylabel('Revenue $')

    axs[0, 1].plot(years, net_income, 'r-o')
    axs[0, 1].set_title('Net Income')
    axs[0, 1].set_xlabel('Year')
    axs[0, 1].set_ylabel('Net Income $')

    axs[1, 0].plot(years, cash_flow, 'g-o')
    axs[1, 0].set_title('Cash Flow')
    axs[1, 0].set_xlabel('Year')
    axs[1, 0].set_ylabel('Cash Flow $')

    axs[1, 1].plot(years, debt_level, 'y-o')
    axs[1, 1].set_title('Debt Level')
    axs[1, 1].set_xlabel('Year')
    axs[1, 1].set_ylabel('Debt Level $')

    axs[2, 0].plot(years, eps, 'm-o')
    axs[2, 0].set_title('Earnings Per Share (EPS)')
    axs[2, 0].set_xlabel('Year')
    axs[2, 0].set_ylabel('EPS ($)')

    axs[2, 1].plot(years, roe, 'c-o')
    axs[2, 1].set_title('Return on Equity (ROE)')
    axs[2, 1].set_xlabel('Year')
    axs[2, 1].set_ylabel('ROE (%)')

    # Add some space between the subplots
    plt.tight_layout()

    # Save the figure to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', transparent=True)
    img.seek(0)

    return img
