import unittest
from app import run
class Diagnostico(unittest.TestCase):
    def test_sobreposicao(self):
        data={"referencia":"Jo 15","inicio":1,"fim":5,"diagnostico":True,"blocos":[{"inicio":1,"fim":3,"observacao":"A"},{"inicio":3,"fim":4,"observacao":"B"}]}
        result=run(data)
        self.assertEqual(result["versiculos_anotados"],[1,2,3,4])
        self.assertEqual(result["sobreposicoes"],[{"versiculo":3,"observacoes":2}])
        self.assertEqual(result["cobertura_percentual"],80.0)
        data["diagnostico"]="sim"
        with self.assertRaises(ValueError): run(data)
