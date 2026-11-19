# Estudo de perícopes bíblicas

Organize uma passagem em blocos e identifique versículos ainda sem observação.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Informe a referência, o primeiro e último versículo da perícope e os blocos já observados. Os intervalos são inclusivos. O relatório devolve os versículos sem observação em `sem_observacao`, as lacunas contíguas em `lacunas` e a cobertura percentual. Cada lacuna usa `inicio` e `fim` inclusivos; quando não há lacunas, a lista é vazia. Os blocos sobrepostos são contados uma única vez.

Exemplo de saída para `exemplo.json`:

```json
{
  "referencia": "João 15:1–8",
  "sem_observacao": [4],
  "lacunas": [{"inicio": 4, "fim": 4}],
  "cobertura_percentual": 87.5
}
```

## Fontes e exemplos

Os exemplos incluem referências bíblicas, perguntas e anotações de demonstração. Consulte o texto e o contexto em uma [tradução publicada pela Sociedade Bíblica do Brasil](https://www.sbb.org.br/traducoes-da-biblia). Para aprofundar, o catálogo da [Nova Bíblia de Estudo Almeida](https://www.sbb.org.br/nova-almeida/biblias-de-estudo/biblia-de-estudo-almeida) e o do [Comentário Bíblico Pentecostal do Novo Testamento, CPAD](https://www.cpad.com.br/comentario-biblico-pentecostal-novo-testamento-/p) ajudam a identificar edições. Registre as páginas verificadas na sua própria consulta.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar os intervalos de versículos sem observação. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```
