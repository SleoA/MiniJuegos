from pygame import *
from random import *

# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# clase del jugador principal
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.lives = 3  # El jugador tiene 3 vidas
    
    def Update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 5   
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += 5 

    def fire(self):
        bullet_centerx = self.rect.centerx
        bullet_top = self.rect.top
        bullet = Bullet("bullet.png", bullet_centerx, bullet_top, 20, 20, 4)
        bullets.add(bullet)

score = 0
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:  
            self.rect.x = randint(80, 640)          
            self.rect.y = 0
            lost = lost + 1

class MiniEnemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:  
            self.kill()

class BossEnemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = 10  # El jefe necesita 5 disparos para morir
        self.direction = 1  # Dirección de movimiento lateral (1 = derecha, -1 = izquierda)
    
    def update(self):
        # Movimiento vertical más lento
        self.rect.y += self.speed / 2
        
        # Movimiento lateral
        self.rect.x += self.speed * self.direction
        
        # Cambiar dirección si llega a los bordes
        if self.rect.x <= 0 or self.rect.x >= 620:
            self.direction *= -1
            
        # Si sale por abajo, reaparece arriba
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(80, 540)

class ShootingBoss(BossEnemy):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = 50  # Más salud que el primer jefe
        self.shoot_timer = 0
        self.shoot_delay = 90  # Dispara cada 90 frames (aproximadamente 1.5 segundos)
    
    def update(self):
        super().update()  # Mantener el movimiento del jefe normal
        
        # Lógica de disparo
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_mini_enemy()
            self.shoot_timer = 0
    
    def shoot_mini_enemy(self):
        # Crear mini enemigos desde diferentes posiciones del jefe
        mini1 = MiniEnemy("ufo.png", self.rect.left + 10, self.rect.bottom, 40, 25, 2)  # Velocidad reducida
        mini2 = MiniEnemy("ufo.png", self.rect.centerx - 20, self.rect.bottom, 40, 25, 2)  # Velocidad reducida
        mini3 = MiniEnemy("ufo.png", self.rect.right - 50, self.rect.bottom, 40, 25, 2)  # Velocidad reducida
        mini_enemies.add(mini1)
        mini_enemies.add(mini2)
        mini_enemies.add(mini3)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:  
            self.kill()     
       

window = display.set_mode((700, 500))
display.set_caption("Tirador")
#establecer fondo de la escena
background = transform.scale(image.load("galaxy.jpg"), (700,500))
font.init()
font2 = font.Font(None, 36)
font3 = font.Font(None, 50)
font1 = font.Font(None, 80)
win = font1.render('GANASTE', True, (255, 255, 255))
lose = font1.render('PERDISTE', True, (180, 0, 0))

f1 = Player('rocket.png', 5, 400, 50, 70, 10)

# Cargar imagen pequeña para las vidas
life_image = transform.scale(image.load('rocket.png'), (30, 40))

mixer.init()
mixer.music.load('spacesound.mp3')
mixer.music.play()

game = True
finish = False
clock = time.Clock()
FPS = 60

# Variables para los jefes
boss_spawned = False
boss_defeated = False
shooting_boss_spawned = False
shooting_boss_defeated = False

enemies = sprite.Group()
bosses = sprite.Group()  # Grupo para el primer jefe
shooting_bosses = sprite.Group()  # Grupo para el segundo jefe que dispara
mini_enemies = sprite.Group()  # Grupo para los mini enemigos

for i in range(1,6):
    enemy = Enemy("ufo.png", randint(80, 640), -40, 80, 50, randint(1, 2))  # Velocidad reducida: entre 1 y 2
    enemies.add(enemy)

bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                f1.fire()
               
    if not finish:    
        window.blit(background, (0,0))

        # Spawnear primer jefe cuando el score llega a 100
        if score >= 100 and not boss_spawned and not boss_defeated:
            boss = BossEnemy("ufo.png", 300, -150, 240, 150, 1)  # Velocidad reducida
            bosses.add(boss)
            boss_spawned = True

        # Spawnear segundo jefe (que dispara) cuando el score llega a 500
        if score >= 500 and not shooting_boss_spawned and not shooting_boss_defeated:
            shooting_boss = ShootingBoss("ufo.png", 250, -200, 280, 180, 0.5)  # Velocidad reducida
            shooting_bosses.add(shooting_boss)
            shooting_boss_spawned = True

        # Colisiones con enemigos normales
        collides = sprite.groupcollide(enemies,bullets, True, True)
        for c in collides:
            enemy = Enemy("ufo.png", randint(80, 640), -40, 80, 50, randint(1, 2))  # Velocidad reducida: entre 1 y 2
            enemies.add(enemy)
            score += 1

        # Colisiones con mini enemigos
        mini_collides = sprite.groupcollide(mini_enemies, bullets, True, True)
        for c in mini_collides:
            score += 2  # Bonus por mini enemigos

        # Colisiones con el primer jefe
        boss_collides = sprite.groupcollide(bosses, bullets, False, True)
        for boss, bullet_list in boss_collides.items():
            boss.health -= len(bullet_list)
            if boss.health <= 0:
                boss.kill()
                boss_spawned = False
                boss_defeated = True
                score += 10  # Bonus por matar al primer jefe

        # Colisiones con el segundo jefe (que dispara)
        shooting_boss_collides = sprite.groupcollide(shooting_bosses, bullets, False, True)
        for boss, bullet_list in shooting_boss_collides.items():
            boss.health -= len(bullet_list)
            if boss.health <= 0:
                boss.kill()
                shooting_boss_spawned = False
                shooting_boss_defeated = True
                score += 20  # Bonus mayor por matar al segundo jefe

        # Detectar colisiones con el jugador y restar vidas
        if sprite.spritecollide(f1, enemies, True) or sprite.spritecollide(f1, bosses, False) or sprite.spritecollide(f1, shooting_bosses, False) or sprite.spritecollide(f1, mini_enemies, True):
            f1.lives -= 1
            # Reponer enemigo normal si fue destruido por colisión
            if len(enemies) < 5:
                enemy = Enemy("ufo.png", randint(80, 640), -40, 80, 50, randint(1, 2))  # Velocidad reducida
                enemies.add(enemy)

        # Condiciones de derrota
        if f1.lives <= 0 or lost >= 5:
            finish = True
            window.blit(lose, (200,200))
            window.blit(puntaje1, (160,250))

        text = font2.render("Puntaje: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))

        puntaje1 = font3.render("Tu puntaje final fue: " + str(score), True, (255, 255, 255))

        text = font2.render("Fallados: " + str(lost), 1, (255, 255, 255))
        window.blit(text, (10,50))
        
        # Mostrar vidas como imágenes en la esquina superior derecha
        for i in range(f1.lives):
            window.blit(life_image, (650 - i * 40, 10))  # Se dibujan de derecha a izquierda
        
        # Mostrar salud de los jefes si existen
        if boss_spawned and len(bosses) > 0:
            boss = list(bosses)[0]
            health_text = font2.render("Jefe 1: " + str(boss.health) + "/10", 1, (255, 0, 0))
            window.blit(health_text, (500, 20))
        
        if shooting_boss_spawned and len(shooting_bosses) > 0:
            boss = list(shooting_bosses)[0]
            health_text = font2.render("Jefe 2: " + str(boss.health) + "/50", 1, (255, 100, 100))
            window.blit(health_text, (500, 50))
        
        f1.reset()
        f1.Update()

        enemies.update()
        enemies.draw(window)

        bosses.update()
        bosses.draw(window)

        shooting_bosses.update()
        shooting_bosses.draw(window)

        mini_enemies.update()
        mini_enemies.draw(window)

        bullets.update()
        bullets.draw(window)

        clock.tick(FPS)
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        # Reiniciar variables
        boss_spawned = False
        boss_defeated = False
        shooting_boss_spawned = False
        shooting_boss_defeated = False
        f1.lives = 3  # Reiniciar vidas
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()
        for boss in bosses:
            boss.kill()
        for boss in shooting_bosses:
            boss.kill()
        for mini in mini_enemies:
            mini.kill()

        time.delay(3000)
        for i in range(1,6):
            enemy = Enemy("ufo.png", randint(80, 640), -40, 80, 50, randint(1, 2))  # Velocidad reducida: entre 1 y 2
            enemies.add(enemy)