# Generar un código que seleccione aleatoriamente una comida y la imprima en pantalla la receta e información de la misma.

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