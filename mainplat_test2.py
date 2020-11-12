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

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
window = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.mixer.music.load('sound/b_music.wav')
pygame.mixer.music.play(-1)
sound_coin = pygame.mixer.Sound('sound/coin.wav')
sound_jump = pygame.mixer.Sound('sound/jump_landing.wav')
sound_shotgun = pygame.mixer.Sound('sound/shotgun.wav')
sound_Pulemet = pygame.mixer.Sound('sound/machinegun.wav')
sound_run = pygame.mixer.Sound('sound/run.wav')
sound_gun = pygame.mixer.Sound('sound/gun.wav')
sound_gameover = pygame.mixer.Sound('sound/gameover.wav')
sound_key = pygame.mixer.Sound('sound/key.wav')
sound_new_level = pygame.mixer.Sound('sound/new_level.wav')
sound_trampoline = pygame.mixer.Sound('sound/trampoline.wav')

background_image = pygame.image.load('background1.png').convert_alpha()
hero_right = pygame.image.load('mario_right.png').convert_alpha()
hero_left = pygame.image.load('mario_left.png').convert_alpha()
ground = pygame.image.load('ground.png').convert_alpha()
mud = pygame.image.load('mud.png').convert_alpha()
brick = pygame.image.load('brick.png').convert_alpha()
trampoline = pygame.image.load('trampoline.png').convert_alpha()
coin = pygame.image.load('coin.png').convert_alpha()
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
boss1_left = pygame.image.load('boss1_left.png').convert_alpha()
boss1_right = pygame.image.load('boss1_right.png').convert_alpha()
gun_right = pygame.image.load('gun_right.png').convert_alpha()
gun_left = pygame.image.load('gun_left.png').convert_alpha()
pistol_left = pygame.image.load('pistol_left.png').convert_alpha()
pistol_right = pygame.image.load('pistol_right.png').convert_alpha()
shotgun_left = pygame.image.load('shotgun_left.png').convert_alpha()
shotgun_right = pygame.image.load('shotgun_right.png').convert_alpha()
Pulemet_right = pygame.image.load('Pulemet_right.png').convert_alpha()
Pulemet_left = pygame.image.load('Pulemet_left.png').convert_alpha()

hero_right = pygame.transform.scale(hero_right, (block_size, block_size))
hero_left = pygame.transform.scale(hero_left, (block_size, block_size))
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
boss1_left = pygame.transform.scale(boss1_left, (block_size*3, block_size*3))
boss1_right = pygame.transform.scale(boss1_right, (block_size*3, block_size*3))
pistol_left = pygame.transform.scale(pistol_left, (block_size, block_size))
pistol_right = pygame.transform.scale(pistol_right, (block_size, block_size))
shotgun_left = pygame.transform.scale(shotgun_left, (block_size, block_size))
shotgun_right = pygame.transform.scale(shotgun_right, (block_size, block_size))
Pulemet_left = pygame.transform.scale(Pulemet_left, (block_size, block_size))
Pulemet_right = pygame.transform.scale(Pulemet_right, (block_size, block_size))


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
        self.image = hero_right
        self.image_left = hero_left
        self.image_right = hero_right
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.camera_x = 0
        self.camera_y = 0
        self.gun = gun

    def update(self):
        global gravity, state, state_game_over, camera_x, camera_y, stable_x, stable_y

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
        if mouse_x > self.rect.centerx + camera_x:
            self.image = hero_right
            self.gun.image = self.gun.image_right
            self.gun.look_left = False
            self.look_left = False
        elif mouse_x < self.rect.centerx + camera_x:
            self.image = hero_left
            self.gun.image = self.gun.image_left
            self.gun.look_left = True
            self.look_left = True

        self.h_speed = 0
        self.v_speed = self.v_speed + gravity
        if self.v_speed > 25:
            self.v_speed = 25
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE] or keystate[pygame.K_UP]:
            if self.jump_is_allowed:
                sound_jump.play()
                self.v_speed = -self.jump_height
                self.jump_is_allowed = False
        if keystate[pygame.K_LEFT]:
            #self.gun.look_left = True
            #self.look_left = True
            #self.image = self.image_left
            #self.gun.image = self.gun.image_left
            self.h_speed = -7
        if keystate[pygame.K_RIGHT]:
            #self.gun.look_left = False
            #self.look_left = False
            #self.image = self.image_right
            #self.gun.image = self.gun.image_right
            self.h_speed = 7
        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed
        self.gun.rect.x = self.rect.x
        self.gun.rect.y = self.rect.y + gun_size // 4


    def shoot(self):
        pygame.mixer.Channel(1).play(sound_shotgun)
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
    def __init__(self, x, y, image_left, image_right, size, gun):
        pygame.sprite.Sprite.__init__(self)
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 22
        self.jump_is_allowed = False
        self.look_left = False
        self.health = 100
        self.points = 0
        self.image_left = pygame.transform.scale(image_left, (size, size)) 
        self.image_right = pygame.transform.scale(image_right, (size, size))
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
        self.gun = gun

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
            if self.wait_to_shoot == 0:
                self.shoot()
            self.path = []
        self.wait_to_shoot = (self.wait_to_shoot + 1) % self.gun.reload

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
            self.gun.rect.x = self.rect.x + gun_size // 2
            self.gun.rect.y = self.rect.y + gun_size // 4
            self.image = self.image_right
            self.gun.image = self.gun.image_right
            self.gun.look_left = False
        else:
            self.gun.rect.x = self.rect.x
            self.gun.rect.y = self.rect.y + gun_size // 4
            self.image = self.image_left
            self.gun.image = self.gun.image_left
            self.gun.look_left = True

        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed
        self.trigger_old = self.trigger

    def shoot(self):
        pygame.mixer.Channel(2).play(sound_gun)
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.gun)
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

