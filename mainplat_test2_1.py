import pygame
import math

WIDTH = 1024
HEIGHT = 768
block_size = 50
coin_size = block_size//2
gun_size = block_size*2
FPS = 60

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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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

ground = pygame.transform.scale(ground, (block_size, block_size))
mud = pygame.transform.scale(mud, (block_size, block_size))
brick = pygame.transform.scale(brick, (block_size, block_size))
trampoline = pygame.transform.scale(trampoline, (block_size, block_size//2))
coin = pygame.transform.scale(coin, (coin_size, coin_size))
gun_right = pygame.transform.scale(gun_right, (gun_size, gun_size))
gun_left = pygame.transform.scale(gun_left, (gun_size, gun_size))
enemy1_left = pygame.transform.scale(enemy1_left, (block_size, block_size))
enemy1_right = pygame.transform.scale(enemy1_right, (block_size, block_size))


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
        #self.image = pygame.Surface((50,40))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.camera_x = 0
        self.camera_y = 0

    def update(self):
        global gravity, state, state_game_over, camera_x, camera_y, stable_x, stable_y

        if self.rect.x + camera_x > WIDTH * 0.65:
            camera_x -= 10
        elif self.rect.x + camera_x < WIDTH * 0.35:
            camera_x += 10
        camera_y = -self.rect.y + HEIGHT * 0.5

        if self.y > HEIGHT:
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
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= camera_x
        mouse_y -= int(camera_y * 0.3)
        print((mouse_x, mouse_y),(camera_x, camera_y), pygame.mouse.get_pos(), (self.rect.x, self.rect.y), (self.x, self.y), bullet.rect.x, bullet.rect.y)
        rel_x, rel_y = mouse_x - bullet.rect.x, mouse_y - bullet.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        bullet.image = pygame.transform.rotate(bullet.image, int(angle))
        bullet.v_speed = rel_y // int(math.sqrt(abs(rel_y + rel_x)))
        bullet.h_speed = rel_x // int(math.sqrt(abs(rel_y + rel_x)))
        # bullet.v_speed = 40
        # bullet.h_speed = 40
        all_sprites.add(bullet)
        bullets.add(bullet)

    def add_points(self):
        self.points += 1

    def get_points(self):
        return self.points


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
        self.image = pygame.transform.scale(enemy1_left, (block_size, block_size))
        #self.image = pygame.Surface((50,40))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.rect.x = x
        self.rect.y = y
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
        self.h_speed = 0
        self.v_speed = self.v_speed + gravity
        if self.v_speed > 25:
            self.v_speed = 25

        # self.rect.x += self.v_speed
            
        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.x += self.h_speed
        self.rect.y += self.v_speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - bullet.rect.x, mouse_y - bullet.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        bullet.image = pygame.transform.rotate(bullet.image, int(angle))
        bullet.v_speed = rel_y // int(math.sqrt(abs(rel_y + rel_x)))
        bullet.h_speed = rel_x // int(math.sqrt(abs(rel_y + rel_x)))
        all_sprites.add(bullet)
        bullets.add(bullet)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(gun_right, (gun_size, gun_size))
        self.rect = self.image.get_rect()
        self.look_left = False
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global camera_x, camera_y
        
        self.rect.x = player.rect.x - block_size//2
        self.rect.y = player.rect.y - block_size//2
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
        # print(camera_y)
        if self.rect.bottom < 0 - camera_y or self.rect.left > WIDTH - camera_x or self.rect.right + camera_x < 0 or self.rect.top > HEIGHT + camera_y:
            self.kill()

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

    if sprite1 == player and sprite2 == blocks:
        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        if collisions == []:
            sprite1.jump_is_allowed = False
        else:
            for collision in collisions:
                r_from_above = collision.rect.y - sprite1.y - block_size
                r_from_below = sprite1.y - collision.rect.y - block_size
                if (abs(sprite1.x + block_size//2 - collision.rect.centerx) < block_size) and ((((sprite1.rect.bottom - collision.rect.top) < 1) or ((sprite1.rect.top - collision.rect.bottom) < 1))) and (r_from_above >= 0 or r_from_below >= 0):

                    # print(sprite1.rect.x, sprite1.x, collision.rect.left)
                    # print(sprite1.rect.centery, collision.rect.centery)
                    # sprite1.rect.y = sprite1.y
                    # print(sprite1.rect.bottom)
                    if sprite1.v_speed > 0:
                        sprite1.rect.y = sprite1.y + r_from_above
                        sprite1.jump_is_allowed = True
                    elif sprite1.v_speed < 0:
                        sprite1.rect.y = sprite1.y
                    sprite1.v_speed = 0
                    if collision.jump:
                        sprite1.v_speed = -sprite1.jump_height
                        sprite1.jump_height = 40
                    else:
                        sprite1.jump_height = 30

        collisions = pygame.sprite.spritecollide(sprite1, sprite2, False)
        for collision in collisions:
            # if ((sprite1.rect.left - collision.rect.right) == 0) or ((sprite1.rect.right - collision.rect.left) < 1):
            if sprite1.rect.left <= collision.rect.right or sprite1.rect.right >= collision.rect.left:
                # print('yaho')
                sprite1.rect.x = sprite1.x


    if sprite1 == mobs and sprite2 == blocks:
        for mob in sprite1:
            collisions = pygame.sprite.spritecollide(mob, sprite2, False)
            for collision in collisions:
                r_from_above = collision.rect.y - mob.y - block_size
                r_from_below = mob.y - collision.rect.y - block_size
                if ((((mob.rect.bottom - collision.rect.top) < 1) or ((mob.rect.top - collision.rect.bottom) < 1))) and (r_from_above >= 0 or r_from_below >= 0):
                    mob.rect.y = mob.y 
                    if mob.v_speed > 0:
                        mob.rect.y = mob.y + r_from_above
                        mob.jump_is_allowed = True
                    # elif mob.v_speed < 0:
                        # mob.rect.y = mob.y - r_from_below
                    mob.v_speed = 0
                    if collision.jump:
                        mob.v_speed = -mob.jump_height
                        mob.jump_height = 40
                    else:
                        mob.jump_height = 30

            collisions = pygame.sprite.spritecollide(mob, sprite2, False)
            for collision in collisions:
                if ((mob.rect.left - collision.rect.right) < 1) or ((mob.rect.right - collision.rect.left) < 1):
                    mob.rect.x = mob.x
                    
    elif sprite1 == player and sprite2 == coins:
        for collision in sprite2:
            if sprite1.rect.colliderect(collision.rect):
                collision.kill()
                sprite1.add_points()
    elif sprite1 == bullets and sprite2 == blocks:
        hits = pygame.sprite.groupcollide(sprite1, sprite2, True, False)
        for hit in hits:
            hit.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
blocks = pygame.sprite.Group()
coins = pygame.sprite.Group()
# all_sprites.add(mob)
# for i in range(8):
    # m = Mob()
    # all_sprites.add(m)
    # mobs.add(m)

game_map = []
gravity = 3
state = state_start

waiting_command = 0


done = True
while done:
    screen.fill((30, 140, 255))


    if state == state_start:
        if waiting_command < 1:
            # camera variables
            camera_x = 0
            camera_y = 0

            # stable coordinates of the window
            stable_x = 0
            stable_y = 0


            load_game_map()
            for i in range(3):
                mob = Mob(250*(i + 1), 0)
                mobs.add(mob)
                all_sprites.add(mob)
            player = Player()
            all_sprites.add(player)
            gun = Weapon(player.rect.x,player.rect.y)
            all_sprites.add(gun)
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
        waiting_command += 1

    if state == state_play:
        # player.shoot()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # gun.rotate()
                    player.shoot()
        # gun.update(player)
        all_sprites.update()
        collide(player, blocks)
        # print(player.v_speed)
        collide(player, coins)
        collide(bullets, blocks)
        collide(mobs, blocks)

        hits = pygame.sprite.groupcollide(mobs, bullets, False, True)

        for m in hits.keys():
            m.health -= len(hits[m]) * 34
            if m.health <= 0:
                print('sdfasd')
                m.kill()
        # for hit in hits
            # m = Mob()
            # all_sprites.add(m)
        #     mobs.add(m)
        # hits = pygame.sprite.spritecollide(player, mobs, False)
        # if hits:
        #     running = False
        # screen.blit(player.image_right, player.rect)
        for fanta in all_sprites:
            screen.blit(fanta.image, (fanta.rect.x + camera_x, fanta.rect.y + int(camera_y * 0.3)))
        # print(stable_x, stable_y)
        # print(camera_x, camera_y)

        stable_x += camera_x
        stable_y += int(camera_y * 0.3)

        screen.blit(coin, (10, 10), )
        score = font.render(f"{player.get_points()}", True, (255, 204, 0))
        screen.blit(score, (40, -10))
        # all_sprites.draw(screen)


    if state == state_game_over:
        screen.blit(text_game_over, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = state_start
                    waiting_command = 0
                    for sprite in all_sprites:
                        sprite.kill()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()