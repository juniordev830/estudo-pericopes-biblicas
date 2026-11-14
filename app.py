'Organize uma passagem em blocos e identifique versículos ainda sem observação.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


def run(data):
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
            "cobertura_percentual": round(100 * len(anotados) / (fim - inicio + 1), 1)}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
