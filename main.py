import pickle
import bs4 as bs
import yfinance as yf
import requests
import streamlit as st
from fundamental_info import show_fundamental_stock_info
from technical_info import show_technical_info

def get_sp500_tickers():
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(response.text, "lxml")
    table = soup.find('table', {'id': 'constituents'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.find_all('td')[0].text.strip()
        tickers.append(ticker)
    return tickers

st.title('Stock Screener')
ticker = st.sidebar.selectbox('Choose a S&P 500 Stock', options=get_sp500_tickers())
info_type = st.sidebar.radio("Choose an info type",('Fundamental', 'Technical')) 
if(info_type == 'Fundamental'):
    show_fundamental_stock_info(ticker)
if(info_type == 'Technical'):
    show_technical_info(ticker)
