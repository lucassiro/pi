import io
import json
import zipfile

import httpx
from logs import logger


class CamaraAPI:
    def __init__(self) -> None:
        self.api_base_url = "https://dadosabertos.camara.leg.br/api/v2"

    def request(self, endpoint: str) -> dict:
        response = httpx.get(f"{self.api_base_url}/{endpoint}")
        return response.json()

    def get_deputados(self) -> dict:
        return self.request("deputados")

    def data_from_api(self, id: int, year: int) -> dict:
        return self.request(f"deputados/{id}/despesas?ano={year}")

    @staticmethod
    def data_from_url(url: str) -> dict[str, list[dict]]:
        response = httpx.get(url=url)
        zip_content = response.content

        with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
            with zip_file.open(zip_file.namelist()[0]) as json_file:
                json_content = json_file.read().decode("utf-8")

        return json.loads(json_content)

    def get_data(self, urls: list = [], years: list = []) -> dict:
        data: dict[str, list] = {"url": [], "api": []}

        # data from urls
        for url in urls:
            logger.info(f"Obtendo dados da url: {url}")

            url_data = self.data_from_url(url=url)
            logger.info(f"Foram obtidos {len(url_data.get('dados'))} registros de despesas")
            data["url"].extend(url_data.get("dados"))

        # data from API
        deputados = self.get_deputados()
        deputados_ids = [i.get("id") for i in deputados.get("dados")]
        deputados_ids = deputados_ids[:1]  # limitar se quiser testar

        for year in years:
            for deputado in deputados_ids:
                logger.info(f"Obtendo dados da API do ano: {year} para o deputado: {deputado}")

                api_data = self.data_from_api(id=deputado, year=year)
                logger.info(f"Foram obtidos {len(api_data.get('dados'))} registros de despesas")
                data["api"].extend(api_data.get("dados"))

        logger.info(f"Quantidade total de registros das urls: {len(data.get('url'))}")
        logger.info(f"Quantidade total de registros da API: {len(data.get('api'))}")

        return data
