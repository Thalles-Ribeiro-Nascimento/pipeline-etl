from sqlalchemy import (
    create_engine,
    Table, Column, MetaData,
    Integer, String, Float, DateTime
)
import os
from dotenv import load_dotenv


load_dotenv()

def conexao():

# Criando a conexão com o Banco de Dados MySQL
    host = os.getenv('HOST')
    name_db = os.getenv('NAME')
    user = os.getenv('USER_DB')
    port = os.getenv('PORT')
    password = os.getenv('PASSWORD')


    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{name_db}"
    )

def criar_tabela(engine):
    metadata = MetaData()

    cotacao_crypto = Table(
        "cotacao_crypto", metadata,
        Column("id",              Integer,    primary_key=True, autoincrement=True),
        Column("crypto",          String(50), nullable=False),
        Column("amount",          Float,      nullable=False),
        Column("cotacao_usd_brl", Float,      nullable=False),
        Column("amount_brl",      Float,      nullable=False),
        Column("timestamp",       DateTime),
    )
 
    metadata.create_all(engine, checkfirst=True)
