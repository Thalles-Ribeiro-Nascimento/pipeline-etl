from sqlalchemy import create_engine
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


