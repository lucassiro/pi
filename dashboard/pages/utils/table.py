import sqlite3

import pandas as pd


def get_table() -> pd.DataFrame:
    db_path = "database.db"

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
            deputados on despesas.nome_deputado = deputados.nome
        LEFT JOIN
            fornecedores ON despesas.cnpj_cpf_fornecedor = fornecedores.cnpj_cpf_fornecedor;
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    query_results = cur.fetchall()

    data = []
    for result in query_results:
        data.append({
            "nome_deputado": result[0],
            "ano": result[1],
            "mes": result[2],
            "tipo_despesa": result[3],
            "valor_documento": result[4],
            "cnpj_cpf_fornecedor": result[5],
            "sigla_partido": result[6],
            "id_legislatura": result[7],
            "sigla_uf": result[8],
            "nome_fornecedor": result[9],
        })

    df = pd.DataFrame(data)

    return df
