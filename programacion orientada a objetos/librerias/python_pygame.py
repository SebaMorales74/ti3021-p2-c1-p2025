import pygame
import random

# =========================
#    CONFIGURACIÓN BASE
# =========================
WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE = "AwfulDay"

# Colores
NEGRO     = ( 20,  20,  20)
BLANCO    = (240, 240, 240)
GRIS      = ( 60,  60,  60)
AZUL      = ( 80, 160, 255)
AZUL_OSC  = ( 40,  90, 180)
ROJO      = (220,  60,  60)
VERDE     = ( 60, 200, 100)
VERDE_OSC = ( 40, 160,  80)
NARANJA   = (255, 160,  60)
MORADO    = (180,  60, 200)
CYAN      = ( 60, 200, 200)
AMARILLO  = (255, 220,  80)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("consolas", 48)
font = pygame.font.SysFont("consolas", 24)


# =========================
#         CLASES
# =========================
class Platform:
    """Plataforma rectangular. Puede ser estática o moverse con velocidad y límites."""
    def __init__(self, x, y, w, h, vx=0, vy=0, min_x=None, max_x=None, min_y=None, max_y=None, color=VERDE_OSC):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx, self.vy = vx, vy
        # límites de movimiento (para invertir dirección al llegar al borde)
        self.min_x, self.max_x = min_x, max_x
        self.min_y, self.max_y = min_y, max_y
        self.color = color
        # Último delta aplicado (para "arrastrar" al jugador si está parado sobre esta plataforma móvil)
        self.last_dx = 0
        self.last_dy = 0

    def update(self):
        self.last_dx, self.last_dy = 0, 0

        if self.vx != 0:
            self.rect.x += self.vx
            self.last_dx = self.vx
            if self.min_x is not None and self.rect.left < self.min_x:
                self.rect.left = self.min_x
                self.vx *= -1
                self.last_dx = 0
            if self.max_x is not None and self.rect.right > self.max_x:
                self.rect.right = self.max_x
                self.vx *= -1
                self.last_dx = 0

        if self.vy != 0:
            self.rect.y += self.vy
            self.last_dy = self.vy
            if self.min_y is not None and self.rect.top < self.min_y:
                self.rect.top = self.min_y
                self.vy *= -1
                self.last_dy = 0
            if self.max_y is not None and self.rect.bottom > self.max_y:
                self.rect.bottom = self.max_y
                self.vy *= -1
                self.last_dy = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)


class Enemy:
    """Enemigo rectangular que patrulla entre un rango horizontal."""
    def __init__(self, x, y, w, h, vx, min_x, max_x, color=ROJO):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = vx
        self.min_x = min_x
        self.max_x = max_x
        self.color = color

    def update(self):
        self.rect.x += self.vx
        if self.rect.left < self.min_x or self.rect.right > self.max_x:
            self.vx *= -1
            # corregimos desbordes
            self.rect.x += self.vx

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)


class PowerUp:
    """Power-up de invencibilidad (3s). Aparece en posiciones predefinidas."""
    def __init__(self, size=20, respawn_ms=6000, active=True):
        self.size = size
        self.rect = pygame.Rect(0, 0, size, size)
        self.active = active
        self.respawn_ms = respawn_ms
        self.next_spawn_at = 0
        self.color = MORADO

    def place_on(self, pos):
        self.rect.center = pos

    def deactivate(self, now_ms):
        self.active = False
        self.next_spawn_at = now_ms + self.respawn_ms

    def maybe_respawn(self, now_ms, spawn_points):
        if not self.active and now_ms >= self.next_spawn_at and spawn_points:
            self.place_on(random.choice(spawn_points))
            self.active = True

    def draw(self, surf):
        if self.active:
            pygame.draw.rect(surf, self.color, self.rect)


