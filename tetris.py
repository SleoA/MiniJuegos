from pygame import *
import pygame
import random
def juegotetris():
    pygame.init()

    window = display.set_mode((300, 600))
    display.set_caption("Tetris")

    columnas = 10
    filas = 20
    cuadrito = 30

    grid = [[0 for _ in range(columnas)] for _ in range(filas)]

    class Pieza:
        def __init__(self, x, y, color, forma):
            self.x = x
            self.y = y
            self.color = color
            self.forma = forma

    formas = {
        "O": [(0,0), (1,0), (0,1), (1,1)],
        "I": [(0,0), (0,1), (0,2), (0,3)],
        "T": [(1,0), (0,1), (1,1), (2,1)],
        "L": [(0,0), (0,1), (0,2), (1,2)],
        "J": [(1,0), (1,1), (1,2), (0,2)],
        "S": [(1,0), (2,0), (0,1), (1,1)],
        "Z": [(0,0), (1,0), (1,1), (2,1)]
    }

    def nueva_pieza():
        forma = random.choice(list(formas.values()))
        color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        return Pieza(4, 0, color, forma)

    pieza = nueva_pieza()

    def dibujar_grid():
        for y in range(filas):
            for x in range(columnas):
                if grid[y][x] != 0:
                    draw.rect(window, grid[y][x], (x*cuadrito, y*cuadrito, cuadrito, cuadrito))

    def dibujar_pieza(p):
        for dx, dy in p.forma:
            x_real = (p.x + dx) * cuadrito
            y_real = (p.y + dy) * cuadrito
            draw.rect(window, p.color, (x_real, y_real, cuadrito, cuadrito))

    def colisiona_abajo(p):
        for dx, dy in p.forma:
            nuevo_y = p.y + dy + 1
            if nuevo_y >= filas:
                return True
            if grid[nuevo_y][p.x + dx] != 0:
                return True
        return False

    def colisiona_lados(p):
        for dx, dy in p.forma:
            x = p.x + dx
            if x < 0 or x >= columnas:
                return True
            if grid[p.y + dy][x] != 0:
                return True
        return False

    def pegar_pieza(p):
        for dx, dy in p.forma:
            grid[p.y + dy][p.x + dx] = p.color

    def rotar_forma(forma):
        return [(-dy, dx) for dx, dy in forma]

    def normalizar_forma(forma):
        min_x = min(dx for dx, dy in forma)
        min_y = min(dy for dx, dy in forma)
        return [(dx - min_x, dy - min_y) for dx, dy in forma]

    def colisiona_pared(p, forma_rotada):
        for dx, dy in forma_rotada:
            x = p.x + dx
            y = p.y + dy
            if x < 0 or x >= columnas or y >= filas:
                return True
        return False

    def borrar_lineas():
        for y in range(filas-1, -1, -1):
            if 0 not in grid[y]:
                del grid[y]
                grid.insert(0, [0 for _ in range(columnas)])

    def colision_inicio(pieza):
        for dx, dy in pieza.forma:
            px = pieza.x + dx
            py = pieza.y + dy
            if py < 0:
                continue
            if grid[py][px] != 0:
                return True

        return False


    clock = time.Clock()
    drop_speed = 300
    drop_timer = 0
    game = True

    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False

            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    pieza.x -= 1
                    if colisiona_lados(pieza):
                        pieza.x += 1

                if e.key == K_RIGHT:
                    pieza.x += 1
                    if colisiona_lados(pieza):
                        pieza.x -= 1

                if e.key == K_DOWN:
                    if not colisiona_abajo(pieza):
                        pieza.y += 1

                if e.key == K_UP:
                    nueva = rotar_forma(pieza.forma)
                    nueva = normalizar_forma(nueva)

                    if not colisiona_pared(pieza, nueva):
                        pieza.forma = nueva
                    else:
                        pieza.x -= 1
                        if not colisiona_pared(pieza, nueva):
                            pieza.forma = nueva
                        else:
                            pieza.x += 2
                            if not colisiona_pared(pieza, nueva):
                                pieza.forma = nueva
                            else:
                                pieza.x -= 1  

        #caer
        current_time = pygame.time.get_ticks()
        if current_time - drop_timer > drop_speed:
            if not colisiona_abajo(pieza):
                pieza.y += 1
            else:
                pegar_pieza(pieza)
                borrar_lineas()
                pieza = nueva_pieza()

                if colision_inicio(pieza):
                    game = False

            drop_timer = current_time

        window.fill((0,0,0))
        dibujar_grid()
        dibujar_pieza(pieza)

        clock.tick(60)
        display.update()

juegotetris()