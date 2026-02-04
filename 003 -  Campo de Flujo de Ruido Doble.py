import pygame
import random
import math
import noise 

# --- CONFIGURACIÓN INICIAL ---
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_PARTICLES = 1500  # Cantidad de puntos (ajústalo según la potencia de tu PC)
BG_COLOR = (0, 0, 0)  # Fondo negro

# --- PARÁMETROS DEL DOBLE RUIDO ---
# Escala: qué tan "zoomed in" está el mapa de ruido. Valores más bajos = curvas más suaves.
NOISE_SCALE = 0.005 
# Velocidad del tiempo: qué tan rápido cambia el patrón de flujo.
TIME_SPEED = 0.003
# Offset Z: La variable que cambia con el tiempo para animar el ruido.
z_off = 0
# Offset para separar las dos capas de ruido (ángulo y velocidad)
SPEED_LAYER_OFFSET = 5000

# --- CLASE PARTÍCULA ---
class Particle:
    def __init__(self):
        # Posición inicial aleatoria en la pantalla
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.max_speed = random.uniform(1.5, 3.0) # Velocidad base variada
        # Color base (cyan/azulado)
        self.base_color = pygame.Color(0, 200, 255)

    def follow_field(self, z_time):
        # --- AQUÍ ESTÁ LA MAGIA DEL DOBLE RUIDO ---

        # RUIDO 1: ÁNGULO (Dirección)
        # Usamos pnoise3 para ruido 3D (x, y, tiempo)
        angle_noise = noise.pnoise3(self.pos.x * NOISE_SCALE, 
                                    self.pos.y * NOISE_SCALE, 
                                    z_time)
        # Mapeamos el ruido (aprox -1 a 1) a un ángulo en radianes (rotación completa)
        angle = angle_noise * math.pi * 4

        # RUIDO 2: VELOCIDAD (Magnitud)
        # Usamos un offset gigante en X e Y para leer una zona "diferente" del ruido
        speed_noise = noise.pnoise3((self.pos.x + SPEED_LAYER_OFFSET) * NOISE_SCALE, 
                                    (self.pos.y + SPEED_LAYER_OFFSET) * NOISE_SCALE, 
                                    z_time)
        # Normalizamos speed_noise para que sea un multiplicador positivo (ej. entre 0.2 y 1.8)
        speed_multiplier = (speed_noise + 1.2) * 0.8
        
        # Creamos el vector de dirección basado en el ángulo
        dir_vector = pygame.Vector2(math.cos(angle), math.sin(angle))
        
        # Aplicamos la fuerza: dirección * velocidad variable
        force = dir_vector * speed_multiplier
        self.apply_force(force)

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        # Limitamos la velocidad máxima para que no se descontrolen
        if self.vel.length() > self.max_speed:
             self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel
        self.acc *= 0 # Reseteamos la aceleración para el siguiente frame

        # Manejo de bordes: si sale por un lado, aparece por el opuesto
        if self.pos.x > WIDTH: self.pos.x = 0
        if self.pos.x < 0: self.pos.x = WIDTH
        if self.pos.y > HEIGHT: self.pos.y = 0
        if self.pos.y < 0: self.pos.y = HEIGHT

    def draw(self, surface):
        # Variamos ligeramente el brillo según la velocidad actual para efecto visual
        current_speed_ratio = self.vel.length() / self.max_speed
        color = self.base_color.lerp((255, 255, 255), current_speed_ratio * 0.5)
        # Dibujamos un pequeño círculo
        pygame.draw.circle(surface, color, (int(self.pos.x), int(self.pos.y)), 1)

# --- SETUP DE PYGAME ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campo de Flujo de Doble Ruido Animado")
clock = pygame.time.Clock()

# Creamos la lista de partículas
particles = [Particle() for _ in range(NUM_PARTICLES)]

# Superficie para el efecto de rastro (fade effect)
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
# Rellenamos con negro semitransparente (el último valor es alpha: 0-255)
# Menor alpha = rastros más largos. Mayor alpha = rastros más cortos.
trail_surface.fill((0, 0, 0, 25)) 


# --- BUCLE PRINCIPAL ---
running = True
while running:
    clock.tick(FPS)

    # 1. Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 2. Lógica de actualización
    # Avanzamos el tiempo para que el patrón de ruido cambie
    z_off += TIME_SPEED

    for p in particles:
        p.follow_field(z_off)
        p.update()

    # 3. Dibujado
    # En lugar de limpiar la pantalla, dibujamos la capa semitransparente
    # Esto es lo que crea las estelas.
    screen.blit(trail_surface, (0, 0))
    
    for p in particles:
        p.draw(screen)

    pygame.display.flip()

pygame.quit()