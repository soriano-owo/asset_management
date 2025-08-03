import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime

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
 # Gráfico Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode='lines',
            name='Precio de Cierre',
            line=dict(color="#00ffcc", width=2)
        ))

        fig.update_layout(
            title=f"{ticker} - Precio de Cierre",
            template="plotly_dark",
            plot_bgcolor="#1e1e1e",
            paper_bgcolor="#1e1e1e",
            font=dict(color='white'),
            xaxis=dict(
                title="Fecha",
                gridcolor="#333333",
                zerolinecolor="#444444"
            ),
            yaxis=dict(
                title="Precio",
                gridcolor="#333333",
                zerolinecolor="#444444"
            ),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            ),
        )

        st.subheader("Últimos datos")
        st.dataframe(df.tail())
    else:
        st.warning("No se encontraron datos para ese ticker.")
