import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import fundamentus
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots

# O que falta:

    # Pensar em como fazer o filtro por setor (pegar a função com todos os tickers do setor e filtrar o b3, talvez)


# Funções que serão utilizadas

def download_screening(df):
    return df.to_csv().encode('utf-8')

b3 = fundamentus.get_resultado()

#tickers = [i + '.SA' for i in list(b3.index)]
tickers = list(b3.index)

st.title("Stock Screener")

st.subheader("\nAbaixo estão os filtros possíveis. Selecione os que deseja utilizar no seu screening\n")

st.sidebar.title("Filtros selecionados")

# Opções de filtro

roe_select      = (st.checkbox(label = 'ROE'))
pl_select       = (st.checkbox(label = 'P/L'))
dy_select       = (st.checkbox(label = 'DY'))
vol_select      = (st.checkbox(label = 'VOL'))
setor_select    = (st.checkbox(label = 'Setor'))

filtros = {}

if roe_select:
    roe = float(((st.sidebar.number_input("Escolha o ROE mínimo (%)"))) / 100)
    filtros['roe'] = roe

if pl_select:
    pl  = float((st.sidebar.number_input("Escolha o PL mínimo")))
    filtros['pl'] = pl
    

if dy_select:
    dy  = float(((st.sidebar.number_input("Escolha o DY mínimo (%)"))) / 100)
    filtros['dy'] = dy

if vol_select: 
    vol = ((st.sidebar.number_input("Escolha o Volume mínimo nos últimos 2 meses")))
    filtros['liq2m'] = vol

if setor_select:
    pass # Configurar


if filtros:
    condicoes = []

    for multiplo, valor in filtros.items():

        condicoes.append(f"{multiplo} > {valor}")

    filtro_final = " & ".join(condicoes)

    b3_final = b3.query(filtro_final)

    st.write(f"\nO screening selecionou {b3_final.shape[0]} empresas\n")

    st.write(b3_final.T)

    st.caption("Dados extraídos do site https://www.fundamentus.com.br/resultado.php")

    st.write("\nAs empresas filtradas são:\n")
    st.write(list(b3_final.index))

    screening = download_screening(b3_final.T)

    st.sidebar.download_button(
        label = "Download do Data Frame como CSV",
        data = screening,
        file_name = 'screening_python.csv',
    )

else:

    condicoes = []

    st.write(f"\nA base contém um total de {b3.shape[0]} empresas\n")

    st.write(b3.T)

    st.caption("Dados extraídos do site https://www.fundamentus.com.br/resultado.php")