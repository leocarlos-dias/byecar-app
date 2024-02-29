import requests


class RequestHandler:
    def __init__(self):
        self.base_url: str = "https://veiculos.fipe.org.br/api/veiculos/"
        self.payload: tPayload = {
            "codigoTabelaReferencia": "",
            "codigoMarca": "",
            "codigoModelo": "",
            "codigoTipoVeiculo": 1,
            "anoModelo": "",
            "codigoTipoCombustivel": "",
            "tipoVeiculo": "carro",
            "modeloCodigoExterno": "",
            "tipoConsulta": "tradicional",
        }

    def make_request(self, endpoint: str):
        try:
            response = requests.post(f"{self.base_url}{endpoint}", params=self.payload)
            if response.status_code != 200:
                raise Exception(f"Erro {response.status_code}")
            data = response.json()
            if "erro" in data:
                raise Exception(data["erro"])
            return data
        except requests.exceptions.RequestException as e:
            return str(e)
