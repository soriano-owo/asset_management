import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Soriano Asset Management Co.", layout="wide")

st.title("Soriano Asset Management Co.")


# Inputs
ticker = st.text_input("Ticker:", value="AAPL")
start_date = st.date_input("Fecha inicio", pd.to_datetime("2020-01-01"))
end_date = st.date_input("Fecha fin", pd.to_datetime("today"))

# Descargar datos
if ticker:
    df = yf.download(ticker, start=start_date, end=end_date)
    df = df[["Close"]].dropna().reset_index()

    if not df.empty:
        # Crear gráfico Altair (más customizable que st.line_chart)
        chart = alt.Chart(df).mark_line(
            color="#00ffcc",  # color estilo Bloomberg
            strokeWidth=2
        ).encode(
            x='Date:T',
            y='Close:Q',
            tooltip=["Date:T", "Close:Q"]
        ).properties(
            width=1000,
            height=400,
            title=f"{ticker} - Precio de Cierre"
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            labelColor='white',
            titleColor='white',
            gridColor='#333'
        ).configure_title(
            color='white'
        ).configure_background(
            color='#1e1e1e'
        )

        st.altair_chart(chart, use_container_width=True)
        st.dataframe(df.tail())
    else:
        st.warning("No se encontraron datos para ese ticker.")
