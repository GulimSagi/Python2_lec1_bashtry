import pygame
import math
import random
import sys

WIDTH = 1080
HEIGHT = 768
block_size = 60
coin_size = block_size//2
gun_size = block_size
key_size = 30
FPS = 60
current_time = 0
button_press_time = 0
turret_reload = 0
timer_for_shooting = 0
coin_iteration = 0
heart_iteration = 0
key_iteration = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COIN = (204,204,0)

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 40, True, False)
text_start = font.render("Press space to start", True, RED)
text_game_over = font.render("Game Over", True, RED)
text_buy_gun = font.render("You need 1 points to buy a weapon", True, COIN)
text_no_coin = font.render("You don't have enough money", True, RED)
text_full_gun = font.render("You have already received a weapon", True, RED)
text_success_purchase = font.render("You have bought a weapon!", True, GREEN)

state_start = "welcome"
state_play = "play"
state_game_over = "game over"

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
window = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.mixer.music.load('sound/TheFatRat_Epic.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
sound_coin = pygame.mixer.Sound('sound/coin.wav')
sound_jump = pygame.mixer.Sound('sound/jump_landing.wav')
sound_shotgun = pygame.mixer.Sound('sound/shotgun.wav'); sound_shotgun.set_volume(0.2)
sound_machinegun = pygame.mixer.Sound('sound/machine_gun2.wav'); sound_machinegun.set_volume(0.2)
sound_run = pygame.mixer.Sound('sound/run.wav')
sound_gun = pygame.mixer.Sound('sound/gun.wav'); sound_gun.set_volume(0.2)
sound_gameover = pygame.mixer.Sound('sound/gameover.wav')
sound_key = pygame.mixer.Sound('sound/key.wav')
sound_new_level = pygame.mixer.Sound('sound/new_level.wav')
sound_trampoline = pygame.mixer.Sound('sound/trampoline.wav')
sound_no_bullets = pygame.mixer.Sound('sound/no_bullets.wav')
sound_reload_fast = pygame.mixer.Sound('sound/reload3.wav')
sound_reload_slow = pygame.mixer.Sound('sound/reload5.wav')

background_image = pygame.image.load('png/BG/BG.png').convert_alpha()
player_right = pygame.image.load('png/Characters/player/SnowMan1_right.png').convert_alpha()
player_left = pygame.image.load('png/Characters/player/SnowMan1_left.png').convert_alpha()
boss1_left = pygame.image.load('png/Characters/boss/boss1_left.png').convert_alpha()
boss1_right = pygame.image.load('png/Characters/boss/boss1_right.png').convert_alpha()
snow_left = pygame.image.load('png/Tiles/1.png').convert_alpha()
snow_mid = pygame.image.load('png/Tiles/2.png').convert_alpha()
snow_right = pygame.image.load('png/Tiles/3.png').convert_alpha()
ground_left = pygame.image.load('png/Tiles/4.png').convert_alpha()
ground_mid = pygame.image.load('png/Tiles/5.png').convert_alpha()
ground_right = pygame.image.load('png/Tiles/6.png').convert_alpha()
brick = pygame.image.load('png/Object/brick.png').convert_alpha()
case = pygame.image.load('png/Object/case.png').convert_alpha()
trampoline = pygame.image.load('png/Object/trampoline.png').convert_alpha()
key = pygame.image.load('png/Object/key.png').convert_alpha()
health = pygame.image.load('png/Object/health.png').convert_alpha()
closed_door = pygame.image.load('png/Object/closed_door.png').convert_alpha()
opened_door = pygame.image.load('png/Object/opened_door.png').convert_alpha()
tree = pygame.image.load('png/Object/Tree.png').convert_alpha()
trees = pygame.image.load('png/Object/Trees.png').convert_alpha()
cloud = pygame.image.load('png/Object/cloud.png').convert_alpha()
bullet = pygame.image.load('png/Weapon/bullet.png').convert_alpha()
transparent_piece = pygame.image.load('png/Weapon/transparent_piece.png').convert_alpha()
pistol_left = pygame.image.load('png/Weapon/pistol_left.png').convert_alpha()
pistol_right = pygame.image.load('png/Weapon/pistol_right.png').convert_alpha()
shotgun_left = pygame.image.load('png/Weapon/shotgun_left.png').convert_alpha()
shotgun_right = pygame.image.load('png/Weapon/shotgun_right.png').convert_alpha()
machine_gun_right = pygame.image.load('png/Weapon/machine_gun_right.png').convert_alpha()
machine_gun_left = pygame.image.load('png/Weapon/machine_gun_left.png').convert_alpha()
coins_list=[pygame.image.load('png/Object/coins/coin1.png').convert_alpha(),
       pygame.image.load('png/Object/coins/coin2.png').convert_alpha(),
       pygame.image.load('png/Object/coins/coin3.png').convert_alpha(),
       pygame.image.load('png/Object/coins/coin4.png').convert_alpha(),
       pygame.image.load('png/Object/coins/coin5.png').convert_alpha()]

enemy_list_left = []
enemy_list_right = []
enemy_stay_left = pygame.image.load('png/Characters/enemy/stay_left.png').convert_alpha()
enemy_stay_right = pygame.image.load('png/Characters/enemy/stay_right.png').convert_alpha()
heart_list = [pygame.image.load('png/Object/heart_1.png').convert_alpha(),
              pygame.image.load('png/Object/heart_2.png').convert_alpha(),
              pygame.image.load('png/Object/heart_3.png').convert_alpha(),
              pygame.image.load('png/Object/heart_4.png').convert_alpha()]
key_list = [pygame.image.load('png/Object/key_1.png').convert_alpha(),
            pygame.image.load('png/Object/key_2.png').convert_alpha(),
            pygame.image.load('png/Object/key_3.png').convert_alpha(),
            pygame.image.load('png/Object/key_3.png').convert_alpha()]

for i in range(10):
    enemy_list_right.append(pygame.image.load(f'png/Characters/enemy/walk_rigint_{i + 1}.png').convert_alpha())
for i in range(10):
    enemy_list_left.append(pygame.image.load(f'png/Characters/enemy/walk_left_{i + 1}.png').convert_alpha())


player_right = pygame.transform.scale(player_right, (block_size, block_size))
player_left = pygame.transform.scale(player_left, (block_size, block_size))
boss1_left = pygame.transform.scale(boss1_left, (block_size*3, block_size*3))
boss1_right = pygame.transform.scale(boss1_right, (block_size*3, block_size*3))
snow_left = pygame.transform.scale(snow_left, (block_size, block_size))
snow_mid = pygame.transform.scale(snow_mid, (block_size, block_size))
snow_right = pygame.transform.scale(snow_right, (block_size, block_size))
ground_left = pygame.transform.scale(ground_left, (block_size, block_size))
ground_mid = pygame.transform.scale(ground_mid, (block_size, block_size))
ground_right = pygame.transform.scale(ground_right, (block_size, block_size))
brick = pygame.transform.scale(brick, (block_size, block_size))
case = pygame.transform.scale(case, (block_size, block_size))
trampoline = pygame.transform.scale(trampoline, (block_size, block_size//2))
key = pygame.transform.scale(key, (key_size, key_size))
health = pygame.transform.scale(health,(coin_size, coin_size))
closed_door = pygame.transform.scale(closed_door, (block_size, block_size))
opened_door = pygame.transform.scale(opened_door, (block_size, block_size))
tree = pygame.transform.scale(tree, (block_size*2, block_size*2))
trees = pygame.transform.scale(trees, (block_size*2, block_size*2))
cloud = pygame.transform.scale(cloud, (block_size*2, block_size))
bullet = pygame.transform.scale(bullet, (block_size//4, block_size//8))
transparent_piece = pygame.transform.scale(transparent_piece, (block_size//4, block_size//8))
pistol_left = pygame.transform.scale(pistol_left, (int(gun_size*0.5), int(gun_size*0.5)))
pistol_right = pygame.transform.scale(pistol_right, (int(gun_size*0.5), int(gun_size*0.5)))
shotgun_left = pygame.transform.scale(shotgun_left, (gun_size, gun_size//2))
shotgun_right = pygame.transform.scale(shotgun_right, (gun_size, gun_size//2))
machine_gun_left = pygame.transform.scale(machine_gun_left, (gun_size, gun_size//2))
machine_gun_right = pygame.transform.scale(machine_gun_right, (gun_size, gun_size//2))
enemy_stay_left = pygame.transform.scale(enemy_stay_left, (block_size, block_size))
enemy_stay_right = pygame.transform.scale(enemy_stay_right, (block_size, block_size))

for i in range(len(coins_list)):
    coins_list[i]=pygame.transform.scale(coins_list[i], (coin_size, coin_size))
case = pygame.transform.scale(case,(block_size,block_size))
for i in range(len(enemy_list_left)):
    enemy_list_left[i] = pygame.transform.scale(enemy_list_left[i], (block_size, block_size))
    enemy_list_right[i] = pygame.transform.scale(enemy_list_right[i], (block_size, block_size))
for i in range(len(heart_list)):
    heart_list[i]=pygame.transform.scale(heart_list[i], (coin_size, coin_size))
for i in range(len(key_list)):
    key_list[i]=pygame.transform.scale(key_list[i], (key_size, key_size))    
    
class Player(pygame.sprite.Sprite):
    def __init__(self, gun):
        pygame.sprite.Sprite.__init__(self)
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 22
        self.jump_is_allowed = False
        self.look_left = False
        self.health = 100
        self.points = 0
        self.keys = 0
        self.image_left = player_left
        self.image_right = player_right
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.camera_x = 0
        self.camera_y = 0
        self.gun = gun
        self.hero_png_iteration = 0

    def update(self):
        global gravity, state, state_game_over, camera_x, camera_y, stable_x, stable_y, button_press_time

        self.rotate_gun()
        if self.rect.x + camera_x > WIDTH * 0.65:
            camera_x -= 7
        elif self.rect.x + camera_x < WIDTH * 0.35:
            camera_x += 7
        camera_y = -self.rect.y + HEIGHT * 0.1

        if self.y > HEIGHT + 200:
            sound_gameover.play()
            self.kill()
            state = state_game_over

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= camera_x
        mouse_y -= int(camera_y * 0.3)
        if mouse_x > self.rect.centerx:
            # self.image = hero_list_right[self.hero_png_iteration // 3]
            self.image = self.image_right
            self.gun.look_left = False
            self.look_left = False
        # elif mouse_x < self.rect.centerx:
        else:
            # self.image = hero_list_left[self.hero_png_iteration // 3]
            self.image = self.image_left
            self.gun.look_left = True
            self.look_left = True
        # elif mouse_x < self.rect.centerx + camera_x and self.h_speed == 0 and self.look_left:
            # self.image = self.image_left
            # self.gun.look_left = True
            # self.look_left = True
        # elif mouse_x > self.rect.centerx + camera_x and self.h_speed == 0 and not self.look_left:
            # self.image = self.image_right
            # self.gun.look_left = False
            # self.look_left = False
        

        self.h_speed = 0
        self.v_speed = self.v_speed + gravity
        if self.v_speed > 25:
            self.v_speed = 25
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE] or keystate[pygame.K_w]:
            if self.jump_is_allowed:
                sound_jump.play()
                self.v_speed = -self.jump_height
                self.jump_is_allowed = False
        if keystate[pygame.K_a]:
            self.h_speed = -7
        if keystate[pygame.K_d]:
            self.h_speed = 7
        if self.gun.automate and keystate[pygame.K_r] and self.gun.bullets_left < self.gun.bullets_number:
            pygame.mixer.Channel(1).play(self.gun.sound_reload_fast)
            self.gun.bullets_left = self.gun.bullets_number
            button_press_time = pygame.time.get_ticks()

            
        # self.hero_png_iteration = (self.hero_png_iteration + 1) % (3 * len(hero_list_right))

        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed
        self.gun.rect.centerx = self.rect.centerx 
        self.gun.rect.centery = self.rect.centery


    def shoot(self):
        pygame.mixer.Channel(1).play(self.gun.sound)
        bullets_list = self.gun.prepare_bullets()
        for bullet in bullets_list:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x -= camera_x
            mouse_y -= int(camera_y * 0.3)
            rel_x, rel_y = mouse_x - bullet.rect.x, mouse_y - bullet.rect.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            bullet.image = pygame.transform.rotate(bullet.image, int(angle))
            lendth_vector = math.sqrt(rel_x**2 + rel_y**2)
            if lendth_vector != 0:
                norm_vector_x, norm_vector_y = rel_x / lendth_vector, rel_y / lendth_vector
                bullet.h_speed = int(norm_vector_x * self.gun.bullet_speed)
                bullet.v_speed = int(norm_vector_y * self.gun.bullet_speed)
                all_sprites.add(bullet)
                bullets.add(bullet)

    def rotate_gun(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= camera_x
        mouse_y -= int(camera_y * 0.3)
        rel_x, rel_y = mouse_x - self.gun.rect.centerx, mouse_y - self.gun.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if self.gun.look_left:
            self.gun.image = pygame.transform.rotate(pygame.transform.scale(self.gun.image_left, (block_size, block_size)), int(angle - 180))
        else:
            self.gun.image = pygame.transform.rotate(pygame.transform.scale(self.gun.image_right, (block_size, block_size)), int(angle))

    def add_points(self):
        self.points += 1
    def add_health(self):
        if self.health<=80:
            self.health+=20
        else:
            self.health=100
    def add_key(self):
        self.keys += 1
    def add_gun(self,gun):
        self.gun = gun
    def show_points(self):
        screen.blit(coins_list[1], (10, 10))
        score = font.render(f"{self.points}", True, COIN)
        screen.blit(score, (40, -5))

    def show_keys(self):
        key_image = pygame.transform.scale(key, (coin_size, coin_size))
        screen.blit(key_image, (10, 50))
        score = font.render(f"{self.keys}", True, (218, 165, 32))
        screen.blit(score, (40, 35))
  
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image_left, image_right, size, gun):
        pygame.sprite.Sprite.__init__(self)
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 22
        self.jump_is_allowed = False
        self.look_left = False
        self.health = 100
        self.points = 0
        self.image_left = image_left
        self.image_right = image_right
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
        self.walk_away = 3
        self.path = []
        self.trigger_old = self.trigger
        self.gun = gun
        self.current_time = pygame.time.get_ticks()
        self.time_shoot = self.current_time - self.gun.reload
        self.enemy_png_iteration = 0

    def update(self):
        global gravity, state, state_game_over
        rand_number = random.randint(1, 4)

        self.shoot_x_ray()
        if self.y > HEIGHT:
            self.kill()
            self.gun.kill()

        self.h_speed = 0
        self.v_speed = self.v_speed + gravity

        if self.v_speed > 25:
            self.v_speed = 25

        if self.trigger and self.trigger_general:
            projection = player.rect.x - self.rect.x
            self.h_speed = rand_number if bool(projection >= 0) else -rand_number
            if pygame.time.get_ticks() - self.time_shoot > self.gun.reload:
                self.shoot()
                self.time_shoot = pygame.time.get_ticks()
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
            self.gun.rect.centerx = self.rect.centerx + gun_size // 2
            self.gun.rect.centery = self.rect.centery + gun_size // 4
            self.image = enemy_list_right[self.enemy_png_iteration // 3]
            self.gun.image = self.gun.image_right
            self.gun.look_left = False
        elif self.h_speed < 0:
            self.gun.rect.centerx = self.rect.centerx + gun_size // 2
            self.gun.rect.centery = self.rect.centery + gun_size // 4
            self.image = enemy_list_left[self.enemy_png_iteration // 3]
            self.gun.image = self.gun.image_left
            self.gun.look_left = True
        elif self.look_left and self.h_speed == 0:
            self.image = enemy_stay_left
        elif self.look_left == False and self.h_speed == 0:
            self.image = enemy_stay_right
        
        self.enemy_png_iteration = (self.enemy_png_iteration + 1) % (3 * len(enemy_list_left))

        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed
        self.trigger_old = self.trigger

    def shoot(self):
        pygame.mixer.Channel(2).play(self.gun.sound)
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.gun)
        mouse_x, mouse_y = player.rect.centerx, player.rect.centery
        rel_x, rel_y = mouse_x - bullet.rect.x, mouse_y - bullet.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        bullet.image = pygame.transform.rotate(bullet.image, int(angle))
        lendth_vector = math.sqrt(rel_x**2 + rel_y**2)
        if lendth_vector != 0:
            norm_vector_x, norm_vector_y = rel_x / lendth_vector, rel_y / lendth_vector
            bullet.h_speed = int(norm_vector_x * self.gun.bullet_speed)
            bullet.v_speed = int(norm_vector_y * self.gun.bullet_speed)
            all_sprites.add(bullet)
            bullets_enemy.add(bullet)

    def shoot_x_ray(self):
        ray = X_ray(self.rect.centerx, self.rect.centery, self)
        mouse_x, mouse_y = player.rect.centerx, player.rect.centery
        rel_x, rel_y = mouse_x - ray.rect.x, mouse_y - ray.rect.y
        lendth_vector = math.sqrt(rel_x**2 + rel_y**2)
        if lendth_vector != 0:
            norm_vector_x, norm_vector_y = rel_x / lendth_vector, rel_y / lendth_vector
            ray.h_speed = int(norm_vector_x * 30)
            ray.v_speed = int(norm_vector_y * 30)
            all_sprites.add(ray)
            x_rays_enemy.add(ray)

class Boss(Mob):
    def __init__(self, x, y, image_left, image_right, size, gun):
        super(Boss, self).__init__(x, y, image_left, image_right, size, gun)
        self.gun.image_left = pygame.transform.scale(self.gun.image_left, (gun_size*2, gun_size*2)) 
        self.gun.image_right = pygame.transform.scale(self.gun.image_right, (gun_size*2, gun_size*2))
        # self.image_left = image_left
        # self.image_right = image_right

    def update(self):
        global gravity, state, state_game_over
        rand_number = random.randint(1, 4)

        self.shoot_x_ray()
        if self.y > HEIGHT:
            self.kill()
            self.gun.kill()

        self.h_speed = 0
        self.v_speed = self.v_speed + gravity

        if self.v_speed > 25:
            self.v_speed = 25

        if self.trigger and self.trigger_general:
            projection = player.rect.x - self.rect.x
            self.h_speed = rand_number if bool(projection >= 0) else -rand_number
            if pygame.time.get_ticks() - self.time_shoot >= self.gun.reload:
                self.shoot()
                self.time_shoot = pygame.time.get_ticks()
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
            self.gun.rect.centerx = self.rect.centerx - gun_size // 4
            self.gun.rect.centery = self.rect.centery + gun_size // 4
            self.image = self.image_right
            self.gun.image = self.gun.image_right
            self.gun.look_left = False
        else:
            self.gun.rect.centerx = self.rect.centerx - gun_size // 4
            self.gun.rect.centery = self.rect.centery + gun_size // 4
            self.image = self.image_left
            self.gun.image = self.gun.image_left
            self.gun.look_left = True

        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed
        self.trigger_old = self.trigger
    

class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pistol_right
        self.image_left = pistol_left
        self.image_right = pistol_right
        self.rect = self.image.get_rect()
        self.look_left = False
        self.rect.x = 0
        self.rect.y = 0
        self.automate_shooting = False

    def update(self):
        global camera_x, camera_y

class WeaponPistol(Weapon):
    def __init__(self):
        super(WeaponPistol, self).__init__()
        self.image = pistol_right
        self.image_left = pistol_left
        self.image_right = pistol_right
        self.bullet_speed = 30
        self.damage = 10
        self.automate = False
        self.reload = 1000
        self.sound = sound_gun

    def prepare_bullets(self):
        bullets = [Bullet(self.rect.centerx, self.rect.centery, self)]
        return bullets

class WeaponShotgun(Weapon):
    def __init__(self):
        super(WeaponShotgun, self).__init__()
        self.image = shotgun_right
        self.image_left = shotgun_left
        self.image_right = shotgun_right
        self.bullet_speed = 50
        self.damage = 10
        self.automate = False
        self.reload = 1000
        self.sound = sound_shotgun

    def prepare_bullets(self):
        bullets_list = [
            Bullet(self.rect.centerx, self.rect.centery, self),
            Bullet(self.rect.centerx, self.rect.centery + 4, self),
            Bullet(self.rect.centerx, self.rect.centery - 4, self),
            Bullet(self.rect.centerx, self.rect.centery + 8, self),
            Bullet(self.rect.centerx, self.rect.centery - 8, self),
            ]
        return bullets_list

class WeaponMachineGun(Weapon):
    def __init__(self):
        super(WeaponMachineGun, self).__init__()
        self.image = machine_gun_right
        self.image_left = machine_gun_left
        self.image_right = machine_gun_right
        self.bullet_speed = 60
        self.reload = 1500
        self.damage = 10
        self.automate = True
        self.automate_shooting = False
        self.bullets_number = 15
        self.bullets_left = self.bullets_number
        self.SPS = 8
        self.sound = sound_machinegun
        self.sound_reload_fast = sound_reload_fast

    def prepare_bullets(self):
        bullets_list = [
            Bullet(self.rect.centerx, self.rect.centery, self),
            ]
        return bullets_list

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, gun):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - gun_size // 4
        self.v_speed = -10
        self.h_speed = 10
        self.gun = gun

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
        self.active = False
        self.have_bought = False
        self.button_sell_time = 0
        self.have_money = False
        self.counter_for_text = 0
        self.start_counting = False

    def shoot(self):
        bullet = Bullet(self.rect.centerx - block_size, self.rect.centery, WeaponPistol())
        bullet.image = pygame.transform.rotate(bullet.image, 180)
        bullet.h_speed = -10
        bullet.v_speed = 0
        bullets_enemy.add(bullet)
        bullets.add(bullet)
        all_sprites.add(bullet)

    def buy_weapon(self):
        if player.points >= 1:
            self.have_money = True
            self.button_sell_time = pygame.time.get_ticks()
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_e]:
                if self.active:
                    self.active = False
                    player.points -= 1
                    player.gun.kill()
                    gun = WeaponMachineGun()
                    all_sprites.add(gun)
                    player.add_gun(gun)
                    self.have_bought = True
        else:
            self.have_money = False
            self.button_sell_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.button_sell_time < 2000 and self.have_money == False and self.have_bought == False:
            screen.blit(text_no_coin, (80, -10))
        elif current_time - self.button_sell_time < 2000 and self.have_bought == False:
            screen.blit(text_buy_gun, (80, -10))
        elif current_time - self.button_sell_time < 2000 and self.have_bought == True and self.counter_for_text < 60:
            screen.blit(text_success_purchase, (80, -10))
            self.start_counting = True
        elif self.counter_for_text == 60:
            self.start_counting = False

        if self.start_counting:
            self.counter_for_text += 1

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
            sound_new_level.play()
            self.image = opened_door
            player.keys -= 1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global coin_iteration
        self.image = coins_list[coin_iteration // 150]
        coin_iteration = (coin_iteration + 1) % (150 * len(coins_list)) 

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        global heart_iteration
        self.image = heart_list[heart_iteration // 150]
        heart_iteration = (heart_iteration + 1) % (150 * len(heart_list)) 
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        global key_iteration
        self.image = key_list[key_iteration // 60]
        key_iteration = (key_iteration + 1) % (60 * len(key_list))

class X_ray(pygame.sprite.Sprite):
    def __init__(self, x, y, mob):
        pygame.sprite.Sprite.__init__(self)
        self.image = transparent_piece
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

class Menu:
    def __init__(self, punkts = [0, 0, 'punkt', (250, 250, 30), (250, 30, 250)]):
        self.punkts = punkts

    def render(self, poverhost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] + 60))
            else:
                poverhost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] + 60))

    def menu(self):
        global state, state_play
        igra = True
        font_menu = pygame.font.Font("super_mario_bros.otf", 50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while igra:
            window.fill((0,100,200))

            mp = pygame.mouse.get_pos()   # learn
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] > i[1] + 50: # learn
                    punkt = i[5]
            self.render(window, font_menu, punkt)

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
                if i.type == pygame.KEYDOWN:    # learn
                    if i.key == pygame.K_ESCAPE:    # learn
                        sys.exit()
                    if i.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if i.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                    if punkt == 0:
                        state = state_play
                        igra = False
                    elif punkt == 1:
                        sys.exit()
            screen.blit(window, (0, 0))
            pygame.display.flip()

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

def automate_shoot(charachter, current_time, button_press_time):
    if charachter.gun.automate_shooting and charachter.gun.bullets_left > 0 and current_time - button_press_time > charachter.gun.reload:
        charachter.shoot()
        charachter.gun.bullets_left -= 1

    if charachter.gun.automate and charachter.gun.bullets_left <= 0:
        charachter.gun.bullets_left = charachter.gun.bullets_number
        pygame.mixer.Channel(1).play(sound_no_bullets)
        pygame.mixer.Channel(6).play(sound_reload_slow)
        button_press_time = pygame.time.get_ticks()

    return button_press_time

def collide(sprite1, sprite2):
    global HEIGHT, state_game_over, state

    if sprite1 == player and sprite2 == blocks:
        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        if collisions == []:
            sprite1.jump_is_allowed = False
        else:
            # sprite1.gun.rect.centery = sprite1.y + block_size // 2
            for collision in collisions:
                r_from_above = collision.rect.y - sprite1.y - block_size
                r_from_below = sprite1.y - collision.rect.y - block_size
                if (abs(sprite1.x + block_size//2 - collision.rect.centerx) < block_size) and ((((sprite1.rect.bottom - collision.rect.top) < 1) or ((sprite1.rect.top - collision.rect.bottom) < 1))) and (r_from_above >= 0 or r_from_below >= 0):
                    if sprite1.h_speed > 0:
                        pygame.mixer.Channel(3).play(sound_run)
                    if sprite1.v_speed > 0:
                        sprite1.rect.y = sprite1.y + r_from_above
                        sprite1.jump_is_allowed = True
                    elif sprite1.v_speed < 0:
                        sprite1.rect.y = sprite1.y - r_from_below
                    sprite1.v_speed = 0
                    if collision.jump:
                        pygame.mixer.Channel(6).play(sound_trampoline)
                        sprite1.jump_height = 32
                        sprite1.v_speed = -sprite1.jump_height
                    else:
                        sprite1.jump_height = 22


        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        if collisions != []:
            sprite1.gun.rect.centerx = sprite1.x + block_size // 2
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
            size = block_size * 3 if mob == boss1 else block_size
            collisions = pygame.sprite.spritecollide(mob, sprite2, False)
            if collisions == []:
                mob.jump_is_allowed = False
            else:
                mob.gun.centery = mob.y + block_size // 2
                for collision in collisions:
                    r_from_above = collision.rect.y - mob.y - size
                    r_from_below = mob.y - collision.rect.y - size
                    if (abs(mob.x + size//2 - collision.rect.centerx) < size) and ((((mob.rect.bottom - collision.rect.top) < 1) or ((mob.rect.top - collision.rect.bottom) < 1))) and (r_from_above >= 0 or r_from_below >= 0):
                        if mob.v_speed > 0:
                            mob.rect.y = mob.y + r_from_above
                            mob.jump_is_allowed = True
                        elif mob.v_speed < 0:
                            mob.rect.y = mob.y - r_from_below
                        mob.v_speed = 0
                        if collision.jump:
                            pygame.mixer.Channel(7).play(sound_trampoline)
                            mob.jump_height = 32
                            mob.v_speed = -mob.jump_height
                            mob.jump_is_allowed = False
                        else:
                            mob.jump_height = 22

            collisions = pygame.sprite.spritecollide(mob, sprite2, False)
            if collisions == []:
                mob.collided_with_block = False
            if collisions != []:
                mob.gun.centerx = mob.x + block_size // 2
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
                sound_coin.play()
                collision.kill()
                sprite1.add_points()

    elif sprite1 == player and sprite2 == hearts:
        for collision in sprite2:
            if sprite1.rect.colliderect(collision.rect):
                collision.kill()
                sprite1.add_health()

    elif sprite1 == player and sprite2 == keys:
        for collision in sprite2:
            if sprite1.rect.colliderect(collision.rect):
                sound_key.play()
                collision.kill()
                sprite1.add_key()

    elif sprite1 == player and sprite2 == door1:
        if sprite1.rect.colliderect(sprite2.rect):
            sprite2.check_key()

    elif sprite1 == player and sprite2 == strong_boxes:
        case = pygame.sprite.spritecollide(sprite1, sprite2, False)
        if case != []:
            if sprite1.rect.colliderect(case[0].rect):
                case[0].buy_weapon()

    
    elif (sprite1 == bullets or sprite1 == bullets_enemy) and sprite2 == blocks:
        hits = pygame.sprite.groupcollide(sprite1, sprite2, True, False)
        for hit in hits:
            hit.kill()

    elif sprite1 == x_rays_enemy and sprite2 == blocks:
        hits = pygame.sprite.groupcollide(sprite1, sprite2, True, False)
        for hit in hits:
            hit.mob.trigger = False
            hit.kill()

    elif sprite1 == mobs and sprite2 == bullets:
        hits = pygame.sprite.groupcollide(sprite1, sprite2, False, True)
        for m in hits.keys():
            m.health -= len(hits[m]) * (hits[m][0].gun.damage)
            if m.health <= 0:
                m.kill()
                m.gun.kill()


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
hearts = pygame.sprite.Group()
keys = pygame.sprite.Group()
x_rays_enemy = pygame.sprite.Group()
strong_boxes = pygame.sprite.Group()
event_blocks = {}
path = []

game_map = []
gravity = 1
state = state_start
waiting_command = 0
punkts =[(450, 250, "Start", (250, 250, 30), (250, 30, 250), 0),
(480, 350, "Quit", (250, 250, 30), (250, 30, 250), 1)]
game = Menu(punkts)


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
                        snow_mid1 = Block(block_size * j, block_size * i, snow_mid)
                        blocks.add(snow_mid1)
                        all_sprites.add(snow_mid1)
                    if game_map[i][j] == 'm':
                        ground_mid1 = Block(block_size * j, block_size * i, ground_mid)
                        blocks.add(ground_mid1)
                        all_sprites.add(ground_mid1)
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
                        coin1 = Coin(block_size * j + coin_size//2, block_size * i + coin_size//2, coins_list[0])
                        coins.add(coin1)
                        all_sprites.add(coin1)
                    if game_map[i][j] == 'C':
                        case1 = Block(block_size*j, block_size * i, case)
                        case1.active = True
                        strong_boxes.add(case1)
                        all_sprites.add(case1)
                    if game_map[i][j] == 'h':
                        heart1 = Heart(block_size * j + coin_size//2, block_size * i + coin_size//2, heart_list[0])
                        hearts.add(heart1)
                        all_sprites.add(heart1)
                    if game_map[i][j] == 'k':
                        key1 = Key(block_size * j + 10, block_size * i + 10, key_list[0])
                        keys.add(key1)
                        all_sprites.add(key1)
                    if game_map[i][j] == 't':
                        tramp1 = Block(block_size * j, block_size * i + block_size//2, trampoline)
                        tramp1.jump = True
                        blocks.add(tramp1)
                        all_sprites.add(tramp1)
                    if game_map[i][j] == 's':
                        event_blocks['boss'] = [block_size * j, False]

            for i in range(len(game_map)):
                for j in range(len(game_map[i])):
                    if game_map[i][j] == 'e':
                        gun = WeaponPistol()
                        mob = Mob(block_size * j, block_size * i, enemy_stay_left, enemy_stay_right, block_size, gun)
                        mobs.add(mob)
                        all_sprites.add(mob)
                        all_sprites.add(gun)

                    if game_map[i][j] == 'B':
                        gun = WeaponShotgun()
                        boss1 = Boss(block_size * j, block_size * i, boss1_left, boss1_right, block_size*3, gun)
                        # mobs.add(boss1)
                        # all_sprites.add(boss1)
                        # all_sprites.add(gun)

            gun = WeaponPistol()
            player = Player(gun)
            all_sprites.add(player)
            all_sprites.add(gun)

        game.menu()
        waiting_command += 1

    if state == state_play:
        # print(player.rect.y, player.y)
        sound_gameover.stop()
        pygame.mixer.music.unpause()
        current_time = pygame.time.get_ticks()

        if player.gun.automate and current_time - timer_for_shooting > 1000 // player.gun.SPS:
            button_press_time = automate_shoot(player, current_time, button_press_time)
            timer_for_shooting = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.gun.automate == False:
                    if (event.button == 1) and (current_time - button_press_time > player.gun.reload):
                        player.shoot()
                        button_press_time = pygame.time.get_ticks()

                if player.gun.automate == True:
                    if event.button == 1:
                        player.gun.automate_shooting = True
                        timer_for_shooting = pygame.time.get_ticks() - 100

            if event.type == pygame.MOUSEBUTTONUP:
                player.gun.automate_shooting = False


        all_sprites.update()
        collide(player, blocks)
        collide(player, door1)
        collide(player, coins)
        collide(player, hearts)
        collide(player, keys)
        collide(player, strong_boxes)
        collide(bullets, blocks)
        collide(mobs, blocks)
        collide(bullets_enemy, blocks)
        collide(player, bullets_enemy)
        collide(player, x_rays_enemy)
        collide(x_rays_enemy, blocks)
        collide(mobs, bullets)

        if (current_time - turret_reload > 1000):
            machinegun1.shoot()
            turret_reload = pygame.time.get_ticks()
        
        for key_i in event_blocks.keys():
            if key_i == 'boss' and player.rect.x > event_blocks[key_i][0] and event_blocks[key_i][1] == False:
                mobs.add(boss1)
                all_sprites.add(boss1)
                all_sprites.add(boss1.gun)
                event_blocks[key_i][1] = True

        for fanta in all_sprites:
            screen.blit(fanta.image, (fanta.rect.x + camera_x, fanta.rect.y + int(camera_y * 0.3)))

        player.show_points()
        player.show_keys()
        draw_shield_bar(120, 20, WIDTH-130, 10, player.health, GREEN)
        screen.blit(health, (WIDTH-165, 5))
        for m in mobs:
            draw_shield_bar(60, 8, m.rect.x + camera_x, m.rect.y + int(camera_y * 0.3)-15, m.health, RED)

        if player.health <= 0:
            sound_gameover.play()
            state = state_game_over 

    if state == state_game_over:
        pygame.mixer.music.pause()
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

# must be done tasks:
# turn turel into a weapon (find a good picture)
# add sound to the turel, it should be really natural to the big gun sound
# find better sound for game over
# find why when player is holding a pistol it becames bigger
# add sound to the turel
# increase the health of the boss and damage of his weapon, then test it (it should be really hard to defeat the boss, but possible)
# make a better, bigger, harder map
# understand the code
# find better music for the background

# optional tasks:
# (optional) find a better weapon for the boss
# (optional) find better pictures of weapons so that when player rotate them, it should look more natural 
# (optional) make jump_up and jump_landing for different cases (when landing and jumping)

# harder tasks:
# ANIMATE WHAT YOU CAN
# find better characthers (pictures) for the: player, enemies, boss

# questions:
# Will we make the shop?
# Will there be an another map?
# Will we animate all the stuff?
