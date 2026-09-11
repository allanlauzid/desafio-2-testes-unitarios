import requests
import re

class ServicoCorreios:
    def valida_cep_api(self, cep):
        """
        Simula validação online (via API) de CEP com os Correios.

        :param cep: String contendo o CEP (com ou sem pontos/traço).
        :return: True se for válido, False caso contrário.
        :raises requests.exceptions.HTTPError: Em caso de erro de comunicação.
        """

        cep_limpo = re.sub(r'\D', '', cep)

        url = f"https://api.ficticia-correios.com.br/v1/ceps/{cep_limpo}"

        resposta = requests.get(url, timeout=5)

        if resposta.status_code == 404:
            return False

        resposta.raise_for_status()

        dados = resposta.json()

        return dados.get("valido", True)