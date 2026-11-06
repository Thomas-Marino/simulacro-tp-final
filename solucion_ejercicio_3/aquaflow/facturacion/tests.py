import unittest
from .funcs import calcular_costo_agua

class TestCalculoCosto(unittest.TestCase):
    def test_tarifa_por_defecto(self):
        consumo_m3 = 30
        tarifa_por_defecto = 850

        resultado_esperado = consumo_m3 * tarifa_por_defecto
        self.assertEqual(calcular_costo_agua(consumo_m3), resultado_esperado)

    def test_tarifa_personalizada(self):
        consumo_m3 = 30
        tarifa_personalizada = 350

        resultado_esperado = consumo_m3 * tarifa_personalizada
        
        self.assertEqual(
            calcular_costo_agua(consumo_m3, tarifa_personalizada), 
            resultado_esperado
        )

    def test_caso_limite(self): 
        resultado_esperado = 0

        self.assertEqual(calcular_costo_agua(0, 300000), resultado_esperado)

    def test_decimales(self): 
        resultado_esperado_aproximado = 5.5

        self.assertAlmostEqual(calcular_costo_agua(1.1, 5), resultado_esperado_aproximado)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            calcular_costo_agua(-2000)
        
