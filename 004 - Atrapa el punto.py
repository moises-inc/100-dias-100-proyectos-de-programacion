import pygame
import random
import time

# --- Configuración Inicial ---
pygame.init()

# Colores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Atrapa al Insecto - Python Edition")

# Reloj para controlar los FPS
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# --- Clase del Insecto ---
class Insect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(WHITE) 
        
        # Dibujamos algo simple dentro para que parezca un bicho
        pygame.draw.circle(self.image, random.choice([RED, GREEN, BLUE]), (20, 20), 15)
        
        self.rect = self.image.get_rect()
        
        # Posición aleatoria dentro de la pantalla (con un margen)
        self.rect.x = random.randrange(50, SCREEN_WIDTH - 50)
        self.rect.y = random.randrange(50, SCREEN_HEIGHT - 50)
        
        # Velocidad aleatoria para que sea más difícil (opcional)
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.choice([-2, -1, 1, 2])

    def update(self):
        # Mover el insecto
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebotar en los bordes
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed_x *= -1
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
            self.speed_y *= -1

# --- Grupos de Sprites ---
all_sprites = pygame.sprite.Group()
insects_group = pygame.sprite.Group()

# Función para generar un nuevo insecto
def spawn_insect():
    insect = Insect()
    all_sprites.add(insect)
    insects_group.add(insect)

# Generar el primer insecto
spawn_insect()

# Variables de juego
score = 0
start_time = time.time()
running = True

# --- Bucle Principal del Juego ---
while running:
    # 1. Manejo de Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Obtener posición del clic
            pos = pygame.mouse.get_pos()
            
            # Verificar si hicimos clic en algún insecto
            # get_sprites_at devuelve una lista de sprites bajo el mouse
            clicked_sprites = [s for s in insects_group if s.rect.collidepoint(pos)]
            
            for insect in clicked_sprites:
                insect.kill() # Eliminar el insecto atrapado
                score += 1
                
                # LA MECÁNICA CLAVE: Por cada uno atrapado, aparecen dos más
                spawn_insect()
                spawn_insect()

    # 2. Actualización de lógica
    all_sprites.update()

    # Calcular tiempo transcurrido
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_str = f"Tiempo: {minutes:02}:{seconds:02}"

    # 3. Dibujado en pantalla
    screen.fill(BLACK) # Limpiar pantalla
    
    all_sprites.draw(screen) # Dibujar insectos

    # Dibujar Interfaz (Score y Tiempo)
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    time_text = font.render(time_str, True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 50))

    # Actualizar la ventana completa
    pygame.display.flip()
    
    # Mantener 60 cuadros por segundo
    clock.tick(60)

pygame.quit()