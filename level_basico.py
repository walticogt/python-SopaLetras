#!/usr/bin/env python3
"""
Ejemplo de nivel básico: Sopa de letras con orientaciones horizontales y verticales.
Tema: Derechos y valores.

Este archivo demuestra cómo usar el generador para crear una sopa simple.
"""

from word_search_generator import WordSearchGenerator
from config import Config


def main():
    """Genera una sopa de letras de nivel básico."""

    # Palabras sobre derechos y valores
    palabras = [
        "IGUALDAD", "RESPETO", "DIVERSIDAD", "EMPATIA", "JUSTICIA",
        "PROTECCION", "EDUCACION", "SALUD", "DIGNIDAD", "INTEGRACION",
        "ACCESIBILIDAD", "PARTICIPACION", "SOLIDARIDAD", "TOLERANCIA",
        "BIENESTAR"
    ]

    print("🎯 Generando sopa de letras - Nivel Básico")
    print(f"📝 Tema: Derechos y Valores")
    print(f"📊 Palabras: {len(palabras)}")
    print(f"🔤 Orientaciones: Horizontal y Vertical")
    print()

    # Crear generador con configuración básica
    generador = WordSearchGenerator(
        palabras=palabras,
        tamaño=18,  # Cuadrícula un poco más grande por las palabras largas
        orientaciones=Config.ORIENTACIONES_BASICO,  # Solo H y V
        alfabeto=Config.ALFABETO_ES,  # Usar alfabeto español
        permitir_inversa=False  # Sin palabras invertidas
    )

    # Generar la sopa
    try:
        print("⏳ Generando...")
        generador.generar()

        # Exportar imagen
        nombre_archivo = 'sopa_de_letras_basico.png'
        generador.exportar_imagen(nombre_archivo)

        # Exportar soluciones
        generador.exportar_solucion('sopa_de_letras_basico_solucion.txt')

        # Mostrar estadísticas
        stats = generador.obtener_estadisticas()
        print("\n✅ ¡Sopa de letras generada exitosamente!")
        print(f"\n📊 Estadísticas:")
        print(f"   • Palabras colocadas: {stats['palabras_colocadas']}/{stats['total_palabras']}")
        print(f"   • Tamaño: {stats['tamaño_cuadricula']}x{stats['tamaño_cuadricula']}")
        print(f"   • Orientaciones usadas: {list(stats['orientaciones_usadas'].keys())}")
        print(f"\n💾 Archivos generados:")
        print(f"   • {nombre_archivo}")
        print(f"   • sopa_de_letras_basico_solucion.txt")

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
