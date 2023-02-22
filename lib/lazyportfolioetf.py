import requests
import pandas as pd
from bs4 import BeautifulSoup
from os import path
from datetime import datetime, timedelta
from typing import List, Dict

def calculate_monthly_inflation_rate(row : str) -> float:
    """
    Calculate an average monthly inflation rate based on the yearly inflation rate

    Using the difference between total return and inflation adjusted return this function will take an average
    and use it for approximating the monthly inflation rate for the current year.

    Parameters:
    row (List[str]): List of string values from the row in the HTML table for the current year

    Returns:
    float: Normalized float value representing the effect inflation will have on the monthly price change
    """

    yearly_inflation_adjusted_return = convert_yearly_return_to_numeric(row[2].text)
    yearly_total_return = convert_yearly_return_to_numeric(row[1].text)
    yearly_inflation_rate = yearly_total_return - yearly_inflation_adjusted_return

    average_monthly_inflation_rate = yearly_inflation_rate/12

    return float(average_monthly_inflation_rate)

def convert_yearly_return_to_numeric(percentage_gain_str : str) -> float:
    """
    Convert string to float

    Converts a string represantation of a percentage gain to an normalized float value

    Parameters:
    percentage_gain_str (str): Percentage gain for example: +5.09, -3.21, 0.0

    Returns:
    float: Normalized float value representing percentage gain, for example: 1.0509, 0.9679, 1.0
    """
    
    #Check if it is a positive return
    if '-' in percentage_gain_str:
        percentage_gain_str = percentage_gain_str.replace('-', '')
        percentage_gain_numeric = float(percentage_gain_str)
        percentage_gain_numeric = (100 - percentage_gain_numeric)/100

    elif '+' in percentage_gain_str:
        percentage_gain_str = percentage_gain_str.replace('+', '')
        percentage_gain_numeric = float(percentage_gain_str)
        percentage_gain_numeric = (100 + percentage_gain_numeric)/100

    elif percentage_gain_str.strip() == '' or percentage_gain_str is None:
        return None

    else:
        percentage_gain_str = percentage_gain_str.replace('+', '')
        percentage_gain_numeric = float(percentage_gain_str)
        percentage_gain_numeric = (100 + percentage_gain_numeric)/100
    
    return percentage_gain_numeric

def parse_monthly_results(soup) -> List[Dict]:
    result = []

    html_table = soup.find('table', id='yearReturns')
    html_table_tbody = html_table.find('tbody')
    html_table_tbody_rows = html_table_tbody.findAll('tr')
    
    for row in html_table_tbody_rows:

        #Get the row data
        average_monthly_inflation_rate = calculate_monthly_inflation_rate(row.find_all('td'))

        for index, column in enumerate(row.find_all('td')):
            if index < 3:
                continue
            elif index >= 3 and index <= 14:
                current_date = datetime(int(row.find('td').text), index - 2, 1)
                return_total = convert_yearly_return_to_numeric(column.text)
                return_inflation_adjusted = convert_yearly_return_to_numeric(column.text)

                #Adjust the monthly return for the inflation rate
                if return_inflation_adjusted is not None:
                    return_inflation_adjusted = return_inflation_adjusted - average_monthly_inflation_rate
                
                result.append({'date': current_date, 'inflation_adjusted': return_inflation_adjusted, 'total': return_total})
        
    #Example return value:
    # [{"date": 1871-01-01, "inflation_adjusted": 8.61, "total": 10.11}, {"date": 1872-02-01, "inflation_adjusted": 2.34, "total": -1.34}...]
    
    return result


def parse_yearly_results(soup) -> List[Dict]:
    """
    Parse annual result

    Parse the annual result from Lazy Portfolio ETFs webpage for a portfolio

    Parameters:
    soup (BeautifulSoup): BeautifulSoup object containing HTML source

    Returns:
    List[Dict]: A list of Dicts where each Dict contains result for each year
    """
    result = []

    html_table = soup.find('table', id='yearReturns')
    html_table_tbody = html_table.find('tbody')
    html_table_tbody_rows = html_table_tbody.findAll('tr')
    
    for row in html_table_tbody_rows:
        current_year = datetime(int(row.find('td').text), 1, 1)
        total = convert_yearly_return_to_numeric(row.find_all('td')[1].text)
        inflation_adjusted = convert_yearly_return_to_numeric(row.find_all('td')[2].text)
        result.append({'date': current_year, 'inflation_adjusted': inflation_adjusted, 'total': total})
        
    #Example return value:
    # [{"date": 1871-01-01, "inflation_adjusted": 8.61, "total": 10.11}, {"date": 1872-02-01, "inflation_adjusted": 2.34, "total": -1.34}...]
    
    return result

def fetch_portfolio_results(portfolio_name : str, granularity : str) -> pd.DataFrame:
    """
    Fetch portfolio result from Lazy Portfolio ETF website

    Parameters:
    portfolio_name (str): Name of the portfolio
    granularity (str): What granularity to use. 'y' for annual and 'm' for monthly.

    Returns:
    DataFrame: Pandas DataFrame with columns 'date', 'return_inflation_adjusted' and 'return_total'
    """
    base_url = "http://www.lazyportfolioetf.com/allocation"
    url = f"{base_url}/{portfolio_name}/"

    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    if(granularity == 'y'):
        df = pd.DataFrame(parse_yearly_results(soup))
        df['date'] = pd.DatetimeIndex(df['date'])
    elif(granularity == 'm'):
        df = pd.DataFrame(parse_monthly_results(soup))
        df['date'] = pd.DatetimeIndex(df['date'])

    df = df.sort_values(by=['date'], ascending=True)

    df['return_inflation_adjusted'] = df['inflation_adjusted'].shift(1)
    df['return_total'] = df['total'].shift(1)

    df = df[['date', 'return_inflation_adjusted', 'return_total']]

    return df

def get_portfolio_results(portfolio_name : str, granularity = 'y') -> pd.DataFrame:
    """
    Get portfolio results

    Parameters:
    portfolio_name (str): Name of the portfolio
    granularity (str): What granularity to use. 'y' for annual and 'm' for monthly.

    Returns:
    DataFrame: Pandas DataFrame with columns 'year', 'inflation_adjusted' and 'total'
    """

    #print(f"Data for portfolio {portfolio_name} with granularity {granularity} does not exist locally...Will fetch it from lazyportfolioetf.com")

    df = fetch_portfolio_results(portfolio_name, granularity)
        
    return df
