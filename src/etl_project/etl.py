import pandas as pd
import requests as rqs
from datetime import datetime
from conection import conexao, criar_tabela
import time
from dotenv import load_dotenv


load_dotenv()


def extract(api):
    responseAPI = rqs.get(api)
    
    if responseAPI.status_code == 200:
        return responseAPI.json()

    return None

def transform(apiResponse):
    api_cotacao_dolarReal = 'https://economia.awesomeapi.com.br/json/last/USD-BRL' # API para consultar a cotação do Dolar para Real em tempo real
    cotacaoDolarReal = extract(api_cotacao_dolarReal)

    amount = float(apiResponse['data']['amount'])  

# Ticker: É o código único, composto por letras e números, que identifica ativos (ações, FIIs, ETFs) negociados na Bolsa de Valores (B3), como PETR4 ou VALE3.
    ticker = apiResponse['data']['base']
    timestamp = datetime.now()

    brl = cotacaoDolarReal['USDBRL']['codein']
    cotacaoVenda = float(cotacaoDolarReal['USDBRL']['ask'])

    amountBrl = amount * cotacaoVenda
    
    dados = {
        'crypto': ticker,
        'amount': amount,
        'cotacao_usd_brl': cotacaoVenda,
        'amount_brl': amountBrl,
        'timestamp': timestamp
    }

    df = pd.DataFrame(dados, index=[0])

    return df


def load(conexao, dataFrame):
    dataFrame.to_sql(
        name=os.getenv('NAME_TABLE'),
        con=conexao,
        if_exists="append",
        index=False
    )
    return "Dados inseridos no Banco!"


criar_tabela(conexao())

while True:
    api_url = 'https://api.coinbase.com/v2/prices/spot' # API para consultar o valor do Bitcoin em tempo real
    
    try: 
        dados = extract(api_url)

        if dados:
            df = transform(dados)
            print(f"\nDados: {df}")
            responseDB = load(conexao(), df)
            print(responseDB)
        time.sleep(5)

    except KeyboardInterrupt:
        print("\nProcesso interrompido pelo usuário. Finalizando...")
        break

    except Exception as e:
        print(f"Erro durante a execução: {e}")
        time.sleep(5) # Atualiza a cada 10 min

