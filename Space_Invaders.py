import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
ALIEN_SPEED = 2
ALIEN_DROP_INTERVAL = 500  
BOMB_DROP_INTERVAL = 500  
PLAYER_LIVES = 3

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

player_image = pygame.image.load("player.png").convert_alpha()  
player_image = pygame.transform.scale(player_image, (50, 30))  

alien_image = pygame.image.load("alien.png").convert_alpha()  
alien_image = pygame.transform.scale(alien_image, (40, 30)) 

bullet_image = pygame.Surface((5, 10))
bullet_image.fill((0, 255, 0)) 

bomb_image = pygame.Surface((10, 10))
bomb_image.fill((255, 0, 0))  


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        global ALIEN_SPEED
        self.rect.x += ALIEN_SPEED
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            ALIEN_SPEED *= -1  

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bomb_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += BULLET_SPEED 
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def draw_text(text, size, color, surface, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def show_winning_screen():
    screen.fill((0, 0, 0))
    draw_text("You Win!", 64, (255, 255, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press R to Restart", 36, (255, 255, 255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_restart()

def show_game_over_screen():
    screen.fill((0, 0, 0))
    draw_text("Game Over!", 64, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press R to Restart", 36, (255, 255, 255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_restart()

def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bombs = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

alien_rows = 5
alien_columns = 10
for row in range(alien_rows):
    for col in range(alien_columns):
        alien = Alien(col * 70 + 50, row * 40 + 50) 
        all_sprites.add(alien)
        aliens.add(alien)

running = True
clock = pygame.time.Clock()
last_drop_time = pygame.time.get_ticks()
last_bomb_time = pygame.time.get_ticks()
lives = PLAYER_LIVES

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    all_sprites.update()

    hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    bomb_hits = pygame.sprite.spritecollide(player, bombs, True)
    if bomb_hits:
        lives -= 1
        if lives <= 0:
            show_game_over_screen()
            lives = PLAYER_LIVES  
            all_sprites.empty()
            aliens.empty()
            bullets.empty()
            bombs.empty()
            player = Player()
            all_sprites.add(player)
            for row in range(alien_rows):
                for col in range(alien_columns):
                    alien = Alien(col * 70 + 50, row * 40 + 50) 
                    all_sprites.add(alien)
                    aliens.add(alien)

    if len(aliens) == 0: 
        show_winning_screen()
        lives = PLAYER_LIVES 
        all_sprites.empty()
        aliens.empty()
        bullets.empty()
        bombs.empty()
        player = Player()
        all_sprites.add(player)
        for row in range(alien_rows):
            for col in range(alien_columns):
                alien = Alien(col * 70 + 50, row * 40 + 50)  
                aliens.add(alien)

    if pygame.time.get_ticks() - last_bomb_time > BOMB_DROP_INTERVAL:
        if aliens:  
            alien = random.choice(aliens.sprites())  
            bomb = Bomb(alien.rect.centerx, alien.rect.bottom)
            all_sprites.add(bomb)
            bombs.add(bomb)
            last_bomb_time = pygame.time.get_ticks()

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    
    draw_text(f"Lives: {lives}", 36, (255, 255, 255), screen, SCREEN_WIDTH - 100, 30)
    
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
