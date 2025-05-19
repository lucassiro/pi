from api import CamaraAPI

urls = ["https://www.camara.leg.br/cotas/Ano-2022.json.zip"]
years = [2023, 2024]

api = CamaraAPI()
data = api.get_data(urls=urls, years=years)
