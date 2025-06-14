import sqlite3

import pandas as pd


def get_table() -> pd.DataFrame:
    db_path = "database.db"

    query = """
    SELECT
    -- Colunas da tabela 'deputados'
    dep.id AS id_deputado,
    dep.nome_deputado,
    dep.sigla_partido,
    dep.sigla_uf,
    dep.id_legislatura,

    -- Colunas da tabela 'despesas'
    d.id_despesa,
    d.ano,
    d.mes,
    d.tipo_despesa,
    d.data_documento,
    d.valor_documento,
    d.valor_liquido,
    d.valor_glosa,

    -- Colunas da tabela 'fornecedores'
    f.cnpj_cpf_fornecedor,
    f.nome_fornecedor
    FROM
    despesas AS d
    JOIN
    deputados AS dep
    ON d.nome_deputado = dep.nome_deputado
    JOIN
    fornecedores AS f
    ON d.cnpj_cpf_fornecedor = f.cnpj_cpf_fornecedor;
    """

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    query_results = cur.fetchall()

    data = [
        {
            # Colunas de 'deputados'
            "id_deputado": result[0],
            "nome_deputado": result[1],
            "sigla_partido": result[2],
            "sigla_uf": result[3],
            "id_legislatura": result[4],
            # Colunas de 'despesas'
            "id_despesa": result[5],
            "ano": result[6],
            "mes": result[7],
            "tipo_despesa": result[8],
            "data_documento": result[9],
            "valor_documento": result[10],
            "valor_liquido": result[11],
            "valor_glosa": result[12],
            # Colunas de 'fornecedores'
            "cnpj_cpf_fornecedor": result[13],
            "nome_fornecedor": result[14],
        }
        for result in query_results
    ]

    df = pd.DataFrame(data)

    return df
