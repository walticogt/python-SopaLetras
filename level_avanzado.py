#!/usr/bin/env python3
"""
Ejemplo de nivel avanzado: Sopa de letras con todas las orientaciones.
Tema: Harry Potter - hechizos y personajes.

Este archivo demuestra cómo usar el generador con máxima dificultad.
"""

from word_search_generator import WordSearchGenerator
from config import Config


def main():
    """Genera una sopa de letras de nivel avanzado."""

    # Palabras de Harry Potter
    palabras = [
        "HARRY", "HERMIONE", "RON", "DUMBLEDORE", "VOLDEMORT", "SNAPE",
        "EXPELLIARMUS", "LUMOS", "ACCIO", "WINGARDIUM", "EXPECTO",
        "PATRONUM", "CRUCIO", "SECTUMSEMPRA", "BELLATRIX", "DRACO"
    ]

    print("🎯 Generando sopa de letras - Nivel Avanzado")
    print(f"📝 Tema: Harry Potter")
    print(f"📊 Palabras: {len(palabras)}")
    print(f"🔤 Orientaciones: Todas (H, V, D + inversas)")
    print(f"⚠️  Palabras pueden aparecer invertidas aleatoriamente")
    print()

    # Crear generador con configuración avanzada
    generador = WordSearchGenerator(
        palabras=palabras,
        tamaño=15,
        orientaciones=Config.ORIENTACIONES_AVANZADO,  # Todas las direcciones
        alfabeto=Config.ALFABETO_EN,  # Alfabeto inglés
        permitir_inversa=True  # Palabras pueden aparecer al revés
    )

    # Generar la sopa
    try:
        print("⏳ Generando...")
        generador.generar()

        # Exportar imagen
        nombre_archivo = 'sopa_de_letras_avanzado.png'
        generador.exportar_imagen(nombre_archivo)

        # Exportar soluciones
        generador.exportar_solucion('sopa_de_letras_avanzado_solucion.txt')

        # Mostrar estadísticas
        stats = generador.obtener_estadisticas()
        print("\n✅ ¡Sopa de letras generada exitosamente!")
        print(f"\n📊 Estadísticas:")
        print(f"   • Palabras colocadas: {stats['palabras_colocadas']}/{stats['total_palabras']}")
        print(f"   • Tamaño: {stats['tamaño_cuadricula']}x{stats['tamaño_cuadricula']}")
        print(f"   • Palabras invertidas: {stats['palabras_invertidas']}")
        print(f"   • Orientaciones usadas:")
        for orientacion, cantidad in stats['orientaciones_usadas'].items():
            print(f"     - {orientacion}: {cantidad}")
        print(f"\n💾 Archivos generados:")
        print(f"   • {nombre_archivo}")
        print(f"   • sopa_de_letras_avanzado_solucion.txt")

        # Mostrar la imagen
        print("\n🖼️  Mostrando imagen...")
        from PIL import Image
        img = Image.open(nombre_archivo)
        img.show()

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("💡 Intenta aumentar el tamaño de la cuadrícula o reducir palabras.")


if __name__ == "__main__":
    main()
