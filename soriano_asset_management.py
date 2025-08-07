import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: white;
    }

        html, body, [class*="css"]  {
        color: white !important;
        background-color: #1e1e1e;
        color: white;
    }

    /* Opcional: botones, inputs y títulos */
    .stTextInput > div > div > input {
        color: white !important;
        background-color: #333333 !important;
    }
    .stDateInput, .stCheckbox, .stButton {
        color: white !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def cargar_datos(tickers, inicio, fin):
    tickers = tickers.upper()
    data = yf.download(tickers, start=inicio, end=fin)
    data.columns = data.columns.droplevel(1)
    data.dropna(subset=["Open", "High", "Low", "Close"], inplace=True)

    return data

# Configuración de página
st.set_page_config(page_title="Soriano Asset Management Co.", layout="wide")
st.title("Soriano Asset Management Co.")

if "ticker" not in st.session_state:
    st.session_state.ticker = "VOO"
if "start_date" not in st.session_state:
    st.session_state.start_date = pd.to_datetime("2024-01-01")
if "end_date" not in st.session_state:
    st.session_state.end_date = pd.to_datetime("today")


col1, col2 = st.columns([2, 1])

with col1:
    placeholder = st.empty() 
    show_ma10 = st.checkbox("MA 10", value=True)
    show_ma20 = st.checkbox("MA 20", value=True)
    show_ma50 = st.checkbox("MA 50", value=True)
    show_candles = st.checkbox("Candles", value=True)
    bollinger = st.checkbox("Bollinger bands", value=False)    

    ticker = st.text_input("Ticker:", value="VOO", key="ticker_input")
    start_date = st.date_input("Start date", pd.to_datetime("2024-01-01"))
    end_date = st.date_input("End date", pd.to_datetime("today"))

    df = cargar_datos(ticker, start_date, end_date)

    if not df.empty:

        #fig = go.Figure()

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            row_heights=[0.8, 0.2]  
        )

        fig.update_layout(
            height=540,
            margin=dict(t=50, b=50),
            showlegend=True,
            template="plotly_dark",
            plot_bgcolor="#1e1e1e",
            paper_bgcolor="#1e1e1e",
            font=dict(color="white"),
            xaxis=dict(
                gridcolor="#333333",
                zerolinecolor="#444444",
                #title="Date",
                color="white",
                fixedrange=False,
                rangeslider=dict(visible=False),
                type='date',
                rangebreaks=[
                    dict(bounds=["sat", "mon"]), 
                    dict(values=["2024-01-01", "2024-12-25"])
                ]
            ),
            yaxis=dict(
                gridcolor="#333333",
                zerolinecolor="#444444",
                title="Price",
                color="white",
                side='right',
                autorange=True,
                fixedrange=False,
                automargin=True
            ),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                orientation = "v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=0               
            ),
            title=dict(
                text=f"{ticker.upper()}",
                font=dict(color="white")
            ),
            yaxis2=dict(
                title='Volume',
                side='right',
                #titlefont=dict(color='white'),
                tickfont=dict(color='white'),
                showgrid=False
            )
        )

        # Medias móviles
        df["MA_10"] = df["Close"].rolling(window=10).mean()
        df["MA_20"] = df["Close"].rolling(window=20).mean()
        df["MA_50"] = df["Close"].rolling(window=50).mean()
        df["MA_20"] = df["Close"].rolling(window=20).mean()

        #cálculos de las bandas de Bollinger.
        df["Upper_BB"] = df["MA_20"] + 2 * df["Close"].rolling(window=20).std()
        df["Lower_BB"] = df["MA_20"] - 2 * df["Close"].rolling(window=20).std()

        #insertamos colores para hacer un gráfico de vol
        colors = ['green' if df['Close'][i] >= df['Open'][i] else 'red' for i in range(len(df))]

        fig.add_trace(go.Bar(
            x=df.index,
            y=df['Volume'],
            marker_color=colors,
            name="Volume",
            opacity=0.6,
            yaxis='y2'
        ), row=2, col=1)

        if show_candles:
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color='green',
                decreasing_line_color='red',
                name='Candles'
            ), row=1, col=1)

        else:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Close price',
                line=dict(color="#00ffcc", width=2)
            ), row=1, col=1)

        if show_ma10:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["MA_10"],
                mode="lines",
                name="MA 10",
                line=dict(color="#0a71de", width=0.8)
            ))

        if show_ma20:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["MA_20"],
                mode="lines",
                name="MA 20",
                line=dict(color="#269e01", width=0.8)
            ))

        if show_ma50:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["MA_50"],
                mode="lines",
                name="MA 50",
                line=dict(color="#483de1", width=0.8)
            ))
        if bollinger:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Upper_BB"],
                line=dict(color="#4ec7ff", width=0.8),
                name="Upper BB",
                hoverinfo='skip',
                showlegend=True
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Lower_BB"],
                line=dict(color="#4ec7ff", width=0.8),
                name="Lower BB",
                hoverinfo='skip',
                fill='tonexty',  
                fillcolor="rgba(10, 198, 113, 0.05)",
                showlegend=True
            ))            


        placeholder.plotly_chart(fig, use_container_width=True)
    else: 
        st.warning("Ticker does not exist or dates are incorrect :(")

with col2:
    st.write("")  



