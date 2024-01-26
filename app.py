# import streamlit as st 
# import yfinance as yf 
# import pandas as pd
# import numpy as np 
# from tradingview_ta import TA_Handler, Interval, Exchange
# import tradingview_ta
# import pickle

# option = "ASII"
# period = "1y"

# stock_name = {
#     "ASII":"Astra International Tbk PT",
#     "BBCA":"Bank Central Asia Tbk PT",
#     "BBRI":"Bank Rakyat Indonesia (Persero) Tbk PT",
#     "BBNI":"Bank Negara Indonesia (Persero) Tbk PT",
#     "BMRI":"Bank Mandiri (Persero) Tbk PT",
#     "GGRM":"Gudang Garam Tbk PT",
#     "SIDO":"Industri Jamu dn Frms Sd Mncl Tbk PT",
#     "TLKM":"Telkom Indonesia (Persero) Tbk PT",
#     "UNTR":"United Tractors Tbk PT",
#     "UNVR":"Unilever Indonesia Tbk PT"
#     }
# with st.sidebar :
#   st.title("Stock Predicition Dashboard")
#   st.header("Stock Name")
#   with st.expander("**Stock name explanation !**"):
#       st.write("You have to use stock **tick code**")
#       st.write("to generate **info** and **result**") 
#   option = st.selectbox(
#         'Select your tick code',
#         ('ASII', 'BBCA', 'BBRI','BBNI','BMRI','GGRM','SIDO','TLKM','UNTR','UNVR'))
#   period = st.selectbox(
#         'Chart period',
#         ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"))
   

# stock = yf.Ticker(option+".jk")
# close = stock.history(period="1y")["Close"]
# op = stock.history(period="1y")["Open"]
# hi = stock.history(period="1y")["High"]
# low = stock.history(period="1y")["Low"]
# yesterday = close[len(close)-2]
# today = close[len(close-1)-1]
# change = round((today - yesterday)/yesterday,4)
# percentage = round(change * 100,2)
# prediction = 0


# st.header("Info & Result")
# st.subheader(option + " - " + stock_name[option])
# col1, col2, col3, col4 = st.columns(4)
# col1.metric("Open",str(op[len(op)-1]))
# col2.metric("Close",str(today))
# col3.metric("High",str(hi[len(hi)-1]))
# col4.metric("Low",str(low[len(low)-1]))
# tab1, tab2, tab3 = st.tabs(["Stock Chart", "Stock Metric", "Recommendation"])
# with tab1 : 
#     st.subheader("Stock Chart")
#     st.line_chart(stock.history(period=period)["Close"])
# with tab2 :
#     loaded_model = pickle.load(open("stock_model.sav", 'rb'))
#     y_pred = loaded_model.predict([[op[len(op)-1],hi[len(hi)-1],low[len(low)-1],today]])
#     np.set_printoptions(precision=2)
#     result = np.concatenate((y_pred.reshape(len(y_pred),1)))
#     prediction  = round(result[0],1)
#     different = round((prediction - today)/today,4)
#     diff_percentage = round(different * 100,2)
#     st.subheader("Stock Metric")
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Yesterday", str(yesterday))
#     col2.metric("Today", str(today), str(percentage)+"%")
#     col3.metric("Prediction",str(prediction), str(diff_percentage)+"%")

# with tab3 :
#     handler = TA_Handler(
#     symbol= option,
#     exchange="idx",
#     screener="indonesia",
#     interval="1M",
#     timeout=None
#     )
#     analysis = handler.get_analysis()
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Buy",(analysis.summary["BUY"]))
#     col2.metric("Neutral",(analysis.summary["NEUTRAL"]))
#     col3.metric("Sell",(analysis.summary["SELL"]))

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from tradingview_ta import TA_Handler, Interval, Exchange
import pickle

# Use f-strings for string formatting
option_name = stock_name[option]
st.title(f"Stock Prediction Dashboard for {option_name}")

# Use st.markdown to write markdown text
with st.sidebar:
    st.markdown("# Stock Prediction Dashboard")
    st.markdown("## Stock Name")
    st.markdown("""
        You have to use stock **tick code**
        to generate **info** and **result**
    """)

# Use st.dataframe to display DataFrame
st.dataframe(stock.history(period="1y"))

# Use st.table to display tabular data
st.table(stock.info)

# Use st.cache to cache the data
@st.cache
def load_model():
    return pickle.load(open("stock_model.sav", 'rb'))

loaded_model = load_model()

# Use st.session_state to store and retrieve user input
if 'option' not in st.session_state:
    st.session_state['option'] = option
else:
    option = st.session_state['option']

if 'period' not in st.session_state:
    st.session_state['period'] = period
else:
    period = st.session_state['period']

try:
    stock = yf.Ticker(option+".jk")
    close = stock.history(period=st.session_state['period'])["Close"]
    op = stock.history(period=st.session_state['period'])["Open"]
    hi = stock.history(period=st.session_state['period'])["High"]
    low = stock.history(period=st.session_state['period'])["Low"]
    yesterday = close[len(close)-2]
    today = close[len(close)-1]
    change = round((today - yesterday)/yesterday,4)
    percentage = round(change * 100,2)
    prediction = 0

    st.header("Info & Result")
    st.subheader(option + " - " + stock_name[option])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Open",str(op[len(op)-1]))
    col2.metric("Close",str(today))
    col3.metric("High",str(hi[len(hi)-1]))
    col4.metric("Low",str(low[len(low)-1]))
    tab1, tab2, tab3 = st.tabs(["Stock Chart", "Stock Metric", "Recommendation"])
    with tab1 : 
        st.subheader("Stock Chart")
        st.line_chart(stock.history(period=st.session_state['period'])["Close"])
    with tab2 :
        y_pred = loaded_model.predict([[op[len(op)-1],hi[len(hi)-1],low[len(low)-1],today]])
        np.set_printoptions(precision=2)
        result = np.concatenate((y_pred.reshape(len(y_pred),1)))
        prediction  = round(result[0],1)
        different = round((prediction - today)/today,4)
        diff_percentage = round(different * 100,2)
        st.subheader("Stock Metric")
        col1, col2, col3 = st.columns(3)
        col1.metric("Yesterday", str(yesterday))
        col2.metric("Today", str(today), str(percentage)+"%")
        col3.metric("Prediction",str(prediction), str(diff_percentage)+"%")

    with tab3 :
        handler = TA_Handler(
        symbol= option,
        exchange="idx",
        screener="indonesia",
        interval="1M",
        timeout=None
        )
        analysis = handler.get_analysis()
        col1, col2, col3 = st.columns(3)
        col1.metric("Buy",(analysis.summary["BUY"]))
        col2.metric("Neutral",(analysis.summary["NEUTRAL"]))
        col3.metric("Sell",(analysis.summary["SELL"]))
except Exception as e:
    st.exception(e)
