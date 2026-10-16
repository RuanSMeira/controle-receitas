import pytest

from controle_receitas.parser import (
    LinhaInvalidaError,
    interpretar_linha,
    ler_arquivo,
    quantidade_parcelas,
)


@pytest.mark.parametrize(
    "parcelas, esperado",
    [("1x3", 3), ("2x5", 4), ("1x1", 1), ("3X6", 4)],
)
def test_quantidade_parcelas(parcelas, esperado):
    assert quantidade_parcelas(parcelas) == esperado


@pytest.mark.parametrize("parcelas", ["", "abc", "5x2", "1x"])
def test_quantidade_parcelas_invalida(parcelas):
    with pytest.raises(LinhaInvalidaError):
        quantidade_parcelas(parcelas)


def test_total_calculado_quando_ausente():
    r = interpretar_linha("5;Cliente Teste;100.00;1x3;;;")
    assert r.total == 300.00
    assert r.pago == ""


def test_total_informado_e_preservado():
    r = interpretar_linha("5;Cliente Teste;100.00;1x3;999.90;obs;OK")
    assert r.total == 999.90
    assert r.pago == "OK"


def test_linha_curta_e_completada():
    r = interpretar_linha("5;Cliente Teste;50.00;1x2")
    assert r.total == 100.00


def test_virgula_decimal():
    assert interpretar_linha("5;Cliente;10,50;1x2;;;").valor_parcela == 10.50


@pytest.mark.parametrize(
    "linha",
    ["abc;Cliente;10;1x2", "40;Cliente;10;1x2", "5;;10;1x2", "5;Cliente;dez;1x2"],
)
def test_linhas_invalidas(linha):
    with pytest.raises(LinhaInvalidaError):
        interpretar_linha(linha)


def test_ler_arquivo_ignora_comentarios_cabecalho_e_reporta_erros(tmp_path):
    txt = tmp_path / "entrada.txt"
    txt.write_text(
        "# comentário\n"
        "dia;cliente;valor_parcela;parcelas;total;observacao;pago\n"
        "\n"
        "5;Ana;100;1x2;;;\n"
        "99;Erro;100;1x2;;;\n",
        encoding="utf-8",
    )
    recebimentos, erros = ler_arquivo(txt)
    assert len(recebimentos) == 1
    assert len(erros) == 1
    assert "Linha 5" in erros[0]
