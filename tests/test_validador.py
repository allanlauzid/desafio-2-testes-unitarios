import pytest
import requests

from app.validador import Validador


@pytest.fixture
def validador():
    return Validador()


class TestValidarCEP:
    @pytest.mark.parametrize(
        "cep",
        ["01001000", "01001-000", "52050000", "52050-000"],
    )
    def test_validar_cep_retorna_true_para_cep_valido(self, validador, mocker, cep):
        servico_mock = mocker.patch("app.validador.ServicoCorreios")
        servico_mock.return_value.valida_cep_api.return_value = True

        assert validador.validar_cep(cep) is True
        servico_mock.return_value.valida_cep_api.assert_called_once_with(cep.replace("-", ""))

    @pytest.mark.parametrize(
        "cep",
        ["0100-100", "0100100", "010010000", "abcdefgh", "11111111"],
    )
    def test_validar_cep_retorna_false_para_cep_invalido(self, validador, mocker, cep):
        servico_mock = mocker.patch("app.validador.ServicoCorreios")

        assert validador.validar_cep(cep) is False
        servico_mock.return_value.valida_cep_api.assert_not_called()

    @pytest.mark.parametrize("valor", [1001000, 10010000, None, [], {}])
    def test_validar_cep_levanta_value_error_para_valor_que_nao_e_texto(self, validador, valor):
        with pytest.raises(ValueError):
            validador.validar_cep(valor)

    def test_validar_cep_retorna_false_quando_api_informa_cep_invalido(self, validador, mocker):
        servico_mock = mocker.patch("app.validador.ServicoCorreios")
        servico_mock.return_value.valida_cep_api.return_value = False

        assert validador.validar_cep("01001000") is False
        servico_mock.return_value.valida_cep_api.assert_called_once_with("01001000")

    def test_validar_cep_levanta_httperror_quando_api_falha_na_comunicacao(self, validador, mocker):
        servico_mock = mocker.patch("app.validador.ServicoCorreios")
        servico_mock.return_value.valida_cep_api.side_effect = requests.exceptions.HTTPError

        with pytest.raises(requests.exceptions.HTTPError):
            validador.validar_cep("01001000")


class TestValidarCPF:
    @pytest.mark.parametrize(
        "cpf",
        ["52998224725", "529.982.247-25", "11144477735", "111.444.777-35"],
    )
    def test_validar_cpf_retorna_true_para_cpf_valido(self, validador, cpf):
        assert validador.validar_cpf(cpf) is True

    @pytest.mark.parametrize(
        "cpf",
        ["52998224724", "529.982.247-24", "5299822472", "529982247250", "abc.def.ghi-jk", "11111111111"],
    )
    def test_validar_cpf_retorna_false_para_cpf_invalido(self, validador, cpf):
        assert validador.validar_cpf(cpf) is False

    @pytest.mark.parametrize("valor", [52998224725, None, [], {}])
    def test_validar_cpf_levanta_value_error_para_valor_que_nao_e_texto(self, validador, valor):
        with pytest.raises(ValueError):
            validador.validar_cpf(valor)


class TestValidarCNPJ:
    @pytest.mark.parametrize(
        "cnpj",
        ["11222333000181", "11.222.333/0001-81", "11444777000161", "11.444.777/0001-61"],
    )
    def test_validar_cnpj_retorna_true_para_cnpj_valido(self, validador, cnpj):
        assert validador.validar_cnpj(cnpj) is True

    @pytest.mark.parametrize(
        "cnpj",
        ["11222333000180", "11.222.333/0001-80", "1122233300018", "112223330001811", "abc.def.ghi/jklm-no", "11111111111111"],
    )
    def test_validar_cnpj_retorna_false_para_cnpj_invalido(self, validador, cnpj):
        assert validador.validar_cnpj(cnpj) is False

    @pytest.mark.parametrize("valor", [11222333000181, None, [], {}])
    def test_validar_cnpj_levanta_value_error_para_valor_que_nao_e_texto(self, validador, valor):
        with pytest.raises(ValueError):
            validador.validar_cnpj(valor)