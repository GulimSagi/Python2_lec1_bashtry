import pygame
import math
import random

WIDTH = 1600
HEIGHT = 900
block_size = 50
coin_size = block_size//2
gun_size = block_size*2
key_size = 30
FPS = 60
current_time = 0
button_press_time = 0
turret_reload = 0

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

pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

background_image = pygame.image.load('background1.png').convert_alpha()
hero_right = pygame.image.load('mario_right.png').convert_alpha()
hero_left = pygame.image.load('mario_left.png').convert_alpha()
ground = pygame.image.load('ground.png').convert_alpha()
mud = pygame.image.load('mud.png').convert_alpha()
brick = pygame.image.load('brick.png').convert_alpha()
trampoline = pygame.image.load('trampoline.png').convert_alpha()
coin = pygame.image.load('coin.png').convert_alpha()
gun_right = pygame.image.load('gun_right.png').convert_alpha()
gun_left = pygame.image.load('gun_left.png').convert_alpha()
enemy1_left = pygame.image.load('enemy1_left.png').convert_alpha()
enemy1_right = pygame.image.load('enemy1_right.png').convert_alpha()
bullet = pygame.image.load('bullet.png').convert_alpha()
key = pygame.image.load('key.png').convert_alpha()
closed_door = pygame.image.load('closed_door.png').convert_alpha()
opened_door = pygame.image.load('opened_door.png').convert_alpha()
tree = pygame.image.load('tree.png').convert_alpha()
cloud = pygame.image.load('cloud.png').convert_alpha()
transparent_piece = pygame.image.load('transparent_piece.png').convert_alpha()
health = pygame.image.load('health.png').convert_alpha()

