"""Interface de linha de comando."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .excel import gerar_planilha
from .parser import ler_arquivo


def _criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="controle-receitas",
        description="Converte o TXT de recebimentos do mês em uma planilha Excel formatada.",
    )
    parser.add_argument("entrada", type=Path, help="arquivo TXT de entrada (separado por ';')")
    parser.add_argument(
        "-o", "--saida",
        type=Path,
        default=Path("saida/receitas.xlsx"),
        help="planilha de saída (padrão: saida/receitas.xlsx)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="exibe logs detalhados")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _criar_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    if not args.entrada.is_file():
        print(f"Arquivo não encontrado: {args.entrada}", file=sys.stderr)
        return 1

    recebimentos, erros = ler_arquivo(args.entrada)
    if not recebimentos:
        print("Nenhum registro válido encontrado.", file=sys.stderr)
        return 1

    destino = gerar_planilha(recebimentos, args.saida)
    parcelas_mes = sum(r.valor_parcela for r in recebimentos)
    recebido = sum(r.valor_parcela for r in recebimentos if r.recebido)
    total = sum(r.total for r in recebimentos)

    print(f"{len(recebimentos)} registros processados")
    print(
        f"Parcelas do mês: R$ {parcelas_mes:,.2f} | "
        f"Já recebido: R$ {recebido:,.2f} | "
        f"Falta receber: R$ {parcelas_mes - recebido:,.2f}"
    )
    print(f"Total do parcelado: R$ {total:,.2f}")
    print(f"Planilha salva em: {destino}")
    if erros:
        print(f"{len(erros)} linha(s) ignorada(s):", file=sys.stderr)
        for erro in erros:
            print(f"  - {erro}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
