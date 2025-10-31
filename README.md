# 🔤 Generador de Sopas de Letras en Python

Un generador modular, extensible y fácil de usar para crear sopas de letras (word search puzzles) en Python con múltiples niveles de dificultad.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Características

- 🎯 **Múltiples niveles de dificultad**: Básico (H/V), Intermedio (+ Diagonal), Avanzado (todas direcciones + inversas)
- 🌍 **Soporte multiidioma**: Alfabeto español (incluye Ñ) e inglés
- 🎨 **Exportación a PNG**: Genera imágenes listas para imprimir
- 📝 **Archivo de soluciones**: Genera automáticamente las posiciones de cada palabra
- 🔧 **Completamente modular**: Fácil de personalizar y extender
- 💻 **Interfaz de línea de comandos**: Modo interactivo y comandos directos
- 📚 **Temas predefinidos**: Harry Potter, Derechos, Lugares, Animales, Frutas y más
- 🧪 **Tests incluidos**: Asegura calidad del código

## 📋 Requisitos

- Python 3.7 o superior
- Pillow (PIL) para generación de imágenes

## 🚀 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/python-SopaLetras.git
cd python-SopaLetras
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 📖 Uso

### Modo Interactivo (Recomendado para principiantes)

El modo interactivo te guía paso a paso para crear tu sopa de letras:

```bash
python main.py -i
```

### Ejemplos Rápidos con CLI

```bash
# Generar sopa básica con tema predefinido
python main.py -t harry_potter -o mi_sopa.png

# Generar sopa avanzada con palabras personalizadas
python main.py -p "PYTHON,CODIGO,PROGRAMA" -d avanzado -s 20 -o programacion.png

# Listar todos los temas disponibles
python main.py --listar-temas

# Generar sopa en español con alfabeto español
python main.py -t derechos -d basico --alfabeto es -o derechos.png
```

### Usar los Scripts de Ejemplo

El proyecto incluye dos ejemplos listos para ejecutar:

```bash
# Nivel básico (solo horizontal y vertical)
python level_basico.py

# Nivel avanzado (todas las direcciones + palabras invertidas)
python level_avanzado.py
```

### Uso Programático

También puedes usar la clase `WordSearchGenerator` directamente en tu código:

```python
from word_search_generator import WordSearchGenerator
from config import Config

# Crear generador
generador = WordSearchGenerator(
    palabras=["PYTHON", "CODIGO", "PROGRAMA", "DESARROLLO"],
    tamaño=15,
    orientaciones=Config.ORIENTACIONES_BASICO,
    alfabeto=Config.ALFABETO_ES,
    permitir_inversa=False
)

# Generar sopa
generador.generar()

# Exportar imagen
generador.exportar_imagen("mi_sopa.png")

# Exportar soluciones
generador.exportar_solucion("soluciones.txt")

# Obtener estadísticas
stats = generador.obtener_estadisticas()
print(f"Palabras colocadas: {stats['palabras_colocadas']}")
```

## 🎮 Opciones de Línea de Comandos

```
Argumentos principales:
  -i, --interactivo          Modo interactivo (guiado)
  -t, --tema TEMA           Tema predefinido (harry_potter, derechos, lugares, etc.)
  -p, --palabras PALABRAS   Palabras personalizadas separadas por comas
  -d, --dificultad NIVEL    Nivel: basico, intermedio, avanzado (default: basico)
  -s, --size TAMAÑO         Tamaño de la cuadrícula NxN (default: 15)
  -o, --output ARCHIVO      Nombre del archivo de salida (default: sopa_de_letras.png)
  --alfabeto ALFABETO       Alfabeto: es (español) o en (inglés) (default: en)
  --listar-temas           Lista todos los temas disponibles
  --sin-solucion           No genera archivo de soluciones
```

## 🎨 Temas Predefinidos

El generador incluye varios temas predefinidos:

| Tema | Descripción | Palabras |
|------|-------------|----------|
| `harry_potter` | Personajes y hechizos de Harry Potter | 16 |
| `derechos` | Derechos humanos y valores | 15 |
| `lugares` | Ciudades del mundo | 13 |
| `animales` | Animales variados | 12 |
| `frutas` | Frutas comunes | 12 |

Puedes ver todos los temas disponibles con:

```bash
python main.py --listar-temas
```

## 📁 Estructura del Proyecto

```
python-SopaLetras/
├── config.py                    # Configuración global
├── word_search_generator.py    # Clase principal del generador
├── main.py                      # CLI y punto de entrada principal
├── level_basico.py              # Ejemplo de nivel básico
├── level_avanzado.py            # Ejemplo de nivel avanzado
├── requirements.txt             # Dependencias
├── README.md                    # Esta documentación
├── .gitignore                   # Archivos ignorados por git
└── tests/                       # Tests unitarios
    └── test_word_search.py
```

## ⚙️ Configuración

Puedes personalizar el comportamiento editando `config.py`:

```python
class Config:
    # Dimensiones de imagen
    IMAGEN_TAMAÑO = 600
    IMAGEN_EXTRA_ALTURA = 150

    # Colores
    COLOR_FONDO = 'white'
    COLOR_LINEAS = 'black'
    COLOR_TEXTO = 'black'

    # Alfabetos
    ALFABETO_ES = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    ALFABETO_EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Orientaciones
    ORIENTACIONES_BASICO = ['H', 'V']
    ORIENTACIONES_AVANZADO = ['H', 'V', 'D', 'H_INV', 'V_INV', 'D_INV']
```

## 🎯 Niveles de Dificultad

### Básico
- Solo orientaciones horizontales (→) y verticales (↓)
- Palabras no invertidas
- Ideal para niños y principiantes

### Intermedio
- Horizontal (→), Vertical (↓) y Diagonal (↘)
- Palabras no invertidas
- Dificultad media

### Avanzado
- Todas las orientaciones: H, V, D y sus inversas (←, ↑, ↖)
- Palabras pueden aparecer invertidas aleatoriamente
- Máxima dificultad

## 🧪 Tests

Ejecutar los tests unitarios:

```bash
python -m pytest tests/
```

O directamente:

```bash
python tests/test_word_search.py
```

## 🎓 Casos de Uso

- 📚 **Educación**: Crear material didáctico para escuelas
- 🎉 **Entretenimiento**: Generar puzzles para fiestas o eventos
- 🧠 **Terapia cognitiva**: Ejercicios de estimulación mental
- 📰 **Publicaciones**: Contenido para revistas o periódicos
- 🎮 **Gamificación**: Integrar en aplicaciones educativas

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Mejoras Futuras

- [ ] Exportar a PDF y SVG
- [ ] Interfaz gráfica (GUI) con Tkinter
- [ ] Generador web con Flask
- [ ] Más opciones de personalización visual
- [ ] Soporte para formas de cuadrícula no cuadradas
- [ ] API REST
- [ ] Búsqueda automática de soluciones (solver)

## 🐛 Reportar Problemas

Si encuentras algún bug o tienes una sugerencia, por favor [abre un issue](https://github.com/tu-usuario/python-SopaLetras/issues).

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ por [Tu Nombre]

## 🙏 Agradecimientos

- Biblioteca Pillow por el manejo de imágenes
- Comunidad Python por las mejores prácticas
- Todos los contribuidores del proyecto

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
