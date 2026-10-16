import pytest

from controle_receitas.models import Recebimento, marcado_como_pago


@pytest.mark.parametrize("texto", ["OK", "ok", " Pago ", "sim", "X"])
def test_marcado_como_pago(texto):
    assert marcado_como_pago(texto)


@pytest.mark.parametrize("texto", ["", "  ", None, "pendente", "nao"])
def test_nao_marcado_como_pago(texto):
    assert not marcado_como_pago(texto)


def test_recebimento_recebido():
    assert Recebimento(1, "Ana", 10.0, "1x1", 10.0, pago="OK").recebido
    assert not Recebimento(1, "Ana", 10.0, "1x1", 10.0).recebido
