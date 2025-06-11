import os
from typing import Any

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from pymysql.err import Error
from services.log_service import logger


class PyMySQLService:
    def __init__(self) -> None:
        self.conn: Connection | None = None
        self.db_host: str | None = os.getenv("DB_HOST")
        self.db_user: str | None = os.getenv("DB_USER")
        self.db_password: str | None = os.getenv("DB_PASSWORD")
        self.db_name: str | None = os.getenv("DB_NAME")
        self.db_port: int = int(os.getenv("DB_PORT", 3306))

    def connect(self) -> bool:
        if self.conn is not None:
            self.close()

        if not all([self.db_host, self.db_user, self.db_password, self.db_name]):
            logger.error("Database connection details (host, user, password, database name) are not fully configured.")
            return False

        try:
            logger.info(
                f"Connecting to MySQL/MariaDB at {self.db_host}:{self.db_port} database: {self.db_name} using PyMySQL"
            )
            self.conn = pymysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                port=self.db_port,
                cursorclass=pymysql.cursors.Cursor,
            )
            logger.info("Successfully connected via PyMySQL.")
            return True
        except Error as e:
            logger.error(f"Error connecting via PyMySQL: {e}")
            self.conn = None
            return False

    def _execute_sql(self, sql_statement: str, params: Any | None = None, many: bool = False) -> Cursor | None:
        try:
            if self.conn is None:
                logger.error("There is no active database connection.")
                return None

            with self.conn.cursor() as cur:
                if many and params:
                    cur.executemany(sql_statement, params)
                elif params:
                    cur.execute(sql_statement, params)
                else:
                    cur.execute(sql_statement)
                self.conn.commit()
                return cur
        except Error as e:
            logger.error(f"Error executing SQL with PyMySQL: {e}")
            if self.conn:
                try:
                    self.conn.rollback()
                except Error as rb_err:
                    logger.error(f"Error during rollback: {rb_err}")
            return None

    def create_tables(self) -> None:
        if not self.conn:
            if not self.connect():
                logger.error("Cannot create tables: No active database connection and couldn't establish one.")
                return

        sql_create_deputados_table = """
        CREATE TABLE IF NOT EXISTS deputados (
            id INTEGER PRIMARY KEY,
            uri TEXT,
            nome TEXT,
            sigla_partido TEXT,
            uri_partido TEXT,
            sigla_uf TEXT,
            id_legislatura INTEGER,
            url_foto TEXT,
            email TEXT,
            fonte TEXT
        );
        """

        sql_create_despesas_table = """
        CREATE TABLE IF NOT EXISTS despesas (
            id_despesa INTEGER PRIMARY KEY AUTO_INCREMENT,
            ano INTEGER,
            mes INTEGER,
            tipo_despesa TEXT,
            cod_documento VARCHAR(255),
            tipo_documento TEXT,
            cod_tipo_documento VARCHAR(255),
            data_documento DATE,
            num_documento VARCHAR(255),
            valor_documento DECIMAL(10, 2),
            url_documento TEXT,
            nome_fornecedor TEXT,
            cnpj_cpf_fornecedor VARCHAR(20),
            valor_liquido DECIMAL(10, 2),
            valor_glosa DECIMAL(10, 2),
            num_ressarcimento VARCHAR(255),
            cod_lote VARCHAR(255),
            parcela VARCHAR(50),
            fonte TEXT
        );
        """

        sql_create_fornecedores_table = """
        CREATE TABLE IF NOT EXISTS fornecedores (
            cnpj_cpf_fornecedor VARCHAR(20) PRIMARY KEY,
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

        sql = """INSERT IGNORE INTO deputados (
                    id, uri, nome, sigla_partido, uri_partido, sigla_uf,
                    id_legislatura, url_foto, email, fonte
                )
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

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
            logger.info(f"{cursor.rowcount} deputados inseridos/ignorados.")

    def insert_despesas(self, despesas: list[dict]) -> None:
        if not self.conn:
            logger.error("There is no active database connection.")
            return
        if not despesas:
            logger.info("There are no data to insert into despesas table.")
            return

        sql = """ INSERT INTO despesas (
                ano, mes, tipo_despesa, cod_documento, tipo_documento,
                cod_tipo_documento, data_documento, num_documento, valor_documento,
                url_documento, nome_fornecedor, cnpj_cpf_fornecedor, valor_liquido,
                valor_glosa, num_ressarcimento, cod_lote, parcela, fonte
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

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
            logger.info(f"{cursor.rowcount} despesas inseridas.")

    def insert_fornecedores(self, fornecedores: list[dict]) -> None:
        if not self.conn:
            logger.error("There is no active database connection.")
            return
        if not fornecedores:
            logger.info("No supplier data provided for insertion.")
            return

        sql = """ INSERT IGNORE INTO fornecedores(cnpj_cpf_fornecedor, nome_fornecedor, fonte)
                  VALUES(%s, %s, %s) """

        data_to_insert = [
            (item.get("cnpj_cpf_fornecedor"), item.get("nome_fornecedor"), item.get("fonte"))
            for item in fornecedores
            if item.get("cnpj_cpf_fornecedor") is not None
        ]

        if data_to_insert:
            cursor = self._execute_sql(sql, data_to_insert, many=True)
            if cursor:
                logger.info(f"{cursor.rowcount} fornecedores inseridos/ignorados.")
        else:
            logger.info("No valid supplier data to insert (after filtering nulls).")

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("PyMySQL connection closed.")