class Boss(Mob):
    def __init__(self, x, y, image_left, image_right, size, gun):
        super(Boss, self).__init__(x, y, image_left, image_right, size, gun)
        

class Weapon(pygame.sprite.Sprite):
    def __init__(self, reload):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(gun_right, (gun_size, gun_size))
        self.image_left = pygame.transform.scale(gun_left, (gun_size, gun_size))
        self.image_right = pygame.transform.scale(gun_right, (gun_size, gun_size))
        self.rect = self.image.get_rect()
        self.look_left = False
        self.rect.x = 0
        self.rect.y = 0
        self.reload = reload

    def update(self):
        global camera_x, camera_y
        # self.rect.centerx = player.rect.centerx
        # self.rect.centery = player.rect.centery
        # self.look_left = player.look_left
        # if self.look_left:
        #     self.image = self.image_left
        # else:
        #     self.image = self.image_right

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

class WeaponPistol(Weapon):
    def __init__(self, reload):
        super(WeaponPistol, self).__init__(reload)
        self.image = pygame.transform.scale(pistol_left, (int(gun_size*0.5), int(gun_size*0.5)))
        self.image_left = pygame.transform.scale(pistol_left, (int(gun_size*0.5), int(gun_size*0.5)))
        self.image_right = pygame.transform.scale(pistol_right, (int(gun_size*0.5), int(gun_size*0.5)))
        self.bullet_speed = 30
        self.damage = 10

    def prepare_bullets(self):
        bullets = [Bullet(self.rect.centerx, self.rect.centery, self)]
        return bullets

