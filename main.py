#!/usr/bin/env python3
"""
Programa principal para generar sopas de letras.
Proporciona una interfaz de línea de comandos para crear sopas personalizadas.
"""

import argparse
import sys
from word_search_generator import WordSearchGenerator
from config import Config


# Temas predefinidos de palabras
TEMAS = {
    'harry_potter': [
        "HARRY", "HERMIONE", "RON", "DUMBLEDORE", "VOLDEMORT", "SNAPE",
        "EXPELLIARMUS", "LUMOS", "ACCIO", "WINGARDIUM", "EXPECTO", "PATRONUM",
        "CRUCIO", "SECTUMSEMPRA", "BELLATRIX", "DRACO"
    ],
    'derechos': [
        "IGUALDAD", "RESPETO", "DIVERSIDAD", "EMPATIA", "JUSTICIA", "PROTECCION",
        "EDUCACION", "SALUD", "DIGNIDAD", "INTEGRACION", "ACCESIBILIDAD",
        "PARTICIPACION", "SOLIDARIDAD", "TOLERANCIA", "BIENESTAR"
    ],
    'lugares': [
        "PARIS", "LONDRES", "TOKYO", "ROMA", "BERLIN", "MADRID", "MOSCU",
        "SIDNEY", "CAIRO", "MEXICO", "PEKIN", "AMSTERDAM", "VIENA"
    ],
    'animales': [
        "LEON", "TIGRE", "ELEFANTE", "JIRAFA", "CEBRA", "HIPOPOTAMO",
        "RINOCERONTE", "PANDA", "KOALA", "CANGURO", "AGUILA", "DELFIN"
    ],
    'frutas': [
        "MANZANA", "NARANJA", "PLATANO", "FRESA", "UVA", "SANDIA",
        "MELON", "PERA", "DURAZNO", "MANGO", "PIÑA", "KIWI"
    ]
}


def listar_temas():
    """Muestra los temas disponibles."""
    print("\n📚 Temas disponibles:")
    print("=" * 50)
    for tema, palabras in TEMAS.items():
        print(f"\n🔹 {tema}")
        print(f"   Palabras: {', '.join(palabras[:5])}...")
        print(f"   Total: {len(palabras)} palabras")
    print("=" * 50)


