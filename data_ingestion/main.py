from data_ingestion.services.api_service import GetDataService
from data_ingestion.services.local_db_service import LocalDBService


def main() -> None:
    url = "https://www.camara.leg.br/cotas/Ano-2022.json.zip"
    anos = [2023, 2024]

    data_service = GetDataService()
    deputados = data_service.get_deputados()

    api_despesas, api_fornecedores = data_service.get_data_from_api(deputados=deputados, anos=anos)
    url_despesas, url_fornecedores = data_service.get_data_from_url(url=url)

    despesas = [*api_despesas, *url_despesas]
    fornecedores = [*api_fornecedores, *url_fornecedores]

    db_service = LocalDBService()
    db_service.connect("database2.db")

    db_service.create_tables()
    db_service.insert_deputados(deputados)
    db_service.insert_despesas(despesas)
    db_service.insert_fornecedores(fornecedores)
    db_service.close()


if __name__ == "__main__":
    main()
