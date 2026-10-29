import unittest

from fatura import calcular_fatura


class TestFatura(unittest.TestCase):
    def test_bandeira_verde(self):
        self.assertEqual(calcular_fatura(100), 95.0)

    def test_bandeira_amarela_e_por_kwh(self):
        self.assertEqual(calcular_fatura(100, "amarela"), 97.0)

    def test_bandeira_vermelha_e_por_kwh(self):
        self.assertEqual(calcular_fatura(200, "vermelha"), 200.0)

    def test_consumo_negativo(self):
        with self.assertRaises(ValueError):
            calcular_fatura(-1)

    def test_bandeira_invalida(self):
        with self.assertRaises(ValueError):
            calcular_fatura(10, "roxa")


if __name__ == "__main__":
    unittest.main()
