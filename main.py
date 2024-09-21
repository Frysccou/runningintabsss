import pygame
import random
import time
import os

# Inicializa Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la ventana
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dispara a los Globos")

# Cargar imagen de fondo
background_img = pygame.image.load(os.path.join("img", "Background.png"))
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Cargar sonidos
shoot_sound = pygame.mixer.Sound(os.path.join("sonido", "gunsound.wav"))
pop_sound = pygame.mixer.Sound(os.path.join("sonido", "ballonpop.wav"))

# Cargar imágenes de los globos
balloon_images = [pygame.image.load(os.path.join("img", "globos", f"globo{i}.png")) for i in range(1, 8)]

class Balloon:
    def __init__(self, speed):
        self.image = random.choice(balloon_images)
        self.image = pygame.transform.scale(self.image, (65, 65)) 
        self.x = random.randint(0, screen_width - self.image.get_width())
        self.y = screen_height
        self.speed = speed

    def move(self):
        self.y -= self.speed 

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def main():
    clock = pygame.time.Clock()
    score = 0
    level = 1
    level_times = [120, 90, 60]  
    balloons_per_level = [300, 250, 200]  
    balloon_speeds = [3, 5, 7] 
    balloons = []
    level_start_time = time.time()
    balloons_generated = 0

    running = True
    while running:
        screen.blit(background_img, (0, 0))  

        elapsed_time = time.time() - level_start_time

        # Generar globos según el nivel
        if balloons_generated < balloons_per_level[level - 1]:
            if elapsed_time > (level_times[level - 1] / balloons_per_level[level - 1]) * balloons_generated:
                balloon = Balloon(balloon_speeds[level - 1])
                balloons.append(balloon)
                balloons_generated += 1

        # Mueve y dibuja los globos
        for balloon in balloons[:]:
            balloon.move()
            if balloon.y < -50:  
                balloons.remove(balloon)
            else:
                balloon.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for balloon in balloons[:]:
                    if (balloon.x < mouse_x < balloon.x + 50) and (balloon.y < mouse_y < balloon.y + 50):
                        score += 1
                        pop_sound.play()
                        balloons.remove(balloon)
                        shoot_sound.play()

        # Mostrar puntuación y temporizador
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntos: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Mostrar tiempo restante
        time_left = level_times[level - 1] - elapsed_time
        if time_left <= 0:
            level += 1
            if level > len(level_times):
                running = False  
            else:
                level_start_time = time.time()
                balloons.clear()
                balloons_generated = 0

        timer_text = font.render(f"Tiempo restante: {max(0, int(time_left))}", True, (0, 0, 0))
        screen.blit(timer_text, (screen_width // 2, 50))

        pygame.display.flip()
        clock.tick(30)

    # Mensaje final
    screen.fill((255, 255, 255))
    final_text = font.render(f"¡Juego terminado! Puntuación: {score}", True, (0, 0, 0))
    screen.blit(final_text, (screen_width // 4, screen_height // 3))
    pygame.display.flip()

    # Espera reinicio
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

    pygame.quit()

if __name__ == "__main__":
    main()