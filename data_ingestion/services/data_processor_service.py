from typing import Any


class DataProcessorService:
    def __init__(self, data: dict, deputados: list) -> None:
        self.data = data
        self.deputados_raw = deputados

    def process_deputados(self) -> list[dict[str, Any]]:
        return [
            {
                "id": dep.get("id"),
                "uri": dep.get("uri"),
                "nome": dep.get("nome"),
                "sigla_partido": dep.get("siglaPartido"),
                "uri_partido": dep.get("uriPartido"),
                "sigla_uf": dep.get("siglaUf"),
                "id_legislatura": dep.get("idLegislatura"),
                "url_foto": dep.get("urlFoto"),
                "email": dep.get("email"),
                "fonte": "api",
            }
            for dep in self.deputados_raw
        ]

    def process_url(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        despesas = []
        fornecedores = []

        for item in self.data.get("url", []):
            despesas.append(
                {
                    "ano": item.get("ano"),
                    "mes": item.get("mes"),
                    "tipoDespesa": item.get("descricao"),
                    "codDocumento": item.get("idDocumento"),
                    "tipoDocumento": item.get("tipoDocumento"),
                    "codTipoDocumento": item.get(""),
                    "dataDocumento": item.get("dataEmissao"),
                    "numDocumento": item.get(""),
                    "valorDocumento": item.get("valorDocumento"),
                    "urlDocumento": item.get("urlDocumento"),
                    "nomeFornecedor": item.get("fornecedor"),
                    "cnpjCpfFornecedor": item.get("cnpjCPF"),
                    "valorLiquido": item.get("valorLiquido"),
                    "valorGlosa": item.get("valorGlosa"),
                    "numRessarcimento": item.get("ressarcimento"),
                    "codLote": item.get("lote"),
                    "parcela": item.get("parcela"),
                    "fonte": "url",
                },
            )

            fornecedores.append({
                "nomeFornecedor": item.get("fornecedor"),
                "cnpjCpfFornecedor": item.get("cnpjCPF"),
                "fonte": "url",
            })

        return despesas, fornecedores

    def process_api(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        despesas = []
        fornecedores = []

        for item in self.data.get("api", []):
            despesas.append(
                {
                    "ano": item.get("ano"),
                    "mes": item.get("mes"),
                    "tipoDespesa": item.get("tipoDespesa"),
                    "codDocumento": item.get("codDocumento"),
                    "tipoDocumento": item.get("tipoDocumento"),
                    "codTipoDocumento": item.get("codTipoDocumento"),
                    "dataDocumento": item.get("dataDocumento"),
                    "numDocumento": item.get("numDocumento"),
                    "valorDocumento": item.get("valorDocumento"),
                    "urlDocumento": item.get("urlDocumento"),
                    "nomeFornecedor": item.get("nomeFornecedor"),
                    "cnpjCpfFornecedor": item.get("cnpjCpfFornecedor"),
                    "valorLiquido": item.get("valorLiquido"),
                    "valorGlosa": item.get("valorGlosa"),
                    "numRessarcimento": item.get("numRessarcimento"),
                    "codLote": item.get("codLote"),
                    "parcela": item.get("parcela"),
                    "fonte": "api",
                },
            )
            fornecedores.append({
                "nomeFornecedor": item.get("nomeFornecedor"),
                "cnpjCpfFornecedor": item.get("cnpjCpfFornecedor"),
                "fonte": "api",
            })

        return despesas, fornecedores

    def process_data(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        api_despesas, api_fornecedores = self.process_api()
        url_despesas, url_fornecedores = self.process_url()

        despesas = [*api_despesas, *url_despesas]
        fornecedores = [*api_fornecedores, *url_fornecedores]
        deputados = self.process_deputados()

        return despesas, fornecedores, deputados
