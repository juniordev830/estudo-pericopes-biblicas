import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from app import run


ROOT = Path(__file__).resolve().parent


class LacunasTest(unittest.TestCase):
    def data(self, blocos):
        return {"referencia": "João 15:1–8", "inicio": 1, "fim": 8, "blocos": blocos}

    def test_lacunas_no_inicio_meio_e_fim(self):
        result = run(self.data([
            {"inicio": 2, "fim": 3, "observacao": "a"},
            {"inicio": 6, "fim": 6, "observacao": "b"},
        ]))
        self.assertEqual(result["sem_observacao"], [1, 4, 5, 7, 8])
        self.assertEqual(result["lacunas"], [
            {"inicio": 1, "fim": 1},
            {"inicio": 4, "fim": 5},
            {"inicio": 7, "fim": 8},
        ])
        self.assertEqual(result["cobertura_percentual"], 37.5)

    def test_nenhum_bloco_e_cobertura_total(self):
        vazio = run(self.data([]))
        self.assertEqual(vazio["lacunas"], [{"inicio": 1, "fim": 8}])
        self.assertEqual(vazio["cobertura_percentual"], 0.0)
        completo = run(self.data([{"inicio": 1, "fim": 8, "observacao": "a"}]))
        self.assertEqual(completo["lacunas"], [])
        self.assertEqual(completo["sem_observacao"], [])
        self.assertEqual(completo["cobertura_percentual"], 100.0)

    def test_blocos_sobrepostos_nao_criam_lacuna_falsa(self):
        result = run(self.data([
            {"inicio": 1, "fim": 3, "observacao": "a"},
            {"inicio": 2, "fim": 5, "observacao": "b"},
            {"inicio": 7, "fim": 8, "observacao": "c"},
        ]))
        self.assertEqual(result["lacunas"], [{"inicio": 6, "fim": 6}])

    def test_cli_inclui_lacunas_e_mantem_campos_existentes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "entrada.json"
            path.write_text(json.dumps(self.data([])), encoding="utf-8")
            process = subprocess.run([sys.executable, str(ROOT / "app.py"), str(path)],
                                     capture_output=True, text=True, check=True)
        result = json.loads(process.stdout)
        self.assertEqual(result["lacunas"], [{"inicio": 1, "fim": 8}])
        self.assertEqual(result["sem_observacao"], list(range(1, 9)))


if __name__ == "__main__":
    unittest.main()
