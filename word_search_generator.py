"""
Generador modular de sopas de letras.
Permite crear sopas de letras personalizables con diferentes niveles de dificultad.
"""

import random
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
from config import Config


class WordSearchGenerator:
    """
    Clase principal para generar sopas de letras.

    Attributes:
        palabras: Lista de palabras a incluir en la sopa
        tamaño: Tamaño de la cuadrícula (NxN)
        orientaciones: Lista de orientaciones permitidas
        alfabeto: Alfabeto a usar para relleno
        cuadrícula: Matriz que representa la sopa de letras
        palabras_colocadas: Diccionario con información de palabras colocadas
    """

    def __init__(
        self,
        palabras: List[str],
        tamaño: int = 15,
        orientaciones: Optional[List[str]] = None,
        alfabeto: str = Config.ALFABETO_EN,
        permitir_inversa: bool = False
    ):
        """
        Inicializa el generador de sopa de letras.

        Args:
            palabras: Lista de palabras a incluir
            tamaño: Tamaño de la cuadrícula (por defecto 15x15)
            orientaciones: Orientaciones permitidas (por defecto básico)
            alfabeto: Alfabeto para letras de relleno
            permitir_inversa: Si se permite invertir palabras aleatoriamente
        """
        self.palabras = [p.upper() for p in palabras]
        self.tamaño = tamaño
        self.orientaciones = orientaciones or Config.ORIENTACIONES_BASICO
        self.alfabeto = alfabeto
        self.permitir_inversa = permitir_inversa
        self.cuadrícula = [['' for _ in range(tamaño)] for _ in range(tamaño)]
        self.palabras_colocadas = {}

    def _validar_palabra(self, palabra: str) -> None:
        """
        Valida que una palabra pueda colocarse en la cuadrícula.

        Args:
            palabra: Palabra a validar

        Raises:
            ValueError: Si la palabra es demasiado larga para la cuadrícula
        """
        if len(palabra) > self.tamaño:
            raise ValueError(
                f"La palabra '{palabra}' (longitud {len(palabra)}) "
                f"es demasiado larga para la cuadrícula de tamaño {self.tamaño}"
            )

    def _puede_colocar(
        self, palabra: str, fila: int, col: int, delta_fila: int, delta_col: int
    ) -> bool:
        """
        Verifica si una palabra puede colocarse en una posición específica.

        Args:
            palabra: Palabra a colocar
            fila: Fila inicial
            col: Columna inicial
            delta_fila: Incremento de fila por cada letra
            delta_col: Incremento de columna por cada letra

        Returns:
            True si la palabra puede colocarse, False en caso contrario
        """
        for i in range(len(palabra)):
            r = fila + i * delta_fila
            c = col + i * delta_col
            if self.cuadrícula[r][c] not in ('', palabra[i]):
                return False
        return True

    def _colocar_en_cuadricula(
        self, palabra: str, fila: int, col: int, delta_fila: int, delta_col: int
    ) -> None:
        """
        Coloca una palabra en la cuadrícula.

        Args:
            palabra: Palabra a colocar
            fila: Fila inicial
            col: Columna inicial
            delta_fila: Incremento de fila por cada letra
            delta_col: Incremento de columna por cada letra
        """
        posiciones = []
        for i in range(len(palabra)):
            r = fila + i * delta_fila
            c = col + i * delta_col
            self.cuadrícula[r][c] = palabra[i]
            posiciones.append((r, c))
        return posiciones

    def _colocar_palabra(self, palabra_original: str) -> bool:
        """
        Intenta colocar una palabra en la cuadrícula.

        Args:
            palabra_original: Palabra a colocar

        Returns:
            True si se colocó exitosamente, False en caso contrario

        Raises:
            ValueError: Si no se puede colocar después del máximo de intentos
        """
        self._validar_palabra(palabra_original)

        palabra = palabra_original
        if self.permitir_inversa and random.choice([True, False]):
            palabra = palabra[::-1]

        intentos = 0
        max_intentos = Config.MAX_INTENTOS_COLOCACION

        while intentos < max_intentos:
            intentos += 1
            orientacion = random.choice(self.orientaciones)

            try:
                if orientacion == 'H':  # Horizontal (izquierda a derecha)
                    fila = random.randint(0, self.tamaño - 1)
                    col = random.randint(0, self.tamaño - len(palabra))
                    if self._puede_colocar(palabra, fila, col, 0, 1):
                        posiciones = self._colocar_en_cuadricula(palabra, fila, col, 0, 1)
                        self.palabras_colocadas[palabra_original] = {
                            'posiciones': posiciones,
                            'orientacion': 'Horizontal',
                            'inversa': palabra != palabra_original
                        }
                        return True

                elif orientacion == 'V':  # Vertical (arriba a abajo)
                    fila = random.randint(0, self.tamaño - len(palabra))
                    col = random.randint(0, self.tamaño - 1)
                    if self._puede_colocar(palabra, fila, col, 1, 0):
                        posiciones = self._colocar_en_cuadricula(palabra, fila, col, 1, 0)
                        self.palabras_colocadas[palabra_original] = {
                            'posiciones': posiciones,
                            'orientacion': 'Vertical',
                            'inversa': palabra != palabra_original
                        }
                        return True

                elif orientacion == 'D':  # Diagonal (arriba-izq a abajo-der)
                    fila = random.randint(0, self.tamaño - len(palabra))
                    col = random.randint(0, self.tamaño - len(palabra))
                    if self._puede_colocar(palabra, fila, col, 1, 1):
                        posiciones = self._colocar_en_cuadricula(palabra, fila, col, 1, 1)
                        self.palabras_colocadas[palabra_original] = {
                            'posiciones': posiciones,
                            'orientacion': 'Diagonal',
                            'inversa': palabra != palabra_original
                        }
                        return True

                elif orientacion == 'H_INV':  # Horizontal inversa (derecha a izquierda)
                    fila = random.randint(0, self.tamaño - 1)
                    col = random.randint(len(palabra) - 1, self.tamaño - 1)
                    if self._puede_colocar(palabra, fila, col, 0, -1):
                        posiciones = self._colocar_en_cuadricula(palabra, fila, col, 0, -1)
                        self.palabras_colocadas[palabra_original] = {
                            'posiciones': posiciones,
                            'orientacion': 'Horizontal Inversa',
                            'inversa': palabra != palabra_original
                        }
                        return True

                elif orientacion == 'V_INV':  # Vertical inversa (abajo a arriba)
                    fila = random.randint(len(palabra) - 1, self.tamaño - 1)
                    col = random.randint(0, self.tamaño - 1)
                    if self._puede_colocar(palabra, fila, col, -1, 0):
                        posiciones = self._colocar_en_cuadricula(palabra, fila, col, -1, 0)
                        self.palabras_colocadas[palabra_original] = {
                            'posiciones': posiciones,
                            'orientacion': 'Vertical Inversa',
                            'inversa': palabra != palabra_original
                        }
                        return True

                elif orientacion == 'D_INV':  # Diagonal inversa (abajo-der a arriba-izq)
                    fila = random.randint(len(palabra) - 1, self.tamaño - 1)
                    col = random.randint(len(palabra) - 1, self.tamaño - 1)
                    if self._puede_colocar(palabra, fila, col, -1, -1):
                        posiciones = self._colocar_en_cuadricula(palabra, fila, col, -1, -1)
                        self.palabras_colocadas[palabra_original] = {
                            'posiciones': posiciones,
                            'orientacion': 'Diagonal Inversa',
                            'inversa': palabra != palabra_original
                        }
                        return True

            except (IndexError, ValueError):
                continue

        raise ValueError(
            f"No se pudo colocar la palabra '{palabra_original}' después de "
            f"{max_intentos} intentos. Considera aumentar el tamaño de la cuadrícula."
        )

    def generar(self) -> None:
        """
        Genera la sopa de letras completa.

        Coloca todas las palabras y rellena espacios vacíos con letras aleatorias.
        """
        # Colocar todas las palabras
        for palabra in self.palabras:
            self._colocar_palabra(palabra)

        # Rellenar espacios vacíos con letras aleatorias
        for fila in range(self.tamaño):
            for col in range(self.tamaño):
                if self.cuadrícula[fila][col] == '':
                    self.cuadrícula[fila][col] = random.choice(self.alfabeto)

    def exportar_imagen(
        self,
        nombre_archivo: str,
        mostrar_palabras: bool = True,
        imagen_tamaño: int = Config.IMAGEN_TAMAÑO,
        color_fondo: str = Config.COLOR_FONDO,
        color_lineas: str = Config.COLOR_LINEAS,
        color_texto: str = Config.COLOR_TEXTO
    ) -> Image.Image:
        """
        Exporta la sopa de letras como una imagen.

        Args:
            nombre_archivo: Ruta donde guardar la imagen
            mostrar_palabras: Si se debe mostrar la lista de palabras
            imagen_tamaño: Tamaño de la imagen en píxeles
            color_fondo: Color de fondo
            color_lineas: Color de las líneas de la cuadrícula
            color_texto: Color del texto

        Returns:
            Objeto Image de PIL con la sopa de letras generada
        """
        cell_size = imagen_tamaño // self.tamaño
        altura_extra = Config.IMAGEN_EXTRA_ALTURA if mostrar_palabras else 0
        imagen = Image.new(
            'RGB',
            (imagen_tamaño, imagen_tamaño + altura_extra),
            color_fondo
        )
        draw = ImageDraw.Draw(imagen)
        font = ImageFont.load_default()

        # Dibujar cuadrícula
        for i in range(self.tamaño + 1):
            # Líneas horizontales
            draw.line(
                [(0, i * cell_size), (imagen_tamaño, i * cell_size)],
                fill=color_lineas
            )
            # Líneas verticales
            draw.line(
                [(i * cell_size, 0), (i * cell_size, imagen_tamaño)],
                fill=color_lineas
            )

        # Dibujar letras centradas en cada celda
        for fila in range(self.tamaño):
            for col in range(self.tamaño):
                letra = self.cuadrícula[fila][col]
                bbox = draw.textbbox((0, 0), letra, font=font)
                ancho_letra = bbox[2] - bbox[0]
                alto_letra = bbox[3] - bbox[1]
                x = col * cell_size + (cell_size - ancho_letra) // 2
                y = fila * cell_size + (cell_size - alto_letra) // 2
                draw.text((x, y), letra, font=font, fill=color_texto)

        # Dibujar lista de palabras si se solicita
        if mostrar_palabras:
            palabra_x = Config.MARGEN_PALABRAS_X
            palabra_y = imagen_tamaño + Config.MARGEN_PALABRAS_Y
            for palabra in self.palabras:
                draw.text(
                    (palabra_x, palabra_y),
                    f"{Config.ESPACIADO_CHECKBOX}   {palabra}",
                    font=font,
                    fill=color_texto
                )
                palabra_y += Config.ESPACIADO_ENTRE_PALABRAS
                # Si se sale del espacio, crear nueva columna
                if palabra_y > imagen_tamaño + altura_extra - 20:
                    palabra_y = imagen_tamaño + Config.MARGEN_PALABRAS_Y
                    palabra_x += Config.ANCHO_COLUMNA_PALABRAS

        # Guardar imagen
        imagen.save(nombre_archivo)
        return imagen

    def exportar_solucion(self, nombre_archivo: str) -> None:
        """
        Exporta un archivo de texto con las soluciones (posiciones de palabras).

        Args:
            nombre_archivo: Ruta donde guardar el archivo de soluciones
        """
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("SOLUCIONES - SOPA DE LETRAS\n")
            f.write("=" * 60 + "\n\n")

            for palabra, info in self.palabras_colocadas.items():
                f.write(f"Palabra: {palabra}\n")
                f.write(f"Orientación: {info['orientacion']}\n")
                if info['inversa']:
                    f.write(f"⚠ Palabra invertida\n")
                f.write(f"Posición inicial: fila {info['posiciones'][0][0]}, "
                       f"columna {info['posiciones'][0][1]}\n")
                f.write(f"Posición final: fila {info['posiciones'][-1][0]}, "
                       f"columna {info['posiciones'][-1][1]}\n")
                f.write("-" * 60 + "\n")

    def imprimir_cuadricula(self) -> None:
        """Imprime la cuadrícula en la consola (útil para debug)."""
        for fila in self.cuadrícula:
            print(' '.join(fila))

    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas sobre la sopa de letras generada.

        Returns:
            Diccionario con estadísticas
        """
        orientaciones_usadas = {}
        palabras_invertidas = 0

        for info in self.palabras_colocadas.values():
            orientacion = info['orientacion']
            orientaciones_usadas[orientacion] = orientaciones_usadas.get(orientacion, 0) + 1
            if info['inversa']:
                palabras_invertidas += 1

        return {
            'total_palabras': len(self.palabras),
            'tamaño_cuadricula': self.tamaño,
            'palabras_colocadas': len(self.palabras_colocadas),
            'orientaciones_usadas': orientaciones_usadas,
            'palabras_invertidas': palabras_invertidas
        }
