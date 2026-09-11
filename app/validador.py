import re

from app.servico_correios import ServicoCorreios


class Validador:
    def validar_cep(self, cep):
        if not isinstance(cep, str):
            raise ValueError("O CEP deve ser um texto.")

        if re.fullmatch(r"\d{5}-\d{3}", cep):
            cep_limpo = cep.replace("-", "")
        elif re.fullmatch(r"\d{8}", cep):
            cep_limpo = cep
        else:
            return False

        if len(set(cep_limpo)) == 1:
            return False

        servico = ServicoCorreios()
        return servico.valida_cep_api(cep_limpo)

    def validar_cpf(self, cpf):
        if not isinstance(cpf, str):
            raise ValueError("O CPF deve ser um texto.")

        if re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
            cpf_limpo = re.sub(r"\D", "", cpf)
        elif re.fullmatch(r"\d{11}", cpf):
            cpf_limpo = cpf
        else:
            return False

        if len(set(cpf_limpo)) == 1:
            return False

        primeiro_digito = self._calcular_digito(cpf_limpo[:9])
        segundo_digito = self._calcular_digito(cpf_limpo[:9] + str(primeiro_digito))

        return cpf_limpo[-2:] == f"{primeiro_digito}{segundo_digito}"

    def validar_cnpj(self, cnpj):
        if not isinstance(cnpj, str):
            raise ValueError("O CNPJ deve ser um texto.")

        if re.fullmatch(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", cnpj):
            cnpj_limpo = re.sub(r"\D", "", cnpj)
        elif re.fullmatch(r"\d{14}", cnpj):
            cnpj_limpo = cnpj
        else:
            return False

        if len(set(cnpj_limpo)) == 1:
            return False

        primeiro_digito = self._calcular_digito_cnpj(cnpj_limpo[:12])
        segundo_digito = self._calcular_digito_cnpj(cnpj_limpo[:12] + str(primeiro_digito))

        return cnpj_limpo[-2:] == f"{primeiro_digito}{segundo_digito}"

    @staticmethod
    def _calcular_digito(numero):
        peso = len(numero) + 1
        total = sum(int(digito) * (peso - indice) for indice, digito in enumerate(numero))
        resto = total % 11
        return 0 if resto < 2 else 11 - resto

    @staticmethod
    def _calcular_digito_cnpj(numero):
        pesos = 9, 8, 7, 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2
        pesos_aplicados = pesos[16 - len(numero):]
        total = sum(int(digito) * peso for digito, peso in zip(numero, pesos_aplicados))
        resto = total % 11
        return 0 if resto < 2 else 11 - resto