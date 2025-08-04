import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go


# Estilos personalizados para modo oscuro
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    .stApp {
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def cargar_datos(tickers, inicio, fin):
    data = yf.download(tickers, start=inicio, end=fin)
    data['Retornos'] = data['Close'].pct_change()
    #data.index = data.index.droplevel(1)
    data.columns = data.columns.droplevel(1)
    #data = data[tickers]
    return data

# Configuración de página
st.set_page_config(page_title="Soriano Asset Management Co.", layout="wide")
st.title("Soriano Asset Management Co.")


ticker = st.text_input("Ticker:", value="VOO.MX")
start_date = st.date_input("Start date", pd.to_datetime("2024-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))


if ticker:

    df = cargar_datos(ticker, start_date, end_date)



    st.write(df)


        # Gráfico Plotly
    fig = go.Figure()

    

    #fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close", line=dict(color="#00ffcc")))
    df["MA_10"] = df["Close"].rolling(window=10).mean()
    df["MA_20"] = df["Close"].rolling(window=20).mean()
    df["MA_50"] = df["Close"].rolling(window=50).mean()

        # Checkboxes para mostrar medias móviles
    show_ma10 = st.checkbox("MA 10", value=False)
    show_ma20 = st.checkbox("MA 20", value=False)
    show_ma50 = st.checkbox("MA 50", value=False)
    show_candles = st.checkbox("Candles", value=False)


    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e",
        font=dict(color="white"),
        xaxis=dict(
            gridcolor="#333333",
            zerolinecolor="#444444",
            title="Date",
            color="white",
            fixedrange=False,
            rangeslider=dict(visible=True),  
            type='date'
        ),
        yaxis=dict(
            gridcolor="#333333",
            zerolinecolor="#444444",
            title="Close price",
            color="white",
            autorange=True,
            fixedrange=False,
            automargin=True,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        ),
        title=dict(
            text=f"Close of {ticker}",
            font=dict(color="white")
        )
    )

    col1, col2 = st.columns([1, 1])  

    with col1:
  
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
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Close',
                line=dict(color="#00ffcc", width=1)
            ))
        if show_ma10:
            fig.add_trace(go.Scatter(x=df.index, 
                                     y=df["MA_10"], 
                                     mode="lines", 
                                     name="MA 10", 
                                     line=dict(color="#0a71de", width = 0.8)))
        if show_ma20:
            fig.add_trace(go.Scatter(x=df.index, 
                                     y=df["MA_20"], 
                                     mode="lines", 
                                     name="MA 20", 
                                     line=dict(color="#269e01", width = 0.8)))
        if show_ma50:
            fig.add_trace(go.Scatter(x=df.index, 
                                     y=df["MA_50"], 
                                     mode="lines", 
                                     name="MA 50", 
                                     line=dict(color="#483de1", width = 0.8)))                  
        st.plotly_chart(fig, use_container_width=True)
        
    #st.plotly_chart(fig, use_container_width=False)
else:
    st.warning("No se encontraron datos para ese ticker.")
