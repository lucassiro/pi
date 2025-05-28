import io
import json
import zipfile

import httpx
from tqdm import tqdm

from data_ingestion.services.log_service import logger


class CamaraAPI:
    def __init__(self) -> None:
        self.api_base_url = "https://dadosabertos.camara.leg.br/api/v2"

    def request(self, endpoint: str) -> dict:
        response = httpx.get(f"{self.api_base_url}/{endpoint}")
        return response.json()

    def get_deputados(self) -> dict:
        return self.request("deputados")

    def data_from_api(self, id_: int, year: int) -> dict:
        return self.request(f"deputados/{id_}/despesas?ano={year}")

    @staticmethod
    def data_from_url(url: str) -> dict[str, list[dict[str, list]]]:
        response = httpx.get(url=url)
        zip_content = response.content

        with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
            with zip_file.open(zip_file.namelist()[0]) as json_file:
                json_content = json_file.read().decode("utf-8")

        return json.loads(json_content)

    def get_data(self, urls: list, years: list) -> tuple[list, dict]:
        data: dict[str, list] = {"url": [], "api": []}

        # data from urls
        logger.info("Getting data from urls")
        for url in tqdm(urls):
            url_data = self.data_from_url(url=url)
            data["url"].extend(url_data["dados"])

        # data from API
        logger.info("Getting data from API")
        deputados = self.get_deputados()
        deputados_ids = [i["id"] for i in deputados["dados"]]
        # deputados_ids = deputados_ids[:10]  # limitar se quiser testar

        for year in years:
            logger.info(f"Getting data from API for year {year}")
            for deputado in tqdm(deputados_ids):
                api_data = self.data_from_api(id_=deputado, year=year)
                data["api"].extend(api_data["dados"])

        logger.info(f"Total number of records from urls: {len(data['url'])}")
        logger.info(f"Total number of records from API: {len(data['api'])}")

        return deputados["dados"], data
