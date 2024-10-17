import random
from PIL import Image, ImageDraw, ImageFont

# Configuración de la sopa de letras
palabras = [
    "HARRY", "HERMIONE", "RON", "DUMBLEDORE", "VOLDEMORT", "SNAPE", "EXPELLIARMUS", 
    "LUMOS", "ACCIO", "WINGARDIUM", "EXPECTO", "PATRONUM", "CRUCIO", "SECTUMSEMPRA", 
    "BELLATRIX", "DRACO"
]
tamaño = 15  # Tamaño de la cuadrícula (15x15)

# Crear cuadrícula vacía
cuadrícula = [['' for _ in range(tamaño)] for _ in range(tamaño)]

# Función para colocar palabras en la cuadrícula
def colocar_palabra(palabra):
    orientaciones = ['H', 'V']  # Horizontal, Vertical
    colocada = False
    while not colocada:
        orientacion = random.choice(orientaciones)
        if orientacion == 'H':
            fila = random.randint(0, tamaño - 1)
            col = random.randint(0, tamaño - len(palabra))
            if all(cuadrícula[fila][col + i] in ('', palabra[i]) for i in range(len(palabra))):
                for i in range(len(palabra)):
                    cuadrícula[fila][col + i] = palabra[i]
                colocada = True
        elif orientacion == 'V':
            fila = random.randint(0, tamaño - len(palabra))
            col = random.randint(0, tamaño - 1)
            if all(cuadrícula[fila + i][col] in ('', palabra[i]) for i in range(len(palabra))):
                for i in range(len(palabra)):
                    cuadrícula[fila + i][col] = palabra[i]
                colocada = True

# Colocar todas las palabras en la cuadrícula
for palabra in palabras:
    colocar_palabra(palabra)

# Llenar espacios vacíos con letras aleatorias
for fila in range(tamaño):
    for col in range(tamaño):
        if cuadrícula[fila][col] == '':
            cuadrícula[fila][col] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Crear imagen de la sopa de letras
imagen_tamaño = 600
cell_size = imagen_tamaño // tamaño
imagen = Image.new('RGB', (imagen_tamaño, imagen_tamaño + 150), 'white')
draw = ImageDraw.Draw(imagen)
font = ImageFont.load_default()

# Dibujar las líneas horizontales y verticales
for i in range(tamaño + 1):
    # Líneas horizontales
    draw.line([(0, i * cell_size), (imagen_tamaño, i * cell_size)], fill='black')
    # Líneas verticales
    draw.line([(i * cell_size, 0), (i * cell_size, imagen_tamaño)], fill='black')

# Dibujar letras en la cuadrícula, centradas en cada celda
for fila in range(tamaño):
    for col in range(tamaño):
        letra = cuadrícula[fila][col]
        # Usar textbbox para calcular el tamaño del texto
        bbox = draw.textbbox((0, 0), letra, font=font)
        ancho_letra = bbox[2] - bbox[0]
        alto_letra = bbox[3] - bbox[1]
        x = col * cell_size + (cell_size - ancho_letra) // 2  # Centrar horizontalmente
        y = fila * cell_size + (cell_size - alto_letra) // 2  # Centrar verticalmente
        draw.text((x, y), letra, font=font, fill='black')

# Dibujar las palabras debajo de la cuadrícula con [ ]
palabra_x = 10
palabra_y = imagen_tamaño + 10
for palabra in palabras:
    draw.text((palabra_x, palabra_y), f"[    ]  {palabra}", font=font, fill='black')
    palabra_y += 15
    if palabra_y > imagen_tamaño + 120:
        palabra_y = imagen_tamaño + 10
        palabra_x += 200

# Guardar imagen
imagen.save('sopa_de_letras.png')

# Mostrar imagen
imagen.show()
