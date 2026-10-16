"""Modelos de dados do projeto."""

from __future__ import annotations

from dataclasses import dataclass


VALORES_PAGO = {"ok", "pago", "sim", "s", "x"}


def marcado_como_pago(texto: object) -> bool:
    """Indica se o campo ``pago`` está marcado (ex.: "OK", "pago", "sim").

    >>> marcado_como_pago("OK")
    True
    >>> marcado_como_pago("")
    False
    """
    return str(texto or "").strip().lower() in VALORES_PAGO


@dataclass(frozen=True)
class Recebimento:
    """Uma linha de recebimento do mês.

    Attributes:
        dia: dia do mês previsto para o pagamento (1-31).
        cliente: nome do cliente.
        valor_parcela: valor de cada parcela, em reais.
        parcelas: intervalo de parcelas a receber no formato "INICIOxFIM" (ex.: "1x3").
        total: valor total a receber (parcela x quantidade de parcelas).
        observacao: texto livre opcional.
        pago: status do pagamento (ex.: "OK"); vazio quando ainda pendente.
    """

    dia: int
    cliente: str
    valor_parcela: float
    parcelas: str
    total: float
    observacao: str = ""
    pago: str = ""

    @property
    def recebido(self) -> bool:
        """True quando a parcela do mês já foi marcada como paga."""
        return marcado_como_pago(self.pago)

    def como_linha(self) -> list:
        """Retorna os valores na ordem das colunas da planilha."""
        return [
            self.dia,
            self.cliente,
            self.valor_parcela,
            self.parcelas,
            self.total,
            self.observacao,
            self.pago,
        ]
