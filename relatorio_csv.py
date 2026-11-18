import csv


def celula(valor):
    """Mantém texto com aparência de fórmula como texto em planilhas."""
    if isinstance(valor, str) and valor.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + valor
    return valor


def linhas(relatorio):
    for lacuna in relatorio["lacunas"]:
        inicio, fim = lacuna["inicio"], lacuna["fim"]
        yield relatorio["referencia"], inicio, fim, fim - inicio + 1


def escrever_csv(relatorio, destino):
    escritor = csv.writer(destino, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
    escritor.writerow(('referencia', 'inicio', 'fim', 'versiculos'))
    for linha in linhas(relatorio):
        escritor.writerow([celula(valor) for valor in linha])
