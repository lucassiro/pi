# deputados = {
#     "id": "",
#     "uri": "",
#     "nome": "",
#     "sigla_partido": "",
#     "uri_partido": "",
#     "sigla_uf": "",
#     "id_legislatura": "",
#     "url_foto": "",
#     "email": "",
#     "fonte": "",
# }

# despesas = {
#     "ano": "",
#     "mes": "",
#     "tipoDespesa": "",
#     "codDocumento": "",
#     "tipoDocumento": "",
#     "codTipoDocumento": "",
#     "dataDocumento": "",
#     "numDocumento": "",
#     "valorDocumento": "",
#     "urlDocumento": "",
#     "nomeFornecedor": "",
#     "cnpjCpfFornecedor": "",
#     "valorLiquido": "",
#     "valorGlosa": "",
#     "numRessarcimento": "",
#     "codLote": "",
#     "parcela": "",
#     "fonte": "",
# }
# fornecedores = {
#     "nomeFornecedor": "",
#     "cnpjCpfFornecedor": "",
#     "fonte": "",
# }

import sqlite3
from sqlite3 import Connection, Error
from typing import Any


class LocalDBService:
    def __init__(self) -> None:
        self.conn: Connection | None = None
        self.db_path: str | None = None

    def connect(self, db_path: str) -> None:
        if self.conn is not None:
            self.close()

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def _execute_sql(self, sql_statement: str, params: Any | None = None, many: bool = False) -> sqlite3.Cursor | None:
        try:
            if self.conn is None:
                print("Erro: Nenhuma conexão com o banco de dados ativa.")
                return None
            cur = self.conn.cursor()
            if many and params:
                cur.executemany(sql_statement, params)
            elif params:
                cur.execute(sql_statement, params)
            else:
                cur.execute(sql_statement)
            self.conn.commit()
        except Error as e:
            print(f"Erro ao executar SQL: {e}")
            return None
        else:
            return cur

    def create_tables(self) -> None:
        if not self.conn:
            print("Erro: Nenhuma conexão com o banco de dados ativa para criar tabelas.")
            return None

        sql_create_deputados_table = """
        CREATE TABLE IF NOT EXISTS deputados (
            id INTEGER PRIMARY KEY,
            uri TEXT NULL,
            nome TEXT NULL,
            sigla_partido TEXT NULL,
            uri_partido TEXT NULL,
            sigla_uf TEXT NULL,
            id_legislatura INTEGER NULL,
            url_foto TEXT NULL,
            email TEXT NULL,
            fonte TEXT NULL
        );
        """

        sql_create_despesas_table = """
        CREATE TABLE IF NOT EXISTS despesas (
            id_despesa INTEGER PRIMARY KEY AUTOINCREMENT,
            ano INTEGER,
            mes INTEGER,
            tipo_despesa TEXT,
            cod_documento TEXT,
            tipo_documento TEXT,
            cod_tipo_documento TEXT,
            data_documento TEXT,
            num_documento TEXT,
            valor_documento REAL,
            url_documento TEXT,
            nome_fornecedor TEXT,
            cnpj_cpf_fornecedor TEXT,
            valor_liquido REAL,
            valor_glosa REAL,
            num_ressarcimento TEXT,
            cod_lote TEXT,
            parcela TEXT,
            fonte TEXT
        );
        """

        sql_create_fornecedores_table = """
        CREATE TABLE IF NOT EXISTS fornecedores (
            cnpj_cpf_fornecedor TEXT PRIMARY KEY,
            nome_fornecedor TEXT,
            fonte TEXT
        );
        """

        print("Verificando/Criando tabelas...")
        self._execute_sql(sql_create_deputados_table)
        self._execute_sql(sql_create_despesas_table)
        self._execute_sql(sql_create_fornecedores_table)
        print("Tabelas verificadas/criadas com sucesso (se não existiam).")

    def insert_deputados(self, deputados: list[dict]) -> None:
        if not self.conn:
            print("Erro: Nenhuma conexão com o banco de dados ativa para inserir deputados.")
            return
        if not deputados:
            print("Nenhum dado de deputado fornecido para inserção.")
            return

        sql = """ INSERT OR IGNORE INTO deputados(id, uri, nome, sigla_partido, uri_partido, sigla_uf, id_legislatura, url_foto, email, fonte)
                  VALUES(?,?,?,?,?,?,?,?,?,?) """

        data_to_insert = [
            (
                dep.get("id"),
                dep.get("uri"),
                dep.get("nome"),
                dep.get("sigla_partido"),
                dep.get("uri_partido"),
                dep.get("sigla_uf"),
                dep.get("id_legislatura"),
                dep.get("url_foto"),
                dep.get("email"),
                dep.get("fonte"),
            )
            for dep in deputados
        ]

        cursor = self._execute_sql(sql, data_to_insert, many=True)
        if cursor:
            print(f"{cursor.rowcount} deputados inseridos/ignorados.")

    def insert_despesas(self, despesas: list[dict]) -> None:
        if not self.conn:
            print("Erro: Nenhuma conexão com o banco de dados ativa para inserir despesas.")
            return
        if not despesas:
            print("Nenhum dado de despesa fornecido para inserção.")
            return

        sql = """ INSERT INTO despesas(ano, mes, tipo_despesa, cod_documento, tipo_documento, cod_tipo_documento, data_documento, num_documento, valor_documento, url_documento, nome_fornecedor, cnpj_cpf_fornecedor, valor_liquido, valor_glosa, num_ressarcimento, cod_lote, parcela, fonte)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

        data_to_insert = [
            (
                item.get("ano"),
                item.get("mes"),
                item.get("tipo_despesa"),
                item.get("cod_documento"),
                item.get("tipo_documento"),
                item.get("cod_tipo_documento"),
                item.get("data_documento"),
                item.get("num_documento"),
                item.get("valor_documento"),
                item.get("url_documento"),
                item.get("nome_fornecedor"),
                item.get("cnpj_cpf_fornecedor"),
                item.get("valor_liquido"),
                item.get("valor_glosa"),
                item.get("num_ressarcimento"),
                item.get("cod_lote"),
                item.get("parcela"),
                item.get("fonte"),
            )
            for item in despesas
        ]

        cursor = self._execute_sql(sql, data_to_insert, many=True)
        if cursor:
            print(f"{cursor.rowcount} despesas inseridas.")

    def insert_fornecedores(self, fornecedores: list[dict]) -> None:
        if not self.conn:
            print("Erro: Nenhuma conexão com o banco de dados ativa para inserir fornecedores.")
            return None
        if not fornecedores:
            print("Nenhum dado de fornecedor fornecido para inserção.")
            return

        sql = """ INSERT OR IGNORE INTO fornecedores(cnpj_cpf_fornecedor, nome_fornecedor, fonte)
                  VALUES(?,?,?) """

        data_to_insert = [
            (item.get("cnpj_cpf_fornecedor"), item.get("nome_fornecedor"), item.get("fonte"))
            for item in fornecedores
            if item.get("cnpj_cpf_fornecedor") is not None
        ]

        ignored = len(fornecedores) - len(data_to_insert)
        if ignored > 0:
            print(f"{ignored} fornecedores ignorados por ter CNPJ/CPF nulo.")

        if data_to_insert:
            cursor = self._execute_sql(sql, data_to_insert, many=True)
            if cursor:
                print(f"{cursor.rowcount} fornecedores inseridos/ignorados.")
        else:
            print("Nenhum fornecedor válido para inserir (após filtrar nulos).")

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            self.db_path = None
