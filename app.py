'Organize uma passagem em blocos e identifique versículos ainda sem observação.'

import argparse
from contextlib import nullcontext
import sys
from relatorio_csv import escrever_csv
import json
from pathlib import Path


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


def agrupar_lacunas(versiculos):
    """Agrupa versículos ordenados e distintos em intervalos inclusivos."""
    intervalos = []
    for versiculo in versiculos:
        if intervalos and versiculo == intervalos[-1]["fim"] + 1:
            intervalos[-1]["fim"] = versiculo
        else:
            intervalos.append({"inicio": versiculo, "fim": versiculo})
    return intervalos


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    if not isinstance(data["blocos"], list) or any(not isinstance(item, dict) for item in data["blocos"]):
        raise ValueError("O campo blocos deve ser uma lista de objetos.")
    inicio, fim = inteiro(data["inicio"], 1), inteiro(data["fim"], 1)
    if fim < inicio or fim - inicio > 200:
        raise ValueError("Informe um intervalo crescente de até 201 versículos.")
    anotados = set()
    for bloco in data["blocos"]:
        primeiro, ultimo = inteiro(bloco["inicio"], 1), inteiro(bloco["fim"], 1)
        if not inicio <= primeiro <= ultimo <= fim:
            raise ValueError("Bloco fora da perícope ou em ordem inversa.")
        texto(bloco["observacao"])
        anotados.update(range(primeiro, ultimo + 1))
    faltam = sorted(set(range(inicio, fim + 1)) - anotados)
    return {"referencia": texto(data["referencia"]), "sem_observacao": faltam,
            "lacunas": agrupar_lacunas(faltam),
            "cobertura_percentual": round(100 * len(anotados) / (fim - inicio + 1), 1)}


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--csv", action="store_true", help="Exportar os intervalos de versículos sem observação em CSV")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open(encoding="utf-8-sig")
        with entrada as source:
            data = json.load(
                source,
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.csv:
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
