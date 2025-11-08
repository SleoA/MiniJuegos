import pygame
import random
import os
import sys

# Inicializar Pygame
pygame.init()

# Constantes del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 350
FPS = 60
GRAVITY = 1
JUMP_FORCE = -20
GAME_SPEED = 5

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

class Dinosaur:
    """Clase que representa al dinosaurio del juego"""
    
    def __init__(self):
        # Cargar imagen del dinosaurio (puedes reemplazar con tu propia imagen)
        try:
            self.image = pygame.Surface((40, 60))
            self.image.fill(GRAY)  # Dinosaurio gris simple
        except:
            # Fallback si hay problemas con la imagen
            self.image = pygame.Surface((40, 60))
            self.image.fill(GRAY)
        
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.velocity_y = 0
        self.is_jumping = False
        
    def jump(self):
        """Hace que el dinosaurio salte"""
        if not self.is_jumping:
            self.velocity_y = JUMP_FORCE
            self.is_jumping = True
    
    def update(self):
        """Actualiza la posición del dinosaurio"""
        # Aplicar gravedad
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Verificar si está en el suelo
        if self.rect.y >= GROUND_HEIGHT - self.rect.height:
            self.rect.y = GROUND_HEIGHT - self.rect.height
            self.is_jumping = False
            self.velocity_y = 0
    
    def draw(self, screen):
        """Dibuja el dinosaurio en la pantalla"""
        screen.blit(self.image, self.rect)

class Obstacle:
    """Clase que representa los obstáculos (cactus)"""
    
    def __init__(self, x):
        # Cargar imagen del cactus (puedes reemplazar con tu propia imagen)
        try:
            self.image = pygame.Surface((20, 40))
            self.image.fill((0, 150, 0))  # Cactus verde simple
        except:
            # Fallback si hay problemas con la imagen
            self.image = pygame.Surface((20, 40))
            self.image.fill((0, 150, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_HEIGHT - self.rect.height
    
    def update(self, speed):
        """Actualiza la posición del obstáculo"""
        self.rect.x -= speed
    
    def draw(self, screen):
        """Dibuja el obstáculo en la pantalla"""
        screen.blit(self.image, self.rect)
    
    def is_off_screen(self):
        """Verifica si el obstáculo salió de la pantalla"""
        return self.rect.x < -self.rect.width

class Cloud:
    """Clase que representa las nubes decorativas"""
    
    def __init__(self, x, y):
        self.image = pygame.Surface((60, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.uniform(0.5, 1.5)
    
    def update(self):
        """Actualiza la posición de la nube"""
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(50, 150)
    
    def draw(self, screen):
        """Dibuja la nube en la pantalla"""
        screen.blit(self.image, self.rect)

class Game:
    """Clase principal del juego"""
    
    def __init__(self):
        # Configurar la pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dino Chrome - Python")
        
        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()
        
        # Crear objetos del juego
        self.dinosaur = Dinosaur()
        self.obstacles = []
        self.clouds = []
        self.score = 0
        self.game_speed = GAME_SPEED
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        
        # Crear nubes iniciales
        for _ in range(3):
            self.clouds.append(Cloud(
                random.randint(0, SCREEN_WIDTH),
                random.randint(50, 150)
            ))
    
    def handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.game_over:
                        # Reiniciar juego si está game over
                        self.__init__()
                    else:
                        self.dinosaur.jump()
                
                if event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def spawn_obstacle(self):
        """Genera nuevos obstáculos aleatoriamente"""
        if not self.obstacles or self.obstacles[-1].rect.x < SCREEN_WIDTH - 300:
            if random.random() < 0.02:  # 2% de probabilidad cada frame
                self.obstacles.append(Obstacle(SCREEN_WIDTH))
    
    def update(self):
        """Actualiza el estado del juego"""
        if not self.game_over:
            # Actualizar dinosaurio
            self.dinosaur.update()
            
            # Generar obstáculos
            self.spawn_obstacle()
            
            # Actualizar obstáculos
            for obstacle in self.obstacles[:]:
                obstacle.update(self.game_speed)
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
                    self.score += 1
            
            # Actualizar nubes
            for cloud in self.clouds:
                cloud.update()
            
            # Verificar colisiones
            for obstacle in self.obstacles:
                if self.dinosaur.rect.colliderect(obstacle.rect):
                    self.game_over = True
            
            # Aumentar velocidad gradualmente
            if self.score % 100 == 0 and self.score > 0:
                self.game_speed = GAME_SPEED + (self.score // 100) * 0.5
    
    def draw(self):
        """Dibuja todos los elementos del juego"""
        # Fondo blanco
        self.screen.fill(WHITE)
        
        # Dibujar línea del suelo
        pygame.draw.line(self.screen, BLACK, (0, GROUND_HEIGHT), 
                        (SCREEN_WIDTH, GROUND_HEIGHT), 2)
        
        # Dibujar nubes
        for cloud in self.clouds:
            cloud.draw(self.screen)
        
        # Dibujar obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Dibujar dinosaurio
        self.dinosaur.draw(self.screen)
        
        # Dibujar puntuación
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Mostrar mensaje de game over
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press SPACE to restart", True, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def run(self):
        """Bucle principal del juego"""
        running = True
        while running:
            # Manejar eventos
            running = self.handle_events()
            
            # Actualizar juego
            self.update()
            
            # Dibujar todo
            self.draw()
            
            # Controlar FPS
            self.clock.tick(FPS)
        
        # Salir del juego
        pygame.quit()
        sys.exit()

# Función principal
def main():
    """Función principal que inicia el juego"""
    game = Game()
    game.run()

# Ejecutar el juego si este archivo es el principal
if __name__ == "__main__":
    main()