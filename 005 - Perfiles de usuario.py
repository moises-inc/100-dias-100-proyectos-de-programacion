import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Configuración de colores (inspirados en el diseño original)
COLOR_FONDO = "#28223f"  # Fondo oscuro general
COLOR_CARD = "#231e39"   # Fondo de la tarjeta
COLOR_TEXTO = "#b3b8cd"  # Texto gris claro
COLOR_ACENTO = "#03bfcb" # Cian/Turquesa
COLOR_BORDE = "#03bfcb"

class ProfileCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Perfil de Usuario - Python")
        self.root.geometry("400x500")
        self.root.configure(bg=COLOR_FONDO)

        # --- Marco Principal (La Tarjeta) ---
        self.card_frame = tk.Frame(root, bg=COLOR_CARD, bd=1, relief="flat")
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

        # --- Elementos de la UI ---
        
        # 1. Etiqueta para la imagen (Avatar)
        self.avatar_label = tk.Label(self.card_frame, bg=COLOR_CARD)
        self.avatar_label.pack(pady=20)

        # 2. Etiqueta para el Nombre
        self.name_label = tk.Label(
            self.card_frame, 
            text="Cargando...", 
            font=("Helvetica", 18, "bold"), 
            bg=COLOR_CARD, 
            fg="white"
        )
        self.name_label.pack()

        # 3. Etiqueta para la ubicación/ciudad
        self.location_label = tk.Label(
            self.card_frame, 
            text="...", 
            font=("Helvetica", 10), 
            bg=COLOR_CARD, 
            fg=COLOR_TEXTO
        )
        self.location_label.pack(pady=5)

        # 4. Sección de Habilidades (Texto simulado)
        self.role_label = tk.Label(
            self.card_frame,
            text="User Interface Designer", # Texto fijo como en el diseño original
            font=("Helvetica", 9),
            bg=COLOR_CARD,
            fg="white"
        )
        self.role_label.pack(pady=10)

        # 5. Botones o Estadísticas (Simulados)
        self.stats_frame = tk.Frame(self.card_frame, bg=COLOR_CARD)
        self.stats_frame.pack(side="bottom", fill="x", pady=20)
        
        # Botón para generar nuevo
        self.btn_new = tk.Button(
            self.card_frame,
            text="Nuevo Perfil",
            command=self.fetch_user_data, # Al hacer clic, llama a la función
            bg=COLOR_ACENTO,
            fg=COLOR_CARD,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2" # Cambia el cursor a manito en Linux/Windows
        )
        self.btn_new.pack(pady=20)

        # Cargar el primer usuario automáticamente
        self.fetch_user_data()

    def fetch_user_data(self):
        """Conecta a la API y actualiza la interfaz"""
        try:
            # Petición a la API (solicitamos nombre, ubicación e imagen)
            url = "https://randomuser.me/api/"
            response = requests.get(url)
            data = response.json()['results'][0]

            # Extraer datos
            first_name = data['name']['first']
            last_name = data['name']['last']
            city = data['location']['city']
            country = data['location']['country']
            img_url = data['picture']['large']

            # Actualizar textos
            self.name_label.config(text=f"{first_name} {last_name}")
            self.location_label.config(text=f"{city}, {country}")

            # Procesar Imagen desde URL
            self.load_image_from_url(img_url)

        except Exception as e:
            print(f"Error: {e}")
            self.name_label.config(text="Error de conexión")

    def load_image_from_url(self, url):
        """Descarga la imagen y la muestra en Tkinter"""
        response = requests.get(url)
        img_data = response.content
        
        # Abrir imagen con PIL
        img = Image.open(BytesIO(img_data))
        
        # Redimensionar
        img = img.resize((120, 120), Image.Resampling.LANCZOS)
        
        # Crear objeto compatible con Tkinter
        photo = ImageTk.PhotoImage(img)
        
        # Asignar a la etiqueta (y guardar referencia para que no se borre)
        self.avatar_label.config(image=photo)
        self.avatar_label.image = photo
        
        # Añadir un borde de color (truco visual usando config del label)
        self.avatar_label.config(highlightbackground=COLOR_ACENTO, highlightthickness=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfileCardApp(root)
    root.mainloop()