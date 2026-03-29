from conection import conexao
import streamlit as stl
import pandas as pd
import time
import plotly.express as px

@stl.cache_data(ttl=60*1) # Fica em cache por 1 minutos
def extractToGrafic():
    engine = conexao()

    df = pd.read_sql("SELECT * FROM cotacao_crypto", engine)
    df.rename(columns={'ticker': 'Ticker', 'Amount': 'Cotação em Dolar', 'Amount BRL': 'Cotação em Real', 'Timestamp':'Data e Hora', 'id': 'ID'}, inplace=True)

    return df


dados = extractToGrafic()

timeStamp = dados['Data e Hora']
cotacaoReal = dados['Cotação em Real']

fig = px.line(dados, x=timeStamp, y=cotacaoReal, title="Gráfico de Linhas em Real")
fig.update_layout(xaxis_title="Data", yaxis_title="Preço em BRL")


cotacaoDolar = dados['Cotação em Dolar']
figDolar = px.line(dados, x=timeStamp, y=cotacaoDolar, title="Gráfico de Linhas em Dolar")
figDolar.update_layout(xaxis_title="Data", yaxis_title="Preço em USD")

# Título da Página
stl.title('Dados do Bitcoin em Dolar e em Real - USD / BRL')

stl.plotly_chart(fig, use_container_width=True, key="btc_brl_chart")
stl.plotly_chart(figDolar, use_container_width=True, key="btc_dolar_chart")

stl.caption(f"Última atualização: {pd.Timestamp.now().strftime('%H:%M:%S')} — atualiza a cada 10 min")
time.sleep(60*10) # Atualiza a cada hora
stl.rerun()