class WeaponShotgun(Weapon):
    def __init__(self, reload):
        super(WeaponShotgun, self).__init__(reload)
        self.image = pygame.transform.scale(shotgun_left, (gun_size, gun_size//2))
        self.image_left = pygame.transform.scale(shotgun_left, (gun_size, gun_size//2))
        self.image_right = pygame.transform.scale(shotgun_right, (gun_size, gun_size//2))
        self.bullet_speed = 50
        self.damage = 10

    def prepare_bullets(self):
        bullets_list = [
            Bullet(self.rect.centerx, self.rect.centery, self),
            Bullet(self.rect.centerx, self.rect.centery + 4, self),
            Bullet(self.rect.centerx, self.rect.centery - 4, self),
            Bullet(self.rect.centerx, self.rect.centery + 8, self),
            Bullet(self.rect.centerx, self.rect.centery - 8, self),
            ]
        return bullets_list

class WeaponPulemet(Weapon):
    def __init__(self, reload):
        super(WeaponPulemet, self).__init__(reload)
        self.image = pygame.transform.scale(Pulemet_left, (gun_size, gun_size//2))
        self.image_left = pygame.transform.scale(Pulemet_left, (gun_size, gun_size//2))
        self.image_right = pygame.transform.scale(Pulemet_right, (gun_size, gun_size//2))
        self.bullet_speed = 50
        self.damage = 10

    def prepare_bullets(self):
        bullets_list = [
            Bullet(self.rect.centerx, self.rect.centery, self),
            Bullet(self.rect.centerx, self.rect.centery + 4, self),
            Bullet(self.rect.centerx, self.rect.centery - 4, self),
            Bullet(self.rect.centerx, self.rect.centery + 8, self),
            Bullet(self.rect.centerx, self.rect.centery - 8, self),
            ]
        return bullets_list
class WeaponPulemet2(Weapon):
    def __init__(self, reload):
        super(WeaponPulemet2, self).__init__(reload)
        self.image = pygame.transform.scale(gun_left, (gun_size, gun_size//2))
        self.image_left = pygame.transform.scale(gun_left, (gun_size, gun_size//2))
        self.image_right = pygame.transform.scale(gun_right, (gun_size, gun_size//2))
        self.bullet_speed = 50
        self.damage = 10

    def prepare_bullets(self):
        bullets_list = [
            Bullet(self.rect.centerx, self.rect.centery, self),
            Bullet(self.rect.centerx, self.rect.centery + 4, self),
            Bullet(self.rect.centerx, self.rect.centery - 4, self),
            Bullet(self.rect.centerx, self.rect.centery + 8, self),
            Bullet(self.rect.centerx, self.rect.centery - 8, self),
            ]
        return bullets_list



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, gun):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet, (block_size//4, block_size//8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx - block_size, self.rect.centery, WeaponPistol(1000))
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

def collide(sprite1, sprite2):
    global HEIGHT, state_game_over, state

    if sprite1 == player and sprite2 == blocks:
        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        if collisions == []:
            sprite1.jump_is_allowed = False
        else:
            sprite1.gun.rect.centery = sprite1.y + block_size // 2
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
                            pygame.mixer.Channel(4).play(sound_trampoline)
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
    elif sprite1 == player and sprite2 == keys:
        for collision in sprite2:
            if sprite1.rect.colliderect(collision.rect):
                sound_key.play()
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
keys = pygame.sprite.Group()
x_rays_enemy = pygame.sprite.Group()
event_blocks = {}
path = []

game_map = []
gravity = 1
state = state_start
waiting_command = 0
punkts =[(450, 250, "Start", (250, 250, 30), (250, 30, 250), 0),
(480, 350, "Quit", (250, 250, 30), (250, 30, 250), 1)]
game = Menu(punkts)

game.menu()
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
                    if game_map[i][j] == 's':
                        event_blocks['boss'] = [block_size * j, False]
                        # print(event_blocks['boss'][0], event_blocks['boss'][1])

            # a = []
            for i in range(len(game_map)):
                for j in range(len(game_map[i])):
                    if game_map[i][j] == 'e':
                        gun = WeaponPistol(60)
                        mob = Mob(block_size * j, block_size * i, enemy1_left, enemy1_right, block_size, gun)
                        # a.append(mob)
                        mobs.add(mob)
                        all_sprites.add(mob)
                        all_sprites.add(gun)

                    if game_map[i][j] == 'B':
                        gun = WeaponShotgun(60)
                        boss1 = Boss(block_size * j, block_size * i, boss1_left, boss1_right, block_size*3, gun)
                        # mobs.add(boss1)
                        # all_sprites.add(boss1)
                        # all_sprites.add(gun)


            gun = WeaponPulemet(1000)
            player = Player(gun)
            all_sprites.add(player)
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
        sound_gameover.stop()
        pygame.mixer.music.unpause()
        # print(a[-1].rect.x, a[-1].rect.y)
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
        screen.blit(health, (WIDTH-160, 10))
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

# turn a turel into a weapon
# fix the tick and counting variable
