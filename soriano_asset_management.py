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

# Inputs
ticker = st.text_input("Ticker:", value="VOO")
start_date = st.date_input("Start date", pd.to_datetime("2024-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))

# Descargar y mostrar datos
if ticker:
    #tickers = [ticker]  # Asegúrate que sea lista
    df = cargar_datos(ticker, start_date, end_date)

    #df = yf.download(ticker, start=start_date, end=end_date)
    st.write(df)


        # Gráfico Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
            x=df.index.date,
            y=df["Close"],
            mode="lines",
            line=dict(color="#00ffcc", width=2)
        ))
    
    fig.update_layout(
    template="plotly_dark",          # Tema oscuro
    plot_bgcolor="#1e1e1e",          # Fondo área de gráfico
    paper_bgcolor="#1e1e1e",         # Fondo general
    #width=700,   # ancho en píxeles
    #height=400,  # alto en píxeles
    font=dict(color="white"),        # Texto blanco
    xaxis=dict(
        gridcolor="#333333",         # Color de grillas
        zerolinecolor="#444444",
        title="Date",
        color="white"
    ),
    yaxis=dict(
        gridcolor="#333333",
        zerolinecolor="#444444",
        title="Close price",
        color="white"
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    ),
    title=dict(
        text=f"Close price of {ticker}",
        font=dict(color="white")
    )
    
)

    col1, col2 = st.columns([1, 1])  

    with col1:
        st.plotly_chart(fig, use_container_width=True)
    #st.plotly_chart(fig, use_container_width=False)
else:
    st.warning("No se encontraron datos para ese ticker.")
