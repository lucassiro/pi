from data_ingestion.services.api_service import CamaraAPI
from data_ingestion.services.data_processor_service import DataProcessorService
from data_ingestion.services.local_db_service import LocalDBService


def main() -> None:
    urls = ["https://www.camara.leg.br/cotas/Ano-2022.json.zip"]
    years = [2023, 2024]

    api = CamaraAPI()
    deputados, data = api.get_data(urls=urls, years=years)

    data_processor = DataProcessorService(data=data, deputados=deputados)
    despesas, fornecedores, deputados_ = data_processor.process_data()

    db_service = LocalDBService()
    db_service.connect("database.db")

    db_service.create_tables()
    db_service.insert_deputados(deputados_)
    db_service.insert_despesas(despesas)
    db_service.insert_fornecedores(fornecedores)
    db_service.close()


if __name__ == "__main__":
    main()
