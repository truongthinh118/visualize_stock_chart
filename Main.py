import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import ta
from plotly.subplots import make_subplots

import crawl_data_trading_view as tv

st.title('Visualize VietNam Security')
st.text('Data using crawl from SSI iboard')

stock_list = tv.getAllStocks()
symbol =  st.sidebar.selectbox('Search Stock',list(stock_list['code']))

data = tv.data_from_tradingview(symbol)

st.dataframe(data)

# data["MA20"] = ta.trend.sma_indicator(data['close'], window=20)
# data["MA50"] = ta.trend.sma_indicator(data['close'], window=50)
# data["MA100"] = ta.trend.sma_indicator(data['close'], window=100)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03,
                        row_width=[0.2, 0.7])

# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=data.index,
                                open=data['open'],
                                high=data['high'],
                                low=data['low'],
                                close=data['close'], name="OHLC"),
                row=1, col=1)
# fig.add_trace(go.Line(x=data.index, y=data['MA20'], name="MA20", line=dict(
#     color="purple",
#     width=1)))
# fig.add_trace(go.Line(x=data.index, y=data['MA50'], name="MA50", line=dict(
#     color="yellow",
#     width=1.5)))
# fig.add_trace(go.Line(x=data.index, y=data['MA100'], name="MA100", line=dict(
#     color="orange",
#     width=2)))

# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=data.index, y=data['volume'], showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot
fig.update(layout_xaxis_rangeslider_visible=False)

fig.update_layout(
    autosize=False,
    width=780,
    height=540,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    )
)

st.plotly_chart(fig)