import sqlite3
from sqlite3 import Connection, Error
from typing import Any

from data_ingestion.services.log_service import logger


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
                logger.error("There is no active database connection.")
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
            logger.info(f"Erro ao executar SQL: {e}")
            return None
        else:
            return cur

    def create_tables(self) -> None:
        if not self.conn:
            logger.error("There is no active database connection.")
            return None

        sql_create_deputados_table = """
        CREATE TABLE IF NOT EXISTS deputados (
            id INTEGER PRIMARY KEY,
            nome_deputado TEXT,
            sigla_partido TEXT,
            sigla_uf TEXT,
            id_legislatura INTEGER
        );
        """

        sql_create_despesas_table = """
        CREATE TABLE IF NOT EXISTS despesas (
            id_despesa INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_deputado TEXT,
            ano INTEGER,
            mes INTEGER,
            tipo_despesa TEXT,
            data_documento TEXT,
            valor_documento REAL,
            cnpj_cpf_fornecedor TEXT,
            valor_liquido REAL,
            valor_glosa REAL,
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

        logger.info("Verificando/Criando tabelas...")
        self._execute_sql(sql_create_deputados_table)
        self._execute_sql(sql_create_despesas_table)
        self._execute_sql(sql_create_fornecedores_table)
        logger.info("Tabelas verificadas/criadas com sucesso (se não existiam).")

    def insert_deputados(self, deputados: list[dict]) -> None:
        if not self.conn:
            logger.error("There is no active database connection.")
            return
        if not deputados:
            logger.info("Nenhum dado de deputado fornecido para inserção.")
            return

        sql = """INSERT OR IGNORE INTO deputados (
                    id,
                    nome_deputado,
                    sigla_partido,
                    sigla_uf,
                    id_legislatura
                )
                  VALUES(?,?,?,?,?)"""

        data_to_insert = [
            (
                dep.get("id"),
                dep.get("nome"),
                dep.get("sigla_partido"),
                dep.get("sigla_uf"),
                dep.get("id_legislatura"),
            )
            for dep in deputados
        ]

        cursor = self._execute_sql(sql, data_to_insert, many=True)
        if cursor:
            logger.info(f"{cursor.rowcount} deputados inseridos/ignorados.")

    def insert_despesas(self, despesas: list[dict]) -> None:
        if not self.conn:
            logger.error("There is no active database connection.")
            return
        if not despesas:
            logger.info("There are no data to insert into despesas table.")
            return

        sql = """ INSERT INTO despesas (
                nome_deputado,
                ano,
                mes,
                tipo_despesa,
                data_documento,
                valor_documento,
                cnpj_cpf_fornecedor,
                valor_liquido,
                valor_glosa,
                fonte
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)"""

        data_to_insert = [
            (
                item.get("nome_deputado"),
                item.get("ano"),
                item.get("mes"),
                item.get("tipo_despesa"),
                item.get("data_documento"),
                item.get("valor_documento"),
                item.get("cnpj_cpf_fornecedor"),
                item.get("valor_liquido"),
                item.get("valor_glosa"),
                item.get("fonte"),
            )
            for item in despesas
        ]

        cursor = self._execute_sql(sql, data_to_insert, many=True)
        if cursor:
            logger.info(f"{cursor.rowcount} despesas inseridas.")

    def insert_fornecedores(self, fornecedores: list[dict]) -> None:
        if not self.conn:
            logger.error("There is no active database connection.")
            return None
        if not fornecedores:
            logger.info("No supplier data provided for insertion.")
            return

        sql = """ INSERT OR IGNORE INTO fornecedores(cnpj_cpf_fornecedor, nome_fornecedor, fonte)
                  VALUES(?,?,?) """

        data_to_insert = [
            (item.get("cnpj_cpf_fornecedor"), item.get("nome_fornecedor"), item.get("fonte"))
            for item in fornecedores
            if item.get("cnpj_cpf_fornecedor") is not None
        ]

        if data_to_insert:
            cursor = self._execute_sql(sql, data_to_insert, many=True)
            if cursor:
                logger.info(f"{cursor.rowcount} fornecedores inseridos/ignorados.")
                logger.info(f"Total data inserted in fornecedores table: {cursor.rowcount}")
        else:
            logger.info("No valid supplier data to insert (after filtering nulls).")

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            self.db_path = None
