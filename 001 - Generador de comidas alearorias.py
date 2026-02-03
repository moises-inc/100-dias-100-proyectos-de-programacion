# Generar un código que seleccione aleatoriamente una comida y la imprima en pantalla la receta e información de la misma.

# Opción un poco más "casera", agregando los valores a mano en una lista.

import random
# Lista de comidas con sus recetas e información
comidas = {
    "Spaghetti Carbonara": {
        "receta": "Ingredientes: Spaghetti, huevos, panceta, queso parmesano, pimienta negra.\nInstrucciones: Cocinar el spaghetti. Freír la panceta. Mezclar huevos y queso. Combinar todo y sazonar con pimienta.",
        "informacion": "Calorías: 400 por porción. Tiempo de preparación: 20 minutos."
    },
    "Tacos de Pollo": {
        "receta": "Ingredientes: Tortillas, pollo, lechuga, tomate, queso, salsa.\nInstrucciones: Cocinar el pollo. Calentar las tortillas. Armar los tacos con los ingredientes.",
        "informacion": "Calorías: 300 por porción. Tiempo de preparación: 15 minutos."
    },
    "Ensalada César": {
        "receta": "Ingredientes: Lechuga romana, crutones, queso parmesano, aderezo César.\nInstrucciones: Mezclar todos los ingredientes en un bol y servir.",
        "informacion": "Calorías: 250 por porción. Tiempo de preparación: 10 minutos."
    },
    "Sushi": {
        "receta": "Ingredientes: Arroz para sushi, alga nori, pescado, vegetales.\nInstrucciones: Cocinar el arroz. Colocar el arroz sobre el alga nori. Añadir pescado y vegetales. Enrollar y cortar.",
        "informacion": "Calorías: 200 por porción. Tiempo de preparación: 30 minutos."
    }
}
# Seleccionar una comida aleatoriamente
comida_seleccionada = random.choice(list(comidas.keys()))
# Imprimir la receta e información de la comida seleccionada
print(f"Comida seleccionada: {comida_seleccionada}\n")
print("Receta:")
print(comidas[comida_seleccionada]["receta"])
print("\nInformación:")
print(comidas[comida_seleccionada]["informacion"])

# Opción de API pública: TheMealDB (https://www.themealdb.com/api.php)
import requests

def obtener_receta_aleatoria():
    # URL de la API pública para una receta aleatoria
    url = "https://www.themealdb.com/api/json/v1/1/random.php"

    try:
        response = requests.get(url)
        response.raise_for_status() # Verificar si hubo errores en la petición
        data = response.json()

        # La API devuelve una lista llamada 'meals' con un solo elemento
        receta = data['meals'][0]

        # 1. Imprimir Título y Categoría
        print("="*60)
        print(f"🍽️  RECETA: {receta['strMeal']}")
        print(f"🌍  Cocina: {receta['strArea']} | Categoría: {receta['strCategory']}")
        print("="*60)

        # 2. Imprimir Ingredientes
        # En esta API, los ingredientes y medidas están en claves separadas (strIngredient1, strMeasure1, etc.)
        print("\n🛒 INGREDIENTES:")
        for i in range(1, 21): # La API soporta hasta 20 ingredientes
            ingrediente = receta.get(f"strIngredient{i}")
            medida = receta.get(f"strMeasure{i}")

            # Si el ingrediente existe y no está vacío, lo imprimimos
            if ingrediente and ingrediente.strip():
                print(f" - {medida.strip()} {ingrediente.strip()}")

        # 3. Imprimir Instrucciones
        print("\n👨‍🍳 PASOS A SEGUIR:")
        instrucciones = receta['strInstructions']
        # Hacemos un poco de limpieza básica del texto
        print(instrucciones.replace('. ', '.\n'))

        # 4. Información Extra
        if receta['strYoutube']:
            print(f"\n📺 Video Tutorial: {receta['strYoutube']}")
        
        if receta['strSource']:
            print(f"🔗 Fuente original: {receta['strSource']}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la base de datos: {e}")

if __name__ == "__main__":
    obtener_receta_aleatoria()