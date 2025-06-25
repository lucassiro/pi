import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

_ = load_dotenv()


def get_table() -> pd.DataFrame:
    db_config = {
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "host": os.environ["DB_HOST"],
        "port": int(os.environ["DB_PORT"]),
        "database": os.environ["DB_NAME"],
    }

    query = """
        SELECT
            despesas.nome_deputado,
            despesas.ano,
            despesas.mes,
            despesas.tipo_despesa,
            despesas.valor_documento,
            despesas.cnpj_cpf_fornecedor,
            deputados.sigla_partido,
            deputados.id_legislatura,
            deputados.sigla_uf,
            fornecedores.nome_fornecedor
        FROM
            despesas
        LEFT JOIN
            deputados ON despesas.nome_deputado = deputados.nome
        LEFT JOIN
            fornecedores ON despesas.cnpj_cpf_fornecedor = fornecedores.cnpj_cpf_fornecedor;
    """

    conn = None
    try:
        conn = mysql.connector.connect(**db_config)

        if conn.is_connected():
            print("Successfully connected to MySQL database")

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        query_results = cursor.fetchall()

        df = pd.DataFrame(query_results)

        return df

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")
