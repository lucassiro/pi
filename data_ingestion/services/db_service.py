from sqlalchemy import Column, Float, Integer, String, create_engine, insert
from sqlalchemy.orm import declarative_base, sessionmaker

from data_ingestion.services.log_service import logger

Base = declarative_base()


class Despesas(Base):
    __tablename__ = "despesas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_deputado = Column(String(100))
    ano = Column(Integer)
    mes = Column(Integer)
    tipo_despesa = Column(String(100))
    data_documento = Column(String(100))
    valor_documento = Column(Float)
    cnpj_cpf_fornecedor = Column(String(100))
    valor_liquido = Column(Float)
    valor_glosa = Column(Float)
    fonte = Column(String(100))


class Fornecedores(Base):
    __tablename__ = "fornecedores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_fornecedor = Column(String(100))
    cnpj_cpf_fornecedor = Column(String(100), unique=True)
    fonte = Column(String(100))


class Deputados(Base):
    __tablename__ = "deputados"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True)
    sigla_partido = Column(String(100))
    id_legislatura = Column(Integer)
    sigla_uf = Column(String(100))


class DBService:
    def __init__(
        self,
        local: bool = False,
        user: str | None = None,
        password: str | None = None,
        host: str | None = None,
        port: int | None = None,
        dbname: str | None = None,
    ) -> None:
        if local:
            self.engine = create_engine("sqlite:///database.db")
            self.dialect = "sqlite"
        else:
            self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}", pool_recycle=3600)

            self.dialect = "mysql"
        self.Session = sessionmaker(bind=self.engine)

    def insert_data(self, deputados: list, despesas: list, fornecedores: list) -> None:
        Base.metadata.create_all(self.engine)
        session = self.Session()

        try:
            logger.info("Inserindo deputados")
            if deputados:
                stmt = insert(Deputados)
                if self.dialect == "sqlite":
                    stmt = stmt.prefix_with("OR IGNORE")
                elif self.dialect == "mysql":
                    stmt = stmt.prefix_with("IGNORE")
                session.execute(stmt, deputados)

            logger.info("Inserindo fornecedores")
            if fornecedores:
                stmt = insert(Fornecedores)
                if self.dialect == "sqlite":
                    stmt = stmt.prefix_with("OR IGNORE")
                elif self.dialect == "mysql":
                    stmt = stmt.prefix_with("IGNORE")
                session.execute(stmt, fornecedores)

            logger.info("Inserindo despesas")
            if despesas:
                stmt = insert(Despesas)
                if self.dialect == "sqlite":
                    stmt = stmt.prefix_with("OR IGNORE")
                elif self.dialect == "mysql":
                    stmt = stmt.prefix_with("IGNORE")
                session.execute(stmt, despesas)

            session.commit()
        finally:
            session.close()
