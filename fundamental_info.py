import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import plotly.graph_objects as go

def show_fundamental_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info 
    st.title('Company Profile')
    st.subheader(info['longName']) 
    st.markdown('** Sector **: ' + info['sector'])
    st.markdown('** Industry **: ' + info['industry'])
    st.markdown('** Phone **: ' + info['phone'])
    st.markdown('** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['zip'] + ', '  +  info['country'])
    st.markdown('** Website **: ' + info['website'])
    st.markdown('** Business Summary **')
    st.info(info['longBusinessSummary'])
        
    fundInfo = {
        'Enterprise Value (USD)': info['enterpriseValue'],
        'Enterprise To Revenue Ratio': info['enterpriseToRevenue'],
        'Enterprise To Ebitda Ratio': info['enterpriseToEbitda'],
        'Net Income (USD)': info['netIncomeToCommon'],
        'Profit Margin Ratio': info['profitMargins'],
        'Forward PE Ratio': info['forwardPE'],
        'PEG Ratio': info['pegRatio'],
        'Price to Book Ratio': info['priceToBook'],
        'Forward EPS (USD)': info['forwardEps'],
        'Beta': info['beta'],
        'Book Value (USD)': info['bookValue'],
        'Dividend Rate (%)': info['dividendRate'], 
        'Dividend Yield (%)': info['dividendYield'],
        'Five year Avg Dividend Yield (%)': info['fiveYearAvgDividendYield'],
        'Payout Ratio': info['payoutRatio']
    }
    fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
    fundDF = fundDF.rename(columns={0: 'Value'})
    fundDF = fundDF.style.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    fundDF.set_properties(**{'text-align': 'left'}).hide_index()
    st.subheader('Fundamental Info') 
    st.table(fundDF)

    st.subheader('General Stock Info') 
    st.markdown('** Market **: ' + info['market'])
    st.markdown('** Exchange **: ' + info['exchange'])
    st.markdown('** Quote Type **: ' + info['quoteType'])

    start = dt.datetime.today()-dt.timedelta(2 * 365)
    end = dt.datetime.today()
    df = yf.download(ticker,start,end)
    df = df.reset_index()
    fig = go.Figure(
            data=go.Scatter(x=df['Date'], y=df['Adj Close'])
        )
    fig.update_layout(
        title={
            'text': "Stock Prices Over Past Two Years",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)

    marketInfo = {
        "Volume": info['volume'],
        "Average Volume": info['averageVolume'],
        "Market Cap": info["marketCap"],
        "Float Shares": info['floatShares'],
        "Regular Market Price (USD)": info['regularMarketPrice'],
        'Bid Size': info['bidSize'],
        'Ask Size': info['askSize'],
        "Share Short": info['sharesShort'],
        'Short Ratio': info['shortRatio'],
        'Share Outstanding': info['sharesOutstanding']
    }

    marketDF = pd.DataFrame(data=marketInfo,index=[0])
    st.table(marketDF)