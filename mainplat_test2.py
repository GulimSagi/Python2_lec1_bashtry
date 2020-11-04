import pygame
import math

WIDTH = 1024
HEIGHT = 768
block_size = 50
coin_size = block_size//2
gun_size = block_size*2
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 40, True, False)
text_start = font.render("Press space to start", True, RED)
text_game_over = font.render("Game Over", True, RED)

state_start = "welcome"
state_play = "play"
state_game_over = "game over"

hero_right = pygame.image.load('mario_right.png')
hero_left = pygame.image.load('mario_left.png')
ground = pygame.image.load('ground.png')
mud = pygame.image.load('mud.png')
brick = pygame.image.load('brick.png')
trampoline = pygame.image.load('trampoline.png')
coin = pygame.image.load('coin.png')
gun_right = pygame.image.load('gun_right.png')
gun_left = pygame.image.load('gun_left.png')
enemy1_left = pygame.image.load('enemy1_left.png')
enemy1_right = pygame.image.load('enemy1_right.png')

ground = pygame.transform.scale(ground, (block_size, block_size))
mud = pygame.transform.scale(mud, (block_size, block_size))
brick = pygame.transform.scale(brick, (block_size, block_size))
trampoline = pygame.transform.scale(trampoline, (block_size, block_size//2))
coin = pygame.transform.scale(coin, (coin_size, coin_size))
gun_right = pygame.transform.scale(gun_right, (gun_size, gun_size))
gun_left = pygame.transform.scale(gun_left, (gun_size, gun_size))
enemy1_left = pygame.transform.scale(enemy1_left, (block_size, block_size))
enemy1_right = pygame.transform.scale(enemy1_right, (block_size, block_size))

pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 30
        self.jump_is_allowed = False
        self.look_left = False
        self.health = 100
        self.points = 0
        self.image = pygame.transform.scale(hero_right, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.camera_x = 0
        self.camera_y = 0

    def update(self):
        global gravity, state, state_game_over

        if self.rect.x + self.camera_x > WIDTH * 0.9:
            self.camera_x -= 10
        elif self.rect.x + self.camera_x < WIDTH * 0.1:
            self.camera_x += 10
        self.camera_y = -self.y + HEIGHT * 0.5

        if self.y > HEIGHT:
            self.kill()
            state = state_game_over
        self.h_speed = 0
        self.v_speed = self.v_speed + gravity
        if self.v_speed > 25:
            self.v_speed = 25
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            if self.jump_is_allowed:
                self.v_speed = -self.jump_height
                self.jump_is_allowed = False
        if keystate[pygame.K_LEFT]:
            self.image = pygame.transform.scale(hero_left, (block_size, block_size))
            self.look_left = True
            self.h_speed = -10
        if keystate[pygame.K_RIGHT]:
            self.image = pygame.transform.scale(hero_right, (block_size, block_size))
            self.look_left = False
            self.h_speed = 10
        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def add_points(self):
        self.points += 1

    def get_points(self):
        return self.points


# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface((10, 20))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.v_speed = -10
#
#     def update(self):
#         self.rect.y += self.speedy
#         if self.rect.bottom < 0:
#             self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jump = False

    # def update(self):
    #     self.rect.x = self.rect.x + camera_x
    #     self.rect.y = self.rect.x + camera_y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # def update(self):
    #     self.rect.x = self.rect.x + camera_x
    #     self.rect.y = self.rect.x + camera_y

#Functions
def load_game_map():
    global game_map
    game_map.clear()
    with open('map.txt', 'r') as f:
        for line in f:
            game_map.append(line)

def collide(sprite1, sprite2):
    global HEIGHT, state_game_over, state

    if sprite2 == blocks:
        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        for collision in collisions:
            if ((sprite1.rect.bottom - collision.rect.top) < 1) or ((sprite1.rect.top - collision.rect.bottom) < 1):
                sprite1.rect.y = sprite1.y
                if sprite1.v_speed > 0:
                    sprite1.jump_is_allowed = True
                sprite1.v_speed = 0
                if collision.jump:
                    sprite1.jump_height = 40
                else:
                    sprite1.jump_height = 30
        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        for collision in collisions:
            if ((sprite1.rect.left - collision.rect.right) < 1) or ((sprite1.rect.right - collision.rect.left) < 1):
                sprite1.rect.x = sprite1.x
    elif sprite2 == coins:
        collisions = pygame.sprite.spritecollide(sprite1, sprite2, True)
        for collision in collisions:
            sprite1.add_points()
            coins.remove(collision)

all_sprites = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# bullets = pygame.sprite.Group()
blocks = pygame.sprite.Group()
coins = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# for i in range(8):
#     m = Mob()
#     all_sprites.add(m)
#     mobs.add(m)

game_map = []
gravity = 3
state = state_start

done = True
while done:
    screen.fill((30, 140, 255))

    if state == state_start:
        load_game_map()
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == 'g':
                    ground1 = Block(block_size * j, block_size * i, ground)
                    blocks.add(ground1)
                    all_sprites.add(ground1)
                if game_map[i][j] == 'm':
                    mud1 = Block(block_size * j, block_size * i, mud)
                    blocks.add(mud1)
                    all_sprites.add(mud1)
                if game_map[i][j] == 'b':
                    brick1 = Block(block_size * j, block_size * i, brick)
                    blocks.add(brick1)
                    all_sprites.add(brick1)
                if game_map[i][j] == 'c':
                    coin1 = Coin(block_size * j + coin_size//2, block_size * i + coin_size//2, coin)
                    coins.add(coin1)
                    all_sprites.add(coin1)
                if game_map[i][j] == 't':
                    tramp1 = Block(block_size * j, block_size * i + block_size//2, trampoline)
                    tramp1.jump = True
                    blocks.add(tramp1)
                    all_sprites.add(tramp1)

        screen.blit(text_start, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = state_play

    if state == state_play:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot()

        all_sprites.update()
        collide(player, blocks)
        collide(player, coins)

        # hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        # for hit in hits:
        #     m = Mob()
        #     all_sprites.add(m)
        #     mobs.add(m)
        # hits = pygame.sprite.spritecollide(player, mobs, False)
        # if hits:
        #     running = False
        # screen.blit(player.image_right, player.rect)

        all_sprites.draw(screen)
        screen.blit(coin, (10, 10), )
        score = font.render(f"{player.get_points()}", True, (255, 204, 0))
        screen.blit(score, (40, -10))

    if state == state_game_over:
        screen.blit(text_game_over, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = state_start

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()