"""Leitura e validação do arquivo TXT de entrada.

Formato esperado (separado por ponto e vírgula):

    dia;cliente;valor_parcela;parcelas;total;observacao;pago

- ``total`` é opcional: se vazio, é calculado a partir de ``parcelas``.
- Linhas em branco e linhas iniciadas por ``#`` são ignoradas.
- A linha de cabeçalho (primeira coluna igual a "dia") também é ignorada.
"""

from __future__ import annotations

import logging
from pathlib import Path

from .models import Recebimento

logger = logging.getLogger(__name__)

SEPARADOR = ";"
TOTAL_COLUNAS = 7


class LinhaInvalidaError(ValueError):
    """Levantada quando uma linha do TXT não pode ser interpretada."""


def quantidade_parcelas(parcelas: str) -> int:
    """Calcula quantas parcelas existem em um intervalo "INICIOxFIM".

    >>> quantidade_parcelas("1x3")
    3
    >>> quantidade_parcelas("2x5")
    4
    """
    try:
        inicio, fim = parcelas.lower().split("x", maxsplit=1)
        quantidade = int(fim) - int(inicio) + 1
    except ValueError as erro:
        raise LinhaInvalidaError(f"parcelas inválidas: {parcelas!r}") from erro

    if quantidade < 1:
        raise LinhaInvalidaError(f"intervalo de parcelas inválido: {parcelas!r}")
    return quantidade


def interpretar_linha(linha: str) -> Recebimento:
    """Converte uma linha do TXT em um :class:`Recebimento`."""
    campos = [campo.strip() for campo in linha.strip().split(SEPARADOR)]
    campos += [""] * (TOTAL_COLUNAS - len(campos))  # garante 7 colunas

    dia, cliente, valor, parcelas, total, observacao, pago = campos[:TOTAL_COLUNAS]

    try:
        dia_int = int(dia)
        valor_parcela = float(valor.replace(",", "."))
    except ValueError as erro:
        raise LinhaInvalidaError(f"valor numérico inválido ({erro})") from erro

    if not 1 <= dia_int <= 31:
        raise LinhaInvalidaError(f"dia fora do intervalo 1-31: {dia_int}")
    if not cliente:
        raise LinhaInvalidaError("cliente não informado")

    if total:
        try:
            total_valor = float(total.replace(",", "."))
        except ValueError as erro:
            raise LinhaInvalidaError(f"total inválido: {total!r}") from erro
    else:
        total_valor = round(valor_parcela * quantidade_parcelas(parcelas), 2)

    return Recebimento(
        dia=dia_int,
        cliente=cliente,
        valor_parcela=valor_parcela,
        parcelas=parcelas,
        total=total_valor,
        observacao=observacao,
        pago=pago,
    )


def _deve_ignorar(linha: str) -> bool:
    texto = linha.strip()
    if not texto or texto.startswith("#"):
        return True
    return texto.split(SEPARADOR, maxsplit=1)[0].strip().lower() == "dia"


def ler_arquivo(caminho: Path) -> tuple[list[Recebimento], list[str]]:
    """Lê o TXT e devolve ``(recebimentos, erros)``.

    Linhas inválidas não interrompem o processamento: são registradas em
    ``erros`` com o número da linha e o motivo.
    """
    recebimentos: list[Recebimento] = []
    erros: list[str] = []

    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            if _deve_ignorar(linha):
                continue
            try:
                recebimentos.append(interpretar_linha(linha))
            except LinhaInvalidaError as erro:
                mensagem = f"Linha {numero}: {linha.strip()!r} -> {erro}"
                logger.warning(mensagem)
                erros.append(mensagem)

    return recebimentos, erros
