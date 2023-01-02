import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import fundamentus

# Funções que serão utilizadas
def download_screening(df):
    return df.to_csv().encode('utf-8')

# Lista de setores
setores = {1: 'Agropecuária', 2: 'Água e Saneamento', 3: 'Alimentos Processados', 4: 'Serviços Médicos', 5: 'Automóveis e Motocicletas', 6: 'Bebidas', 7: 'Comércio',8: 'Comércio e Distribuição',
9: 'Computadores e Equipamentos', 10: 'Construção Civil', 11: 'Construção e Engenharia', 12: 'Diversos', 13: 'Embalagens', 14: 'Energia Elétrica', 15: 'Equipamentos',
16: 'Exploração de Imóveis', 17: 'Gás', 18: 'Holdings Diversificadas', 19: 'Hotéis e Equipamentos', 20: 'Intermediários Financeiros', 21: 'Madeira e Papel',
22: 'Máquinas e Equipamentos', 23: 'Materiais Diversos', 24: 'Material de Transporte', 25: 'Medicamentos e Outros Produtos', 26: 'Mídia', 27: 'Mineração',
28: 'Outros', 29: 'Outros Títulos', 30: 'Petróleo, Gás e Biocombustíveis', 31: 'Previdência e Seguros', 32: 'Produtos de Uso Pessoal e Limpeza', 33: 'Programas e Serviços',
34: 'Químicos', 35: 'Securitizadoras de Recebíveis', 36: 'Serviços Diversos', 37: 'Serviços Financeiros Diversos', 38: 'Siderurgia e Metalurgia',
39: 'Tecidos, Vestuário e Calçados', 40: 'Telecomunicações', 41: 'Transporte', 42: 'Utilidades Domésticas', 43: 'Viagens e Lazer'}

b3 = fundamentus.get_resultado()

#tickers = [i + '.SA' for i in list(b3.index)]
tickers = list(b3.index)

st.title("Stock Screener")

st.subheader("\nAbaixo estão os filtros possíveis. Selecione os que deseja utilizar no seu screening\n")

st.sidebar.title("Filtros selecionados")

# Opções de filtro

setor_select    = (st.checkbox(label = 'Setor'))
roe_select      = (st.checkbox(label = 'ROE'))
pl_select       = (st.checkbox(label = 'P/L'))
dy_select       = (st.checkbox(label = 'DY'))
vol_select      = (st.checkbox(label = 'VOL'))

filtros = {}

if setor_select:
    setor = st.sidebar.selectbox(
        label = 'Escolha o setor',
        options = list(setores.values())
    )

    for codigo, setor_respectivo in setores.items():
        if setor == setor_respectivo:
            setor_selecionado = codigo

    b3_setor = fundamentus.list_papel_setor(setor_selecionado)

if roe_select:
    roe = float(((st.sidebar.number_input("Escolha o ROE mínimo (%)"))) / 100)
    filtros['roe'] = roe

if pl_select:
    pl  = float((st.sidebar.number_input("Escolha o PL máximo")))

if dy_select:
    dy  = float(((st.sidebar.number_input("Escolha o DY mínimo (%)"))) / 100)
    filtros['dy'] = dy

if vol_select: 
    vol = ((st.sidebar.number_input("Escolha o Volume mínimo nos últimos 2 meses")))
    filtros['liq2m'] = vol

confirm = st.sidebar.button('Aplicar filtros')
delete  = st.sidebar.button('Apagar todos os filtros')

# Botão de limpar filtros

if delete:
    
    for filtro in [vol_select, roe_select, pl_select, dy_select, setor_select]:
        filtro = False

# Botão para aplicar filtros

if confirm:

    if filtros:
        condicoes = []

        for multiplo, valor in filtros.items():

            condicoes.append(f"{multiplo} > {valor}")

        filtro_final = " & ".join(condicoes)

        b3_final = b3.query(filtro_final)

        if pl_select:

            b3_final = b3_final[b3_final.pl < pl]

        if setor_select:

            b3_final_setor = b3_final[b3_final.index.isin(b3_setor)]

            st.write(f"\nO screening selecionou {b3_final_setor.shape[0]} empresas\n")
        
            st.write(b3_final_setor.T)

            st.caption("Dados extraídos do site https://www.fundamentus.com.br/resultado.php")

            st.write("\nAs empresas filtradas são:\n")
            st.write(list(b3_final_setor.index))

            screening = download_screening(b3_final_setor.T)

            st.sidebar.download_button(
                label = "Download do Data Frame como CSV",
                data = screening,
                file_name = 'screening_python.csv',
            )

        else:

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

        if setor_select:
        
            b3_final = b3[b3.index.isin(b3_setor)]

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
