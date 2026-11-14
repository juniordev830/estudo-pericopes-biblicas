import json
from pathlib import Path
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['sem_observacao'], [4])

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['sem_observacao'], [4])

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})

    def test_sobreposicao_conta_uma_vez(self):
        resultado = run({"referencia":"João 15", "inicio":1, "fim":3,
                         "blocos":[{"inicio":1,"fim":2,"observacao":"a"},
                                   {"inicio":2,"fim":3,"observacao":"b"}]})
        self.assertEqual(resultado["cobertura_percentual"], 100)
