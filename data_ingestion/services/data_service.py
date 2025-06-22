import io
import json
import re
import zipfile

import httpx
from tqdm import tqdm

from data_ingestion.services.log_service import logger


class DataService:
    def __init__(self) -> None:
        self.api_base_url = "https://dadosabertos.camara.leg.br/api/v2"

    def get_deputados(self) -> list:
        response = httpx.get(f"{self.api_base_url}/deputados")
        data = response.json().get("dados")
        selected_data = [
            {
                "id": i["id"],
                "nome": i["nome"],
                "sigla_partido": i["siglaPartido"],
                "id_legislatura": i["idLegislatura"],
                "sigla_uf": i["siglaUf"],
            }
            for i in data
        ]

        return selected_data

    def get_data_from_api(self, deputados: list[dict], anos: list[int]) -> tuple[list[dict], list[dict]]:
        despesas = []
        fornecedores = []
        for ano in anos:
            logger.info(f"Getting data from API for year {ano}")
            for deputado in tqdm(deputados):
                response = httpx.get(f"{self.api_base_url}/deputados/{deputado['id']}/despesas?ano={ano}")
                despesas_deputado = response.json().get("dados")

                for item in despesas_deputado:
                    despesas.append({
                        "nome_deputado": deputado.get("nome"),
                        "ano": item.get("ano"),
                        "mes": item.get("mes"),
                        "tipo_despesa": item.get("tipoDespesa"),
                        "data_documento": item.get("dataDocumento"),
                        "valor_documento": item.get("valorDocumento"),
                        "cnpj_cpf_fornecedor": re.sub(r"[^0-9]", "", item.get("cnpjCpfFornecedor")),
                        "valor_liquido": item.get("valorLiquido"),
                        "valor_glosa": item.get("valorGlosa"),
                        "fonte": "api",
                    })

                    fornecedores.append({
                        "nome_fornecedor": item.get("nomeFornecedor"),
                        "cnpj_cpf_fornecedor": re.sub(r"[^0-9]", "", item.get("cnpjCpfFornecedor")),
                        "fonte": "api",
                    })

        logger.info(f"Total number of despesas: {len(despesas)}")

        return despesas, fornecedores

    @staticmethod
    def get_data_from_url(url: str) -> tuple[list[dict], list[dict]]:
        logger.info(f"Getting data from url: {url}")
        response = httpx.get(url=url)
        zip_content = response.content

        with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
            with zip_file.open(zip_file.namelist()[0]) as json_file:
                json_content = json_file.read().decode("utf-8")
                json_data = json.loads(json_content).get("dados")

        despesas = []
        fornecedores = []

        for item in json_data:
            despesas.append({
                "nome_deputado": item.get("nomeParlamentar"),
                "ano": item.get("ano"),
                "mes": item.get("mes"),
                "tipo_despesa": item.get("descricao"),
                "data_documento": item.get("dataEmissao"),
                "valor_documento": item.get("valorDocumento"),
                "cnpj_cpf_fornecedor": re.sub(r"[^0-9]", "", item.get("cnpjCPF")),
                "valor_liquido": item.get("valorLiquido"),
                "valor_glosa": item.get("valorGlosa"),
                "fonte": "url",
            })

            fornecedores.append({
                "nome_fornecedor": item.get("fornecedor"),
                "cnpj_cpf_fornecedor": re.sub(r"[^0-9]", "", item.get("cnpjCPF")),
                "fonte": "url",
            })

        logger.info(f"Total number of despesas: {len(despesas)}")

        return despesas, fornecedores