class Player:
    """Jugador rectangular con física simple (gravedad + salto) y colisiones con plataformas."""
    def __init__(self, x, y, w=36, h=48):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = AZUL
        self.color_inv = AMARILLO
        self.speed = 5
        self.jump_force = -12
        self.gravity = 0.6
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.standing_on = None

        # Invencibilidad
        self.invincible = False
        self.inv_until = 0  # timestamp en ms

    def set_invincible(self, now_ms, duration_ms=3000):
        self.invincible = True
        self.inv_until = now_ms + duration_ms

    def _move_and_collide_axis(self, dx, dy, platforms):
        # Movimiento eje X
        if dx != 0:
            self.rect.x += dx
            for p in platforms:
                if self.rect.colliderect(p.rect):
                    if dx > 0:
                        self.rect.right = p.rect.left
                    elif dx < 0:
                        self.rect.left = p.rect.right

        # Movimiento eje Y
        self.on_ground = False
        self.standing_on = None
        if dy != 0:
            self.rect.y += dy
            for p in platforms:
                if self.rect.colliderect(p.rect):
                    if dy > 0:  # bajando
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                        self.standing_on = p
                    elif dy < 0:  # subiendo
                        self.rect.top = p.rect.bottom
                        self.vel_y = 0

    def update(self, keys, platforms):
        # Input horizontal
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        # Salto
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_force

        # Gravedad
        self.vel_y += self.gravity
        if self.vel_y > 18:
            self.vel_y = 18

        # Movimiento y colisiones
        self._move_and_collide_axis(self.vel_x, self.vel_y, platforms)

        # Si está parado sobre una plataforma móvil, aplicamos su desplazamiento horizontal
        if self.on_ground and isinstance(self.standing_on, Platform):
            self.rect.x += self.standing_on.last_dx

        # Limites de pantalla (solo por los lados; por abajo puede caerse -> game over)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Actualizar invencibilidad
        now = pygame.time.get_ticks()
        if self.invincible and now >= self.inv_until:
            self.invincible = False

    def draw(self, surf):
        # Blink cuando invencible
        if self.invincible and (pygame.time.get_ticks() // 150) % 2 == 0:
            pygame.draw.rect(surf, self.color_inv, self.rect)
        else:
            pygame.draw.rect(surf, self.invincible and self.color_inv or self.color, self.rect)


# =========================
#     ESCENA / ESTADO
# =========================
STATE_MENU = "menu"
STATE_PLAY = "play"
STATE_GAME_OVER = "game_over"


def build_level():
    """Crea plataformas (estáticas y móviles), enemigos y puntos de power-up."""
    platforms = []

    # Piso
    platforms.append(Platform(0, HEIGHT - 40, WIDTH, 40, color=GRIS))

    # Plataformas estáticas
    platforms.append(Platform(100, 450, 140, 20, color=VERDE_OSC))
    platforms.append(Platform(350, 350, 140, 20, color=VERDE_OSC))
    platforms.append(Platform(600, 250, 140, 20, color=VERDE_OSC))

    # Plataformas móviles
    # Horizontal
    platforms.append(Platform(200, 520, 120, 20, vx=2, min_x=200, max_x=600, color=CYAN))
    # Vertical
    platforms.append(Platform(520, 420, 120, 20, vy=2, min_y=300, max_y=520, color=CYAN))

    # Enemigos
    enemies = []
    # Uno en el piso
    enemies.append(Enemy(60, HEIGHT - 60, 36, 20, vx=3, min_x=40, max_x=WIDTH - 40))
    # Uno patrullando sobre plataforma estática 1
    p1 = platforms[1].rect
    enemies.append(Enemy(p1.x + 10, p1.y - 20, 30, 18, vx=2, min_x=p1.left + 5, max_x=p1.right - 5))
    # Otro en plataforma estática 2
    p2 = platforms[2].rect
    enemies.append(Enemy(p2.x + 10, p2.y - 20, 30, 18, vx=2, min_x=p2.left + 5, max_x=p2.right - 5))

    # Puntos posibles para el power-up (centros sobre plataformas estáticas)
    spawn_points = [
        (p1.centerx, p1.y - 12),
        (p2.centerx, p2.y - 12),
        (platforms[3].rect.centerx, platforms[3].rect.y - 12),  # la tercera estática
        (WIDTH // 2, 280)
    ]

    return platforms, enemies, spawn_points


def reset_game():
    platforms, enemies, spawn_points = build_level()
    player = Player(60, HEIGHT - 400)
    powerup = PowerUp()
    powerup.place_on(random.choice(spawn_points))
    state = STATE_MENU
    start_time_ms = 0
    survival_time_ms = 0
    return {
        "platforms": platforms,
        "enemies": enemies,
        "spawn_points": spawn_points,
        "player": player,
        "powerup": powerup,
        "state": state,
        "start_time_ms": start_time_ms,
        "survival_time_ms": survival_time_ms
    }


# =========================
#         BUCLE
# =========================
game = reset_game()
running = True

while running:
    dt = clock.tick(FPS)
    now_ms = pygame.time.get_ticks()

    # ---------------------
    #    EVENTOS
    # ---------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game["state"] == STATE_MENU:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_RETURN):
                # iniciar juego
                game["state"] = STATE_PLAY
                game["start_time_ms"] = now_ms

        elif game["state"] == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = reset_game()
                elif event.key == pygame.K_ESCAPE:
                    # volver al menú sin reiniciar plataformas enemigas? reiniciamos todo por simplicidad
                    game = reset_game()

    keys = pygame.key.get_pressed()

    # ---------------------
    #      UPDATE
    # ---------------------
    if game["state"] == STATE_PLAY:
        # 1) Actualizamos plataformas (para tener last_dx/last_dy correctos)
        for p in game["platforms"]:
            p.update()

        # 2) Jugador
        game["player"].update(keys, game["platforms"])

        # 3) Enemigos
        for e in game["enemies"]:
            e.update()

        # 4) Power-up
        game["powerup"].maybe_respawn(now_ms, game["spawn_points"])

        # Colisión jugador-powerup
        if game["powerup"].active and game["player"].rect.colliderect(game["powerup"].rect):
            game["player"].set_invincible(now_ms, duration_ms=3000)
            game["powerup"].deactivate(now_ms)

        # 5) Dificultad dinámica suave (enemigos y plataformas un poco más rápidos con el tiempo)
        elapsed_s = max(0, (now_ms - game["start_time_ms"]) / 1000.0)
        diff_factor = 1.0 + min(0.5, elapsed_s / 40.0)  # hasta +50% en ~40s
        for e in game["enemies"]:
            e.vx = (abs(e.vx) / e.vx if e.vx != 0 else 1) * max(1.5, 2.0 * diff_factor)
        # Acelera apenas plataformas móviles
        for p in game["platforms"]:
            if p.vx != 0:
                p.vx = (abs(p.vx) / p.vx) * (2 * diff_factor)
            if p.vy != 0:
                p.vy = (abs(p.vy) / p.vy) * (2 * diff_factor)

        # 6) Colisiones con enemigos (si no es invencible)
        player = game["player"]
        if not player.invincible:
            for e in game["enemies"]:
                if player.rect.colliderect(e.rect):
                    game["state"] = STATE_GAME_OVER
                    game["survival_time_ms"] = now_ms - game["start_time_ms"]
                    break

        # 7) Caída fuera de la pantalla -> game over
        if game["player"].rect.top > HEIGHT:
            game["state"] = STATE_GAME_OVER
            game["survival_time_ms"] = now_ms - game["start_time_ms"]

    # ---------------------
    #       DIBUJO
    # ---------------------
    screen.fill(NEGRO)

    if game["state"] == STATE_MENU:
        title = font_big.render(TITLE, True, BLANCO)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        lines = [
            "PLATAFORMERO con rectángulos (AwfulDay)",
            "Controles: ←/→ o A/D para moverse | Espacio/W/↑ para saltar",
            "Objetivo: sobrevive el mayor tiempo posible.",
            "Evita enemigos rojos. Toma el power-up morado (invencible 3s).",
            "Plataformas cyan se mueven.",
            "Presiona ENTER para comenzar."
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, BLANCO)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 240 + i*30))

    elif game["state"] == STATE_PLAY:
        # Plataformas
        for p in game["platforms"]:
            p.draw(screen)

        # PowerUp
        game["powerup"].draw(screen)

        # Enemigos
        for e in game["enemies"]:
            e.draw(screen)

        # Jugador
        game["player"].draw(screen)

        # HUD: tiempo sobrevivido
        elapsed_ms = now_ms - game["start_time_ms"]
        seconds = elapsed_ms / 1000.0
        hud = font.render(f"Tiempo: {seconds:0.2f}s", True, BLANCO)
        screen.blit(hud, (10, 10))

        # HUD: estado invencible
        if game["player"].invincible:
            remain = max(0, (game["player"].inv_until - now_ms) / 1000.0)
            inv = font.render(f"INVENCIBLE {remain:0.1f}s", True, AMARILLO)
            screen.blit(inv, (10, 40))

    elif game["state"] == STATE_GAME_OVER:
        # Mostrar el último frame del nivel como fondo
        for p in game["platforms"]:
            p.draw(screen)
        for e in game["enemies"]:
            e.draw(screen)
        game["powerup"].draw(screen)
        game["player"].draw(screen)

        # Overlay
        pygame.draw.rect(screen, (0, 0, 0, 160), pygame.Rect(0, 0, WIDTH, HEIGHT))
        over = font_big.render("GAME OVER", True, NARANJA)
        screen.blit(over, (WIDTH//2 - over.get_width()//2, 160))

        seconds = game["survival_time_ms"] / 1000.0
        msg = font.render(f"Sobreviviste: {seconds:0.2f}s", True, BLANCO)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 240))

        tip1 = font.render("Presiona R para reiniciar", True, BLANCO)
        tip2 = font.render("Presiona ESC para volver al menú", True, BLANCO)
        screen.blit(tip1, (WIDTH//2 - tip1.get_width()//2, 300))
        screen.blit(tip2, (WIDTH//2 - tip2.get_width()//2, 330))

    pygame.display.flip()
