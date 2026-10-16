# Controle de Receitas

Automação em Python que transforma o TXT de recebimentos do mês em uma planilha Excel formatada, com cálculo automático do total a receber por cliente e resumo por dia.

> Projeto criado a partir de uma necessidade real: o controle mensal de receitas.
>
> **Todos os dados deste repositório são fictícios** e servem apenas para demonstração.

## O que o projeto faz

- Lê um arquivo `.txt` com os dados digitalizados (separados por `;`)
- Valida cada linha (dia, valores, formato das parcelas) e reporta erros sem interromper o processamento
- Calcula o total a receber a partir do intervalo de parcelas (`2x5` = 4 parcelas)
- Gera uma planilha com cabeçalho estilizado, valores em R$, painel congelado e colunas ajustadas
- Cria a aba **Resumo por dia** com, para cada dia: quantidade de recebimentos, **parcelas do mês**, **já recebido**, **falta receber** e **total do parcelado** (com fórmulas `SUM`)
- Considera uma parcela como recebida quando a coluna `pago` contém `OK`, `pago`, `sim`, `s` ou `x`
- Adiciona novos registros a uma planilha já existente, preservando os dados anteriores

## Tecnologias

Python 3.10+ · openpyxl · pathlib · argparse · logging · pytest

## Estrutura

```
controle-receitas/
├── controle_receitas/
│   ├── models.py     # dataclass Recebimento
│   ├── parser.py     # leitura e validação do TXT
│   ├── excel.py      # geração e formatação da planilha
│   └── cli.py        # interface de linha de comando
├── data/             # TXT de exemplo (dados fictícios)
├── exemplos/         # planilha gerada a partir do exemplo
├── tests/            # testes automatizados
└── requirements.txt
```

## Como usar

```bash
pip install -r requirements.txt

python -m controle_receitas data/exemplo_outubro_2026.txt -o saida/receitas.xlsx
```

Saída esperada:

```
11 registros processados
Parcelas do mês: R$ 2,431.14 | Já recebido: R$ 820.50 | Falta receber: R$ 1,610.64
Total do parcelado: R$ 7,873.65
Planilha salva em: saida/receitas.xlsx
```

### Formato do arquivo de entrada

```
dia;cliente;valor_parcela;parcelas;total;observacao;pago
5;Mercearia Boa Vista;150.00;1x3;;;OK
10;João Pereira;75.00;3x6;;;
```

| Campo | Descrição |
|---|---|
| `dia` | Dia do mês do pagamento (1-31) |
| `cliente` | Nome do cliente |
| `valor_parcela` | Valor de cada parcela |
| `parcelas` | Intervalo no formato `INICIOxFIM` |
| `total` | Opcional. Se vazio, é calculado automaticamente |
| `observacao` | Opcional |
| `pago` | Opcional. `OK` quando já recebido |

Linhas em branco, comentários (`#`) e o cabeçalho são ignorados.

## Testes

```bash
pytest
```

## Decisões de projeto

- **Separação de responsabilidades**: leitura/validação, geração do Excel e CLI ficam em módulos independentes, o que facilita testar e evoluir.
- **Tolerância a erros**: uma linha inválida gera um aviso com o número da linha, mas não derruba o processamento das demais.
- **Dados em `dataclass`**: o restante do código trabalha com objetos tipados em vez de listas posicionais.

## Autor

Ruan Meira · [GitHub](https://github.com/RuanSMeira) · [LinkedIn](https://linkedin.com/in/ruanmeira)