def crear_sopa_interactiva():
    """Modo interactivo para crear una sopa de letras."""
    print("\n" + "=" * 60)
    print("🎮 GENERADOR DE SOPA DE LETRAS - MODO INTERACTIVO")
    print("=" * 60)

    # Elegir tema o palabras personalizadas
    print("\n¿Deseas usar un tema predefinido? (s/n): ", end='')
    usar_tema = input().strip().lower()

    if usar_tema == 's':
        listar_temas()
        print("\nElige un tema: ", end='')
        tema = input().strip().lower()
        if tema not in TEMAS:
            print(f"❌ Tema '{tema}' no encontrado. Usando tema por defecto.")
            tema = 'harry_potter'
        palabras = TEMAS[tema]
        print(f"✓ Tema '{tema}' seleccionado con {len(palabras)} palabras.")
    else:
        print("\nIngresa las palabras separadas por comas: ", end='')
        palabras_input = input().strip()
        palabras = [p.strip() for p in palabras_input.split(',') if p.strip()]
        if not palabras:
            print("❌ No se ingresaron palabras válidas. Usando tema por defecto.")
            palabras = TEMAS['harry_potter']

    # Elegir nivel de dificultad
    print("\n🎯 Nivel de dificultad:")
    print("  1. Básico (solo horizontal y vertical)")
    print("  2. Intermedio (+ diagonal)")
    print("  3. Avanzado (todas las direcciones + palabras invertidas)")
    print("Elige nivel (1/2/3): ", end='')
    nivel = input().strip()

    if nivel == '1':
        orientaciones = Config.ORIENTACIONES_BASICO
        permitir_inversa = False
        nivel_nombre = "basico"
    elif nivel == '2':
        orientaciones = ['H', 'V', 'D']
        permitir_inversa = False
        nivel_nombre = "intermedio"
    else:
        orientaciones = Config.ORIENTACIONES_AVANZADO
        permitir_inversa = True
        nivel_nombre = "avanzado"

    # Tamaño de la cuadrícula
    print("\nTamaño de la cuadrícula (por defecto 15): ", end='')
    tamaño_input = input().strip()
    tamaño = int(tamaño_input) if tamaño_input.isdigit() else 15

    # Elegir alfabeto
    print("\n🔤 Alfabeto:")
    print("  1. Español (incluye Ñ)")
    print("  2. Inglés")
    print("Elige alfabeto (1/2): ", end='')
    alfabeto_choice = input().strip()
    alfabeto = Config.ALFABETO_ES if alfabeto_choice == '1' else Config.ALFABETO_EN

    # Nombre del archivo
    print(f"\nNombre del archivo (por defecto: sopa_de_letras_{nivel_nombre}.png): ", end='')
    nombre_archivo = input().strip()
    if not nombre_archivo:
        nombre_archivo = f"sopa_de_letras_{nivel_nombre}.png"
    elif not nombre_archivo.endswith('.png'):
        nombre_archivo += '.png'

    # Generar sopa
    print("\n⏳ Generando sopa de letras...")
    try:
        generador = WordSearchGenerator(
            palabras=palabras,
            tamaño=tamaño,
            orientaciones=orientaciones,
            alfabeto=alfabeto,
            permitir_inversa=permitir_inversa
        )
        generador.generar()
        generador.exportar_imagen(nombre_archivo)

        # Generar archivo de soluciones
        nombre_solucion = nombre_archivo.replace('.png', '_solucion.txt')
        generador.exportar_solucion(nombre_solucion)

        # Mostrar estadísticas
        stats = generador.obtener_estadisticas()
        print("\n✅ ¡Sopa de letras generada exitosamente!")
        print(f"\n📊 Estadísticas:")
        print(f"   • Palabras colocadas: {stats['palabras_colocadas']}/{stats['total_palabras']}")
        print(f"   • Tamaño de cuadrícula: {stats['tamaño_cuadricula']}x{stats['tamaño_cuadricula']}")
        if stats['palabras_invertidas'] > 0:
            print(f"   • Palabras invertidas: {stats['palabras_invertidas']}")
        print(f"\n💾 Archivos generados:")
        print(f"   • Imagen: {nombre_archivo}")
        print(f"   • Soluciones: {nombre_solucion}")

        # Preguntar si mostrar la imagen
        print("\n¿Deseas mostrar la imagen ahora? (s/n): ", end='')
        mostrar = input().strip().lower()
        if mostrar == 's':
            from PIL import Image
            img = Image.open(nombre_archivo)
            img.show()

    except Exception as e:
        print(f"\n❌ Error al generar la sopa de letras: {e}")
        sys.exit(1)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Generador de Sopas de Letras',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  Modo interactivo:
    python main.py -i

  Generar sopa básica con tema:
    python main.py -t harry_potter -o mi_sopa.png

  Generar sopa avanzada con palabras personalizadas:
    python main.py -p "PYTHON,CODIGO,PROGRAMA" -d avanzado -s 20

  Listar temas disponibles:
    python main.py --listar-temas
        """
    )

    parser.add_argument(
        '-i', '--interactivo',
        action='store_true',
        help='Modo interactivo para crear sopa de letras'
    )

    parser.add_argument(
        '-t', '--tema',
        choices=list(TEMAS.keys()),
        help='Tema predefinido de palabras'
    )

    parser.add_argument(
        '-p', '--palabras',
        type=str,
        help='Palabras personalizadas separadas por comas'
    )

    parser.add_argument(
        '-d', '--dificultad',
        choices=['basico', 'intermedio', 'avanzado'],
        default='basico',
        help='Nivel de dificultad (default: basico)'
    )

    parser.add_argument(
        '-s', '--size',
        type=int,
        default=15,
        help='Tamaño de la cuadrícula (default: 15)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='sopa_de_letras.png',
        help='Nombre del archivo de salida (default: sopa_de_letras.png)'
    )

    parser.add_argument(
        '--alfabeto',
        choices=['es', 'en'],
        default='en',
        help='Alfabeto a usar (default: en)'
    )

    parser.add_argument(
        '--listar-temas',
        action='store_true',
        help='Listar todos los temas disponibles'
    )

    parser.add_argument(
        '--sin-solucion',
        action='store_true',
        help='No generar archivo de soluciones'
    )

    args = parser.parse_args()

    # Listar temas
    if args.listar_temas:
        listar_temas()
        return

    # Modo interactivo
    if args.interactivo:
        crear_sopa_interactiva()
        return

    # Obtener palabras
    if args.palabras:
        palabras = [p.strip() for p in args.palabras.split(',')]
    elif args.tema:
        palabras = TEMAS[args.tema]
    else:
        print("❌ Error: Debes especificar un tema (-t) o palabras personalizadas (-p)")
        print("    O usa el modo interactivo con -i")
        parser.print_help()
        sys.exit(1)

    # Configurar orientaciones según dificultad
    if args.dificultad == 'basico':
        orientaciones = Config.ORIENTACIONES_BASICO
        permitir_inversa = False
    elif args.dificultad == 'intermedio':
        orientaciones = ['H', 'V', 'D']
        permitir_inversa = False
    else:  # avanzado
        orientaciones = Config.ORIENTACIONES_AVANZADO
        permitir_inversa = True

    # Configurar alfabeto
    alfabeto = Config.ALFABETO_ES if args.alfabeto == 'es' else Config.ALFABETO_EN

    # Generar sopa de letras
    print(f"⏳ Generando sopa de letras con {len(palabras)} palabras...")

    try:
        generador = WordSearchGenerator(
            palabras=palabras,
            tamaño=args.size,
            orientaciones=orientaciones,
            alfabeto=alfabeto,
            permitir_inversa=permitir_inversa
        )

        generador.generar()
        generador.exportar_imagen(args.output)

        # Generar soluciones si se solicita
        if not args.sin_solucion:
            nombre_solucion = args.output.replace('.png', '_solucion.txt')
            generador.exportar_solucion(nombre_solucion)
            print(f"✅ Soluciones guardadas en: {nombre_solucion}")

        # Mostrar estadísticas
        stats = generador.obtener_estadisticas()
        print(f"\n✅ ¡Sopa de letras generada exitosamente!")
        print(f"   Archivo: {args.output}")
        print(f"   Palabras: {stats['palabras_colocadas']}/{stats['total_palabras']}")
        print(f"   Tamaño: {stats['tamaño_cuadricula']}x{stats['tamaño_cuadricula']}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
