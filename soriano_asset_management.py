import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime

# Configuración
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
        # Gráfico Altair personalizado
        chart = alt.Chart(df).mark_line(
            color="#00ffcc",  # color estilo Bloomberg
            strokeWidth=2
        ).encode(
            x=alt.X('Date:T', axis=alt.Axis(title='Fecha')),
            y=alt.Y('Close:Q', axis=alt.Axis(title='Precio')),
            tooltip=["Date:T", "Close:Q"]
        ).properties(
            width=600,
            height=400,
            title=f"{ticker} - Precio de Cierre"
        ).configure_view(
            stroke=None,
            fill='#1e1e1e'  # Fondo oscuro
        ).configure_axis(
            labelColor='white',
            titleColor='white',
            gridColor='#333'
        ).configure_title(
            color='white'
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            st.altair_chart(chart, use_container_width=False)

        st.subheader("Últimos datos")
        st.dataframe(df.tail())
    else:
        st.warning("No se encontraron datos para ese ticker.")