ground = pygame.transform.scale(ground, (block_size, block_size))
mud = pygame.transform.scale(mud, (block_size, block_size))
brick = pygame.transform.scale(brick, (block_size, block_size))
trampoline = pygame.transform.scale(trampoline, (block_size, block_size//2))
coin = pygame.transform.scale(coin, (coin_size, coin_size))
gun_right = pygame.transform.scale(gun_right, (gun_size, gun_size))
gun_left = pygame.transform.scale(gun_left, (gun_size, gun_size))
enemy1_left = pygame.transform.scale(enemy1_left, (block_size, block_size))
enemy1_right = pygame.transform.scale(enemy1_right, (block_size, block_size))
key = pygame.transform.scale(key, (key_size, key_size))
closed_door = pygame.transform.scale(closed_door, (block_size, block_size))
opened_door = pygame.transform.scale(opened_door, (block_size, block_size))
health = pygame.transform.scale(health, (27, 23))
tree = pygame.transform.scale(tree, (block_size*2, block_size*2))
cloud = pygame.transform.scale(cloud, (block_size*2, block_size))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 20
        self.jump_is_allowed = False
        self.look_left = False
        self.health = 100
        self.points = 0
        self.keys = 0
        self.image = pygame.transform.scale(hero_right, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.camera_x = 0
        self.camera_y = 0

    def update(self):
        global gravity, state, state_game_over, camera_x, camera_y, stable_x, stable_y

        if self.rect.x + camera_x > WIDTH * 0.65:
            camera_x -= 7
        elif self.rect.x + camera_x < WIDTH * 0.35:
            camera_x += 7
        camera_y = -self.rect.y + HEIGHT * 0.5

        if self.y > HEIGHT + 200:
            self.kill()
            state = state_game_over
        self.h_speed = 0
        self.v_speed = self.v_speed + gravity
        if self.v_speed > 25:
            self.v_speed = 25
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE] or keystate[pygame.K_UP]:
            if self.jump_is_allowed:
                self.v_speed = -self.jump_height
                self.jump_is_allowed = False
        if keystate[pygame.K_LEFT]:
            self.image = pygame.transform.scale(hero_left, (block_size, block_size))
            self.look_left = True
            self.h_speed = -7
        if keystate[pygame.K_RIGHT]:
            self.image = pygame.transform.scale(hero_right, (block_size, block_size))
            self.look_left = False
            self.h_speed = 7
        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= camera_x
        mouse_y -= int(camera_y * 0.3)
        rel_x, rel_y = mouse_x - bullet.rect.x, mouse_y - bullet.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        bullet.image = pygame.transform.rotate(bullet.image, int(angle))
        lendth_vector = math.sqrt(rel_x**2 + rel_y**2)
        if lendth_vector != 0:
            norm_vector_x, norm_vector_y = rel_x / lendth_vector, rel_y / lendth_vector
            bullet.h_speed = int(norm_vector_x * 30)
            bullet.v_speed = int(norm_vector_y * 30)
            all_sprites.add(bullet)
            bullets.add(bullet)


    def add_points(self):
        self.points += 1

    def add_key(self):
        self.keys += 1

    def show_points(self):
        screen.blit(coin, (10, 10))
        score = font.render(f"{self.points}", True, (255, 204, 0))
        screen.blit(score, (40, -10))

    def show_keys(self):
        key_image = pygame.transform.scale(key, (coin_size, coin_size))
        screen.blit(key_image, (10, 50))
        score = font.render(f"{self.keys}", True, (218, 165, 32))
        screen.blit(score, (40, 30))

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 30
        self.jump_is_allowed = False
        self.look_left = False
        self.health = 100
        self.points = 0
        self.image_left = pygame.transform.scale(enemy1_left, (block_size, block_size)) 
        self.image_right = pygame.transform.scale(enemy1_right, (block_size, block_size))
        self.image = self.image_left
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.rect.x = x
        self.rect.y = y
        self.camera_x = 0
        self.camera_y = 0
        self.cycle = 130
        self.change = 0
        self.trigger = False
        self.trigger_general = False
        self.collided_with_block = False
        self.wait_to_shoot = 10
        self.walk_away = 3
        self.path = []
        self.trigger_old = self.trigger

    def update(self):
        global gravity, state, state_game_over
        rand_number = random.randint(1, 4)

        self.shoot_x_ray()
        if self.y > HEIGHT:
            self.kill()

        self.h_speed = 0
        self.v_speed = self.v_speed + gravity

        if self.v_speed > 25:
            self.v_speed = 25

        if self.trigger and self.trigger_general:
            projection = player.rect.x - self.rect.x
            self.h_speed = rand_number if bool(projection >= 0) else -rand_number
            if self.wait_to_shoot == 0:
                self.shoot()
            self.wait_to_shoot = (self.wait_to_shoot + 1) % 60
            self.path = []

        if self.trigger == False and self.trigger_old == True:
            self.path.append((player.rect.x, player.rect.y))

        if self.trigger == False and self.trigger_general == True:
            self.path.append((player.rect.x, player.rect.y))
            if self.path != [] and self.rect.x != self.path[0][0] and self.rect.y != self.path[0][1]:
                projection = self.path[0][0] - self.rect.x
                self.h_speed = rand_number if bool(projection >= 0) else -rand_number
            elif self.path != [] and self.rect.x == self.path[0][0] and self.rect.y > self.path[0][1] and self.jump_is_allowed:
                self.v_speed -= self.jump_height
                self.jump_is_allowed = False

            # elif self.path == []:
                # pass
            else:
                self.path.pop(0)
            
        if self.trigger == False and self.trigger_general == False:
            if self.cycle >= 0:
                self.h_speed = 2 if bool(self.change) else -2
                self.cycle -= 1
            else:
                self.cycle = 130
                self.change = (self.change + 1) % 2

        if self.collided_with_block and self.jump_is_allowed:
            self.v_speed -= self.jump_height
            self.jump_is_allowed = False

        if self.h_speed > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left

        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed
        self.trigger_old = self.trigger

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        mouse_x, mouse_y = player.rect.centerx, player.rect.centery
        rel_x, rel_y = mouse_x - bullet.rect.x, mouse_y - bullet.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        bullet.image = pygame.transform.rotate(bullet.image, int(angle))
        lendth_vector = math.sqrt(rel_x**2 + rel_y**2)
        if lendth_vector != 0:
            norm_vector_x, norm_vector_y = rel_x / lendth_vector, rel_y / lendth_vector
            bullet.h_speed = int(norm_vector_x * 30)
            bullet.v_speed = int(norm_vector_y * 30)
            all_sprites.add(bullet)
            bullets_enemy.add(bullet)

    def shoot_x_ray(self):
        ray = X_ray(self.rect.centerx, self.rect.centery, self)
        mouse_x, mouse_y = player.rect.centerx, player.rect.centery
        rel_x, rel_y = mouse_x - ray.rect.x, mouse_y - ray.rect.y
        # angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        # bullet.image = pygame.transform.rotate(bullet.image, int(angle))
        lendth_vector = math.sqrt(rel_x**2 + rel_y**2)
        if lendth_vector != 0:
            norm_vector_x, norm_vector_y = rel_x / lendth_vector, rel_y / lendth_vector
            ray.h_speed = int(norm_vector_x * 30)
            ray.v_speed = int(norm_vector_y * 30)
            all_sprites.add(ray)
            x_rays_enemy.add(ray)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, reload):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(gun_right, (gun_size, gun_size))
        self.rect = self.image.get_rect()
        self.look_left = False
        self.rect.x = x
        self.rect.y = y
        self.reload = reload

    def update(self):
        global camera_x, camera_y
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.look_left = True
            self.image = pygame.transform.scale(gun_left, (gun_size, gun_size))
        if keystate[pygame.K_RIGHT]:
            self.look_left = False
            self.image = pygame.transform.scale(gun_right, (gun_size, gun_size))

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if self.look_left:
            new_image = pygame.transform.rotate(self.image, int(-angle))
        else:
            new_image = pygame.transform.rotate(self.image, int(angle))
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet, (block_size//4, block_size//8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_speed = -10
        self.h_speed = 10

    def update(self):
        global camera_x, camera_y
        self.rect.y += self.v_speed
        self.rect.x += self.h_speed
        if self.rect.bottom < -2000 or self.rect.left > WIDTH - camera_x or self.rect.right + camera_x < 0 or self.rect.top > 2000:
            self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jump = False
        self.shooting = False

    def shoot(self):
        bullet = Bullet(self.rect.centerx - block_size, self.rect.centery)
        bullet.image = pygame.transform.rotate(bullet.image, 180)
        bullet.h_speed = -10
        bullet.v_speed = 0
        bullets_enemy.add(bullet)
        bullets.add(bullet)
        all_sprites.add(bullet)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jump = False

    def check_key(self):
        if player.keys == 1:
            self.image = opened_door
            player.keys -= 1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class X_ray(pygame.sprite.Sprite):
    def __init__(self, x, y, mob):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(transparent_piece, (block_size//4, block_size//8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_speed = -10
        self.h_speed = 10
        self.mob = mob

    def update(self):
        global camera_x, camera_y
        self.rect.y += self.v_speed
        self.rect.x += self.h_speed
        if self.rect.bottom < -2000 or self.rect.left > WIDTH - camera_x or self.rect.right + camera_x < 0 or self.rect.top > 2000:
            self.kill()

#Functions
def load_game_map():
    global game_map
    game_map.clear()
    with open('map1.txt', 'r') as f:
        for line in f:
            game_map.append(line)

def draw_shield_bar(length, height, x, y, health, color):
    if health < 0:
        health = 0
    BAR_LENGTH = length
    BAR_HEIGHT = height
    fill = (health / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, color, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

def collide(sprite1, sprite2):
    global HEIGHT, state_game_over, state

    if sprite1 == player and sprite2 == blocks:
        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        if collisions == []:
            sprite1.jump_is_allowed = False
        else:
            for collision in collisions:
                r_from_above = collision.rect.y - sprite1.y - block_size
                r_from_below = sprite1.y - collision.rect.y - block_size
                if (abs(sprite1.x + block_size//2 - collision.rect.centerx) < block_size) and ((((sprite1.rect.bottom - collision.rect.top) < 1) or ((sprite1.rect.top - collision.rect.bottom) < 1))) and (r_from_above >= 0 or r_from_below >= 0):
                    if sprite1.v_speed > 0:
                        sprite1.rect.y = sprite1.y + r_from_above
                        sprite1.jump_is_allowed = True
                    elif sprite1.v_speed < 0:
                        sprite1.rect.y = sprite1.y - r_from_below
                    sprite1.v_speed = 0
                    if collision.jump:
                        sprite1.jump_height = 30
                        sprite1.v_speed = -sprite1.jump_height
                    else:
                        sprite1.jump_height = 20


        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        for collision in collisions:
            if sprite1.rect.left <= collision.rect.right or sprite1.rect.right >= collision.rect.left:
                sprite1.rect.x = sprite1.x
                if sprite1.h_speed > 0:
                    r_from_left = collision.rect.left - sprite1.rect.right
                    sprite1.rect.x = sprite1.x + r_from_left
                if sprite1.h_speed < 0:
                    r_from_right = sprite1.rect.left - collision.rect.right
                    sprite1.rect.x = sprite1.x - r_from_right

    if sprite1 == mobs and sprite2 == blocks:
        for mob in sprite1:
            collisions = pygame.sprite.spritecollide(mob, sprite2, False)
            if collisions == []:
                mob.jump_is_allowed = False
            else:
                for collision in collisions:
                    r_from_above = collision.rect.y - mob.y - block_size
                    r_from_below = mob.y - collision.rect.y - block_size
                    if (abs(mob.x + block_size//2 - collision.rect.centerx) < block_size) and ((((mob.rect.bottom - collision.rect.top) < 1) or ((mob.rect.top - collision.rect.bottom) < 1))) and (r_from_above >= 0 or r_from_below >= 0):
                        if mob.v_speed > 0:
                            mob.rect.y = mob.y + r_from_above
                            mob.jump_is_allowed = True
                        elif mob.v_speed < 0:
                            mob.rect.y = mob.y - r_from_below
                        mob.v_speed = 0
                        if collision.jump:
                            mob.jump_height = 30
                            mob.v_speed = -mob.jump_height
                        else:
                            mob.jump_height = 20

            collisions = pygame.sprite.spritecollide(mob, sprite2, False)
            if collisions == []:
                mob.collided_with_block = False
            for collision in collisions:
                if mob.rect.left <= collision.rect.right or mob.rect.right >= collision.rect.left:
                    mob.rect.x = mob.x
                    if mob.h_speed > 0:
                        r_from_left = collision.rect.left - mob.rect.right
                        mob.rect.x = mob.x + r_from_left
                    if mob.h_speed < 0:
                        r_from_right = mob.rect.left - collision.rect.right
                        mob.rect.x = mob.x - r_from_right
                    mob.collided_with_block = True
                    
    elif sprite1 == player and sprite2 == coins:
        for collision in sprite2:
            if sprite1.rect.colliderect(collision.rect):
                collision.kill()
                sprite1.add_points()
    elif sprite1 == player and sprite2 == keys:
        for collision in sprite2:
            if sprite1.rect.colliderect(collision.rect):
                collision.kill()
                sprite1.add_key()
    elif sprite1 == player and sprite2 == door1:
        if sprite1.rect.colliderect(sprite2.rect):
            sprite2.check_key()
    elif (sprite1 == bullets or sprite1 == bullets_enemy) and sprite2 == blocks:
        hits = pygame.sprite.groupcollide(sprite1, sprite2, True, False)
        for hit in hits:
            hit.kill()

    elif sprite1 == x_rays_enemy and sprite2 == blocks:
        hits = pygame.sprite.groupcollide(sprite1, sprite2, True, False)
        for hit in hits:
            hit.mob.trigger = False
            hit.kill()



    elif sprite1 == player and sprite2 == bullets_enemy:
        hits = pygame.sprite.spritecollide(sprite1, sprite2, False)
        for hit in hits:
            hit.kill()
            sprite1.health -= 5


    elif sprite1 == player and sprite2 == x_rays_enemy:
        hits = pygame.sprite.spritecollide(sprite1, sprite2, False)
        for hit in hits:
            hit.mob.trigger = True
            hit.mob.trigger_general = True
            hit.kill()
            

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()
blocks = pygame.sprite.Group()
coins = pygame.sprite.Group()
keys = pygame.sprite.Group()
x_rays_enemy = pygame.sprite.Group()
path = []

game_map = []
gravity = 1
state = state_start
waiting_command = 0

done = True
while done:
    screen.blit(background_image, (0,0))

    if state == state_start:
        if waiting_command < 1:
            # camera variables
            camera_x = 0
            camera_y = 0

            # stable coordinates of the window
            stable_x = 0
            stable_y = 0

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
                        all_sprites.add(brick1)
                    if game_map[i][j] == '1':
                        machinegun1 = Block(block_size * j, block_size * i, brick)
                        machinegun1.shooting = True
                        blocks.add(machinegun1)
                        all_sprites.add(machinegun1)
                    if game_map[i][j] == '0':
                        cloud1 = Block(block_size * j, block_size * i, cloud)
                        all_sprites.add(cloud1)
                    if game_map[i][j] == 'T':
                        tree1 = Block(block_size * j, block_size * (i-1), tree)
                        all_sprites.add(tree1)
                    if game_map[i][j] == 'd':
                        brick1 = Block(block_size * j, block_size * i, brick)
                        door1 = Door(block_size * j, block_size * i, closed_door)
                        all_sprites.add(brick1)
                        all_sprites.add(door1)
                    if game_map[i][j] == 'c':
                        coin1 = Coin(block_size * j + coin_size//2, block_size * i + coin_size//2, coin)
                        coins.add(coin1)
                        all_sprites.add(coin1)
                    if game_map[i][j] == 'k':
                        key1 = Key(block_size * j + 10, block_size * i + 10, key)
                        keys.add(key1)
                        all_sprites.add(key1)
                    if game_map[i][j] == 't':
                        tramp1 = Block(block_size * j, block_size * i + block_size//2, trampoline)
                        tramp1.jump = True
                        blocks.add(tramp1)
                        all_sprites.add(tramp1)

            for i in range(len(game_map)):
                for j in range(len(game_map[i])):
                    if game_map[i][j] == 'e':
                        mob = Mob(block_size * j, block_size * i)
                        mobs.add(mob)
                        all_sprites.add(mob)

            player = Player()
            all_sprites.add(player)
            gun = Weapon(player.rect.x, player.rect.y, 1000)
            all_sprites.add(gun)

        screen.blit(text_start, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = False
                if event.key == pygame.K_SPACE:
                    state = state_play
        waiting_command += 1

    if state == state_play:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1) and (current_time - button_press_time > gun.reload):
                    # gun.rotate()
                    player.shoot()
                    button_press_time = pygame.time.get_ticks()

        all_sprites.update()
        collide(player, blocks)
        collide(player, door1)
        collide(player, coins)
        collide(player, keys)
        collide(bullets, blocks)
        collide(mobs, blocks)
        collide(bullets_enemy, blocks)
        collide(player, bullets_enemy)
        collide(player, x_rays_enemy)
        collide(x_rays_enemy, blocks)

        if (current_time - turret_reload > 1000):
            machinegun1.shoot()
            turret_reload = pygame.time.get_ticks()
        
        hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
        for m in hits.keys():
            m.health -= len(hits[m]) * 20
            if m.health <= 0:
                m.kill()
        for fanta in all_sprites:
            screen.blit(fanta.image, (fanta.rect.x + camera_x, fanta.rect.y + int(camera_y * 0.3)))

        player.show_points()
        player.show_keys()
        draw_shield_bar(120, 20, WIDTH-130, 10, player.health, GREEN)
        screen.blit(health, (WIDTH-160, 10))
        for m in mobs:
            draw_shield_bar(60, 8, m.rect.x + camera_x, m.rect.y + int(camera_y * 0.3)-15, m.health, RED)

        if player.health <= 0:
            state = state_game_over 

    if state == state_game_over:
        screen.blit(text_game_over, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = False
                if event.key == pygame.K_SPACE:
                    state = state_start
                    waiting_command = 0
                    for sprite in all_sprites:
                        sprite.kill()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()