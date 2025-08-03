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
    datos = {}
    for ticker in tickers:
        df = yf.download(ticker, start=inicio, end=fin)
        df['Retornos'] = df['Close'].pct_change()
        datos[ticker] = df
    return datos

# Configuración de página
st.set_page_config(page_title="Soriano Asset Management Co.", layout="wide")
st.title("Soriano Asset Management Co.")

# Inputs
ticker = st.text_input("Ticker:", value="VOO")
start_date = st.date_input("Fecha inicio", pd.to_datetime("2024-01-01"))
end_date = st.date_input("Fecha fin", pd.to_datetime("today"))

# Descargar y mostrar datos
if ticker:
    df = cargar_datos(ticker, start_date, end_date)
    #df = yf.download(ticker, start=start_date, end=end_date)
    st.write(df)


        # Gráfico Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
            x=df.index.date,
            y=df["Close"],
            mode="lines",
            name="Precio de Cierre",
            line=dict(color="#00ffcc", width=2)
        ))



    st.plotly_chart(fig, use_container_width=False)
else:
    st.warning("No se encontraron datos para ese ticker.")
