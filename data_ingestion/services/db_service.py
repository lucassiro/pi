from sqlmodel import Field, Session, SQLModel, create_engine
from tqdm import tqdm

from data_ingestion.services.log_service import logger


class Despesas(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome_deputado: str
    ano: int
    mes: int
    tipo_despesa: str
    data_documento: str
    valor_documento: float
    cnpj_cpf_fornecedor: str
    valor_liquido: float
    valor_glosa: float
    fonte: str


class Fornecedores(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome_fornecedor: str
    cnpj_cpf_fornecedor: str
    fonte: str


class Deputados(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nome: str
    sigla_partido: str
    id_legislatura: int
    sigla_uf: str


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
        else:
            self.engine = create_engine(
                f"mysql+mysqldb://{user}:{password}@{host}[:{port}]/{dbname}", pool_recycle=3600
            )

    def insert_data(self, deputados: list, despesas: list, fornecedores: list) -> None:
        SQLModel.metadata.create_all(self.engine)

        with Session(self.engine) as session:
            logger.info("Inserindo deputados")
            for dep in tqdm(deputados):
                if session.get(Deputados, dep["id"]) is not None:
                    continue
                dep_tuple = Deputados(**dep)
                session.add(dep_tuple)

            logger.info("Inserindo fonecedores")
            added = []
            for forn in tqdm(fornecedores):
                if forn["cnpj_cpf_fornecedor"] in added:
                    pass
                else:
                    forn_tuple = Fornecedores(**forn)
                    session.add(forn_tuple)
                    added.append(forn["cnpj_cpf_fornecedor"])

            logger.info("Inserindo despesas")
            for desp in tqdm(despesas):
                desp_tuple = Despesas(**desp)
                session.add(desp_tuple)

            session.commit()
