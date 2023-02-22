import requests
import pandas as pd
from bs4 import BeautifulSoup
from os import path
from datetime import datetime, timedelta
from typing import List, Dict

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
    if '+' in percentage_gain_str:
        percentage_gain_str = percentage_gain_str.replace('+', '')
        percentage_gain_numeric = float(percentage_gain_str)
        percentage_gain_numeric = (100 + percentage_gain_numeric)/100
        
    else:
        percentage_gain_str = percentage_gain_str.replace('-', '')
        percentage_gain_numeric = float(percentage_gain_str)
        percentage_gain_numeric = (100 - percentage_gain_numeric)/100
    
    return percentage_gain_numeric

def parse_monthly_results(soup) -> List[Dict]:
    result = []

    html_table = soup.find('table', id='yearReturns')
    html_table_tbody = html_table.find('tbody')
    html_table_tbody_rows = html_table_tbody.findAll('tr')
    
    for row in html_table_tbody_rows:
        current_year = datetime(int(row.find('td').text), 1, 1)
        for index, month in enumerate(row.find_all('td')):
            if index < 3:
                continue
            
        total = convert_yearly_return_to_numeric(row.find_all('td')[1].text)
        inflation_adjusted = convert_yearly_return_to_numeric(row.find_all('td')[2].text)
        result.append({'date': current_year, 'inflation_adjusted': inflation_adjusted, 'total': total})
        
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

    if(granularity == 'y' or granularity != 'y'):
        df = pd.DataFrame(parse_yearly_results(soup))
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
