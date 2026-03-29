from conection import conexao
import streamlit as stl
import pandas as pd
import time
import numpy as np

engine = conexao()

df = pd.read_sql("SELECT * FROM cotacao_crypto", engine)
df.rename(columns={'ticker': 'Ticker', 'Amount': 'Cotação em Dolar', 'Amount BRL': 'Cotação em Real', 'Timestamp':'Data e Hora', 'id': 'ID'}, inplace=True)


# Título da Página
stl.title('Dados relacionados ao Bitcoin')

# Dataframe exposto
stl.dataframe(df, hide_index=True)

