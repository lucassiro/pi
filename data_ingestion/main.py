import os

from dotenv import load_dotenv

from data_ingestion.services.data_service import DataService
from data_ingestion.services.db_service import DBService

_ = load_dotenv()


def main() -> None:
    url = "https://www.camara.leg.br/cotas/Ano-2022.json.zip"
    anos = [2023, 2024]

    data_service = DataService()
    deputados = data_service.get_deputados()

    api_despesas, api_fornecedores = data_service.get_data_from_api(deputados=deputados, anos=anos)
    url_despesas, url_fornecedores = data_service.get_data_from_url(url=url)

    despesas = [*api_despesas, *url_despesas]
    fornecedores = [*api_fornecedores, *url_fornecedores]

    db_service = DBService(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        dbname=os.environ["DB_NAME"],
    )
    db_service.insert_data(deputados=deputados, despesas=despesas, fornecedores=fornecedores)


if __name__ == "__main__":
    main()
