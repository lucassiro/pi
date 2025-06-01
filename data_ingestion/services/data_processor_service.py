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
                    "tipo_despesa": item.get("descricao"),
                    "cod_documento": item.get("idDocumento"),
                    "tipo_documento": item.get("tipoDocumento"),
                    "cod_tipo_documento": item.get(""),
                    "data_documento": item.get("dataEmissao"),
                    "num_documento": item.get(""),
                    "valor_documento": item.get("valorDocumento"),
                    "url_documento": item.get("urlDocumento"),
                    "nome_fornecedor": item.get("fornecedor"),
                    "cnpj_cpf_fornecedor": item.get("cnpjCPF"),
                    "valor_liquido": item.get("valorLiquido"),
                    "valor_glosa": item.get("valorGlosa"),
                    "num_ressarcimento": item.get("ressarcimento"),
                    "cod_lote": item.get("lote"),
                    "parcela": item.get("parcela"),
                    "fonte": "url",
                },
            )

            fornecedores.append({
                "nome_fornecedor": item.get("fornecedor"),
                "cnpj_cpf_fornecedor": item.get("cnpjCPF"),
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
                    "tipo_despesa": item.get("tipoDespesa"),
                    "cod_documento": item.get("codDocumento"),
                    "tipo_documento": item.get("tipoDocumento"),
                    "cod_tipo_documento": item.get("codTipoDocumento"),
                    "data_documento": item.get("dataDocumento"),
                    "num_documento": item.get("numDocumento"),
                    "valor_documento": item.get("valorDocumento"),
                    "url_documento": item.get("urlDocumento"),
                    "nome_fornecedor": item.get("nomeFornecedor"),
                    "cnpj_cpf_fornecedor": item.get("cnpjCpfFornecedor"),
                    "valor_liquido": item.get("valorLiquido"),
                    "valor_glosa": item.get("valorGlosa"),
                    "num_ressarcimento": item.get("numRessarcimento"),
                    "cod_lote": item.get("codLote"),
                    "parcela": item.get("parcela"),
                    "fonte": "api",
                },
            )
            fornecedores.append({
                "nome_fornecedor": item.get("nomeFornecedor"),
                "cnpj_cpf_fornecedor": item.get("cnpjCpfFornecedor"),
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
