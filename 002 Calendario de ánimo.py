# Generar un calendario de ánimo, donde se registra como te vas sintiendo cada día y se guarda el resultado en un archivo de texto.

import datetime
import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Definir el archivo donde se guardarán los datos
DATA_FILE = "calendario_animo.txt"
# Función para cargar los datos desde el archivo
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}
# Función para guardar los datos en el archivo
def guardar_datos(datos):
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f)
# Función para registrar el ánimo del día
def registrar_animo(fecha, animo):
    datos = cargar_datos()
    datos[fecha] = animo
    guardar_datos(datos)
# Función para graficar el ánimo a lo largo del tiempo
def graficar_animo():
    datos = cargar_datos()
    fechas = []
    animos = []
    for fecha_str, animo in sorted(datos.items()):
        fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        fechas.append(fecha)
        animos.append(animo)
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, animos, marker='o')
    plt.title("Calendario de Ánimo")
    plt.xlabel("Fecha")
    plt.ylabel("Ánimo")
    plt.ylim(0, 10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.show()
# Menú principal
def main():
    while True:
        print("1. Registrar ánimo del día")
        print("2. Graficar ánimo")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            fecha = input("Ingrese la fecha (YYYY-MM-DD) o deje en blanco para hoy: ")
            if not fecha:
                fecha = datetime.date.today().strftime("%Y-%m-%d")
            animo = int(input("Ingrese su ánimo (0-10): "))
            registrar_animo(fecha, animo)
            print("Ánimo registrado.")
        elif opcion == "2":
            graficar_animo()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")
if __name__ == "__main__":
    main()