import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import talib
import plotly.express as px

header = st.beta_container()
data = st.beta_container()
interactive = st.beta_container()
sidebar = st.beta_container()

with header:
    st.title("Stock Market Analysis")

with sidebar:
    st.sidebar.header('Changeable Arguments')

with interactive:

    def user_input():
        brand = st.sidebar.text_input("Brand", 'GOOGL')
        data = {'Brand': brand}
        features = pd.DataFrame(data, index=[0])
        return brand

    df = user_input()

    brand = str(df)

    time = st.sidebar.selectbox("Time Period:",options= ['1d', '5d', '1y', '2y', '3y', '5y'], index = 0)

    value = st.sidebar.selectbox("Values:",options= ["Open", 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'ma20', 'ma200', 'rsi'], index = 3)

    if time == '1d':
        int = '1m'
    elif time == '5d':
        int = '5m'
    else:
        int = '1d'

with data:
    stock = yf.download(tickers=brand, period=time, interval=int)

    fig2 = go.Figure()

    fig2.add_trace(go.Candlestick(x=stock.index,
                open=stock['Open'],
                high=stock['High'],
                low=stock['Low'],
                close=stock['Close'], name = 'market data'))

    fig2.update_layout(
        title= brand + ' live share price evolution',
        yaxis_title='Stock Price (USD per Shares)')

    fig2.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15min", step="minute", stepmode="backward"),
                dict(count=45, label="45min", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=2, label="2y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    stock.loc[:, 'ma20'] = stock.Close.rolling(20).mean()
    stock.loc[:, 'ma200'] = stock.Close.rolling(200).mean()

    stock.loc[:, "rsi"] = talib.RSI(stock.Close, 14)

    fig, ax = plt.subplots(1, 2, figsize=(21, 7))
    ax0 = stock[["rsi"]].plot(ax=ax[0])
    ax0.axhline(30, color="black")
    ax0.axhline(70, color="black")
    stock[["Close"]].plot(ax=ax[1])

    stock.columns = stock.columns.str.replace(' ', '')

@st.cache(allow_output_mutation=True)
def get_data():
    return []

def high(stoc):
    return max(stoc['High'])

def low(stoc):
    return min(stoc['Low'])

foo = high(stock)
bar = low(stock)

if st.button("Calculate Period-High/Low"):
    get_data().append({"Brand": brand, "Period High": foo, "Period Low": bar, "Period": time})

st.write(pd.DataFrame(get_data()))

st.header(brand + " Live chart")
st.plotly_chart(fig2)

st.header(value)
if value == 'Close':
    st.line_chart(stock.Close)
elif value == 'Open':
    st.line_chart(stock.Open)
elif value == 'volume':
    st.line_chart(stock.volume)
elif value == 'ma20':
    st.line_chart(stock.ma20)
elif value == 'ma200':
    st.line_chart(stock.ma200)
elif value == 'rsi':
    st.line_chart(stock.rsi)
elif value == 'High':
    st.line_chart(stock.High)
elif value == 'Low':
    st.line_chart(stock.Low)
elif value == 'Adj_Close':
    st.line_chart(stock.AdjClose)




