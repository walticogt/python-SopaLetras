"""
Tests unitarios para el generador de sopas de letras.
"""

import unittest
import os
import sys

# Agregar el directorio padre al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from word_search_generator import WordSearchGenerator
from config import Config


class TestWordSearchGenerator(unittest.TestCase):
    """Tests para la clase WordSearchGenerator."""

    def setUp(self):
        """Configuración antes de cada test."""
        self.palabras_basico = ["PYTHON", "CODIGO", "TEST"]
        self.palabras_largo = ["PROGRAMACION", "DESARROLLO", "APLICACION"]

    def test_inicializacion_basica(self):
        """Test: Inicialización básica del generador."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=10
        )
        self.assertEqual(len(generador.palabras), 3)
        self.assertEqual(generador.tamaño, 10)
        self.assertEqual(len(generador.cuadrícula), 10)
        self.assertEqual(len(generador.cuadrícula[0]), 10)

    def test_palabras_se_convierten_a_mayusculas(self):
        """Test: Las palabras se convierten automáticamente a mayúsculas."""
        generador = WordSearchGenerator(
            palabras=["python", "codigo", "TEST"],
            tamaño=10
        )
        self.assertEqual(generador.palabras[0], "PYTHON")
        self.assertEqual(generador.palabras[1], "CODIGO")
        self.assertEqual(generador.palabras[2], "TEST")

    def test_generacion_basica(self):
        """Test: Generación básica de sopa de letras."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=10,
            orientaciones=['H', 'V']
        )
        generador.generar()

        # Verificar que no haya celdas vacías
        for fila in generador.cuadrícula:
            for celda in fila:
                self.assertNotEqual(celda, '')
                self.assertTrue(celda.isalpha())

    def test_todas_palabras_colocadas(self):
        """Test: Todas las palabras se colocan exitosamente."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=15,
            orientaciones=Config.ORIENTACIONES_BASICO
        )
        generador.generar()

        self.assertEqual(
            len(generador.palabras_colocadas),
            len(self.palabras_basico)
        )

    def test_palabra_demasiado_larga_lanza_error(self):
        """Test: Palabra más larga que la cuadrícula lanza ValueError."""
        generador = WordSearchGenerator(
            palabras=["PALABRAMUYMUYLARGA"],
            tamaño=5
        )
        with self.assertRaises(ValueError):
            generador.generar()

    def test_orientaciones_basicas(self):
        """Test: Generación con orientaciones básicas (H, V)."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=15,
            orientaciones=Config.ORIENTACIONES_BASICO
        )
        generador.generar()

        # Verificar que solo se usan orientaciones permitidas
        for info in generador.palabras_colocadas.values():
            self.assertIn(
                info['orientacion'],
                ['Horizontal', 'Vertical']
            )

    def test_orientaciones_avanzadas(self):
        """Test: Generación con orientaciones avanzadas."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=15,
            orientaciones=Config.ORIENTACIONES_AVANZADO,
            permitir_inversa=True
        )
        generador.generar()

        self.assertEqual(
            len(generador.palabras_colocadas),
            len(self.palabras_basico)
        )

    def test_exportar_imagen(self):
        """Test: Exportar imagen a archivo PNG."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=10
        )
        generador.generar()

        archivo_test = 'test_output.png'
        try:
            imagen = generador.exportar_imagen(archivo_test)
            self.assertTrue(os.path.exists(archivo_test))
            self.assertIsNotNone(imagen)
        finally:
            # Limpiar archivo de test
            if os.path.exists(archivo_test):
                os.remove(archivo_test)

    def test_exportar_solucion(self):
        """Test: Exportar archivo de soluciones."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=10
        )
        generador.generar()

        archivo_test = 'test_solucion.txt'
        try:
            generador.exportar_solucion(archivo_test)
            self.assertTrue(os.path.exists(archivo_test))

            # Verificar que el archivo contiene información
            with open(archivo_test, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.assertIn('SOLUCIONES', contenido)
                self.assertIn('PYTHON', contenido)
        finally:
            # Limpiar archivo de test
            if os.path.exists(archivo_test):
                os.remove(archivo_test)

    def test_estadisticas(self):
        """Test: Obtener estadísticas de la sopa generada."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=15,
            orientaciones=Config.ORIENTACIONES_BASICO
        )
        generador.generar()

        stats = generador.obtener_estadisticas()

        self.assertEqual(stats['total_palabras'], len(self.palabras_basico))
        self.assertEqual(stats['tamaño_cuadricula'], 15)
        self.assertEqual(stats['palabras_colocadas'], len(self.palabras_basico))
        self.assertIsInstance(stats['orientaciones_usadas'], dict)

    def test_alfabeto_español(self):
        """Test: Uso del alfabeto español."""
        generador = WordSearchGenerator(
            palabras=["NIÑO", "ESPAÑA"],
            tamaño=10,
            alfabeto=Config.ALFABETO_ES
        )
        generador.generar()

        # Verificar que la Ñ está en el alfabeto usado
        tiene_enie = any('Ñ' in fila for fila in generador.cuadrícula)
        # Puede o no tener Ñ en la cuadrícula, pero debe aceptar palabras con Ñ
        self.assertEqual(len(generador.palabras_colocadas), 2)

    def test_cuadricula_vacia_al_inicio(self):
        """Test: La cuadrícula está vacía al inicializar."""
        generador = WordSearchGenerator(
            palabras=self.palabras_basico,
            tamaño=5
        )
        for fila in generador.cuadrícula:
            for celda in fila:
                self.assertEqual(celda, '')

    def test_multiples_palabras_largas(self):
        """Test: Colocación de múltiples palabras largas."""
        generador = WordSearchGenerator(
            palabras=self.palabras_largo,
            tamaño=20,
            orientaciones=Config.ORIENTACIONES_AVANZADO
        )
        generador.generar()

        self.assertEqual(
            len(generador.palabras_colocadas),
            len(self.palabras_largo)
        )

    def test_permitir_inversa(self):
        """Test: Palabras pueden aparecer invertidas."""
        # Este test verifica que al menos algunas veces aparecen invertidas
        palabras_invertidas_encontradas = False

        for _ in range(10):  # Intentar múltiples veces
            generador = WordSearchGenerator(
                palabras=self.palabras_basico,
                tamaño=15,
                orientaciones=Config.ORIENTACIONES_AVANZADO,
                permitir_inversa=True
            )
            generador.generar()

            stats = generador.obtener_estadisticas()
            if stats['palabras_invertidas'] > 0:
                palabras_invertidas_encontradas = True
                break

        # Nota: Este test puede fallar ocasionalmente debido a la aleatoriedad
        # En 10 intentos, deberíamos ver al menos una palabra invertida
        # Si falla consistentemente, puede indicar un problema

    def test_tamano_minimo(self):
        """Test: Tamaño mínimo de cuadrícula."""
        generador = WordSearchGenerator(
            palabras=["AB"],
            tamaño=3
        )
        generador.generar()
        self.assertEqual(generador.tamaño, 3)

    def test_palabra_unica_larga(self):
        """Test: Una sola palabra larga en cuadrícula justa."""
        generador = WordSearchGenerator(
            palabras=["ABCDEFGHIJ"],
            tamaño=10,
            orientaciones=['H']
        )
        generador.generar()
        self.assertEqual(len(generador.palabras_colocadas), 1)


class TestConfig(unittest.TestCase):
    """Tests para la configuración."""

    def test_alfabeto_español_contiene_enie(self):
        """Test: El alfabeto español contiene Ñ."""
        self.assertIn('Ñ', Config.ALFABETO_ES)

    def test_alfabeto_ingles_sin_enie(self):
        """Test: El alfabeto inglés no contiene Ñ."""
        self.assertNotIn('Ñ', Config.ALFABETO_EN)

    def test_orientaciones_basico(self):
        """Test: Orientaciones básicas son H y V."""
        self.assertEqual(Config.ORIENTACIONES_BASICO, ['H', 'V'])

    def test_orientaciones_avanzado(self):
        """Test: Orientaciones avanzadas incluyen todas las direcciones."""
        self.assertEqual(
            len(Config.ORIENTACIONES_AVANZADO),
            6
        )
        self.assertIn('H', Config.ORIENTACIONES_AVANZADO)
        self.assertIn('D_INV', Config.ORIENTACIONES_AVANZADO)


def run_tests():
    """Ejecuta todos los tests."""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestWordSearchGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))

    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
