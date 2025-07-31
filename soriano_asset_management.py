import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Funciones auxiliares
def calcular_sharpe_ratio(returns, risk_free_rate=0.02):
    excess_returns = returns - risk_free_rate / 252
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

def calcular_sortino_ratio(returns, risk_free_rate=0.02, target_return=0):
    excess_returns = returns - risk_free_rate / 252
    downside_returns = excess_returns[excess_returns < target_return]
    downside_deviation = np.sqrt(np.mean(downside_returns**2))
    return np.sqrt(252) * excess_returns.mean() / downside_deviation if downside_deviation != 0 else np.nan

# Forzar fondo oscuro de la app
st.markdown(
    """
    <style>
    .main {
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuración de la página
st.set_page_config(page_title="Soriano Asset Management Co.", layout="wide")
st.sidebar.title("Soriano Asset Management Co.")
st.title("Visor de datos financieros")

# Input ticker y fechas
ticker = st.text_input("Ingresa el ticker del activo (ej. AAPL, BTC-USD, ^GSPC):", value="AAPL")
start_date = st.date_input("Fecha de inicio", pd.to_datetime("2020-01-01"))
end_date = st.date_input("Fecha de fin", pd.to_datetime("today"))

if ticker:
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            st.warning("No se encontraron datos para ese ticker y fechas.")
        else:
            # Solo tomamos las filas donde Close no sea NaN
            df = df[df["Close"].notna()]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Close"],
                mode='lines',
                name='Precio Cierre',
                line=dict(color="#00ffcc", width=2)
            ))
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#1e1e1e",
                paper_bgcolor="#1e1e1e",
                font=dict(color="white"),
                title=f"{ticker} - Precio de Cierre",
                xaxis_title="Fecha",
                yaxis_title="Precio",
                xaxis=dict(gridcolor="#333333", zerolinecolor="#444444"),
                yaxis=dict(gridcolor="#333333", zerolinecolor="#444444"),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Ocurrió un error al obtener los datos: {e}")
