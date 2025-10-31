"""
Configuración global para el generador de sopa de letras.
"""


class Config:
    """Configuración por defecto para la generación de sopas de letras."""

    # Dimensiones de la imagen
    IMAGEN_TAMAÑO = 600
    IMAGEN_EXTRA_ALTURA = 150  # Espacio extra para mostrar palabras

    # Colores
    COLOR_FONDO = 'white'
    COLOR_LINEAS = 'black'
    COLOR_TEXTO = 'black'

    # Fuente
    FUENTE_POR_DEFECTO = None  # None usa la fuente por defecto de PIL

    # Alfabeto español (incluye Ñ)
    ALFABETO_ES = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'

    # Alfabeto inglés
    ALFABETO_EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Orientaciones disponibles
    ORIENTACIONES_BASICO = ['H', 'V']  # Horizontal, Vertical
    ORIENTACIONES_AVANZADO = ['H', 'V', 'D', 'H_INV', 'V_INV', 'D_INV']

    # Límites
    MAX_INTENTOS_COLOCACION = 1000

    # Formato de palabras en la lista
    ESPACIADO_CHECKBOX = "[ ]"
    ESPACIADO_ENTRE_PALABRAS = 15
    MARGEN_PALABRAS_X = 10
    MARGEN_PALABRAS_Y = 10
    ANCHO_COLUMNA_PALABRAS = 200
