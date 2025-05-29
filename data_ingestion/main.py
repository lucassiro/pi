import pandas as pd

from data_ingestion.services.api_service import CamaraAPI
from data_ingestion.services.data_processor_service import DataProcessorService
from data_ingestion.services.local_db_service import LocalDBService


def main() -> None:
    urls = ["https://www.camara.leg.br/cotas/Ano-2022.json.zip"]
    years = [2023, 2024]

    api = CamaraAPI()
    deputados, data = api.get_data(urls=urls, years=years)

    data = {key: value[:2] for key, value in data.items()}

    data_processor = DataProcessorService(data=data, deputados=deputados)
    despesas, fornecedores, deputados_ = data_processor.process_data()

    pd.DataFrame(despesas).to_csv("despesas.csv", index=False)
    pd.DataFrame(fornecedores).to_csv("fornecedores.csv", index=False)
    pd.DataFrame(deputados_).to_csv("deputados.csv", index=False)

    db_service = LocalDBService()

    try:
        db_service.connect("database.db")

        if db_service.conn:
            db_service.create_tables()
            db_service.insert_deputados(deputados)
            db_service.insert_despesas(despesas)
            db_service.insert_fornecedores(fornecedores)

    except Exception as e:
        print(f"Ocorreu um erro geral: {e}")
    finally:
        db_service.close()


if __name__ == "__main__":
    main()
