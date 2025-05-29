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
from sqlite3 import Error


class LocalDBService:
    def __init__(self):
        self.conn = None
        self.db_path = None

    def connect(self, db_path: str) -> None:
        if self.conn:
            print(f"Já conectado a {self.db_path}. Fechando conexão existente.")
            self.close()

        self.db_path = db_path
        try:
            self.conn = sqlite3.connect(self.db_path)
            print(f"Conectado ao banco de dados SQLite: {self.db_path}")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados {self.db_path}: {e}")
            self.conn = None
            self.db_path = None

    def _execute_sql(self, sql_statement: str, params=None, many=False) -> sqlite3.Cursor | None:
        if not self.conn:
            print("Erro: Nenhuma conexão com o banco de dados ativa.")
            return None
        try:
            cur = self.conn.cursor()
            if many and params:
                cur.executemany(sql_statement, params)
            elif params:
                cur.execute(sql_statement, params)
            else:
                cur.execute(sql_statement)
            self.conn.commit()
            return cur
        except Error as e:
            print(f"Erro ao executar SQL: {e}")
            return None

    def create_tables(self) -> None:
        if not self.conn:
            print("Erro: Nenhuma conexão com o banco de dados ativa para criar tabelas.")
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

        data_to_insert = []
        for dep in deputados:
            data_to_insert.append((
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
            ))

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
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

        data_to_insert = []
        for item in despesas:
            data_to_insert.append((
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
            ))

        cursor = self._execute_sql(sql, data_to_insert, many=True)
        if cursor:
            print(f"{cursor.rowcount} despesas inseridas.")

    def insert_fornecedores(self, fornecedores: list[dict]) -> None:
        if not self.conn:
            print("Erro: Nenhuma conexão com o banco de dados ativa para inserir fornecedores.")
            return
        if not fornecedores:
            print("Nenhum dado de fornecedor fornecido para inserção.")
            return

        sql = """ INSERT OR IGNORE INTO fornecedores(cnpj_cpf_fornecedor, nome_fornecedor, fonte)
                  VALUES(?,?,?) """

        data_to_insert = []
        for item in fornecedores:
            cnpj_cpf = item.get("cnpj_cpf_fornecedor")
            if cnpj_cpf is None:
                print(f"Fornecedor ignorado por ter CNPJ/CPF nulo: {item.get('nome_fornecedor')}")
                continue
            data_to_insert.append((cnpj_cpf, item.get("nome_fornecedor"), item.get("fonte")))

        if data_to_insert:
            cursor = self._execute_sql(sql, data_to_insert, many=True)
            if cursor:
                print(f"{cursor.rowcount} fornecedores inseridos/ignorados.")
        else:
            print("Nenhum fornecedor válido para inserir (após filtrar nulos).")

    def close(self) -> None:
        if self.conn:
            try:
                self.conn.close()
                print(f"Conexão com {self.db_path} fechada.")
                self.conn = None
                self.db_path = None
            except Error as e:
                print(f"Erro ao fechar a conexão com o banco de dados: {e}")
