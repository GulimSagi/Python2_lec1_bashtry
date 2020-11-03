import pygame
import math
pygame.init()

#Classes
class Player():
    def __init__(self,image_right, image_left, x, y, w, h):
        self.image_right = image_right
        self.image_left = image_left
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.old_x = 0
        self.old_y = 0
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 30
        self.jump_is_allowed = False
        self.look_left = False
        self.XP = 100
        self.points = 0
        self.get_coins = False

    def death(self):
        if self.XP == 0:
            return True
        else:
            return False

    def add_points(self):
        self.points += 1

    def get_points(self):
        return self.points


class Enemy:
    def __init__(self,image_right, image_left, x, y, w, h):
        self.image_right = image_right
        self.image_left = image_left
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.old_x = 0
        self.old_y = 0
        self.v_speed = -5
        self.h_speed = 0
        self.jump_height = 30
        self.jump_is_allowed = False
        self.look_left = False
        self.XP = 100
        self.points = 0

    def death(self):
        if self.XP == 0:
            return True
        else:
            return False

    def add_points(self):
        self.points += 1

    def get_points(self):
        return self.points

class Weapon:
    def __init__(self, image_right, image_left, x, y):
        self.x = x
        self.y = y
        self.look_left = False
        self.image_right = image_right
        self.image_left = image_left
        self.rect = self.image_right.get_rect(center=(self.x, self.y))

    def rotate(self, image):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if image == gun.image_left:
            self.image = pygame.transform.rotate(image, int(-angle))
        else:
            self.image = pygame.transform.rotate(image, int(angle))
        self.rect = self.image.get_rect(center=(self.x, self.y))


# Functions
def load_game_map():
    global game_map
    game_map.clear()
    with open('map.txt', 'r') as f:
        for line in f:
            game_map.append(line)

def check_collide_y(x, y, old_x, old_y, v_speed, jump_height, block_size, trampoline_h, jump_is_allowed):
    # check the collision with respect to y
    ## rectangle of the player
    rect_character = pygame.Rect(x + 5, y, block_size - 8, block_size)
    collide = False
    get_coins = False
    death = False

    ## rectangles of the blocks in the game_map
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            if game_map[i][j] == 'g' or game_map[i][j] == 'm' or game_map[i][j] == 'b':
                rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                if rect_character.colliderect(rect_block):
                    # we need them to eluminate the residual distances
                    r_from_up = block_size * (i - 1)
                    r_from_below = block_size * (i + 1)
                    collide = True
                    jump_height = 30
            if game_map[i][j] == 't':
                rect_tramp = pygame.Rect(block_size * j , trampoline_h + block_size * i, block_size, trampoline_h)
                if rect_character.colliderect(rect_tramp):
                    # we need them to eluminate the residual distances
                    # r_from_up = block_size * (i - 1) + trampoline_h
                    # r_from_below = block_size * (i + 1)
                    # collide = True
                    jump_height = 40
            if game_map[i][j] == 'c':
                rect_coin = pygame.Rect(coin_size//2 + block_size * j, coin_size//2 + block_size * i, coin_size, coin_size)
                if rect_character.colliderect(rect_coin):
                    get_coins = True
                    ### after that player took the coin, the line below removes it from the map
                    game_map[i] = game_map[i][:j] + " " + game_map[i][j+1:]

    if collide:
        y = old_y
        if v_speed > 0:
            delta_r = r_from_up - old_y
            y += delta_r
            jump_is_allowed = True
        elif jump_is_allowed == False and v_speed < 0:
            delta_r = old_y - r_from_below
            y -= delta_r
            v_speed = 0
        else:
            v_speed = 0

    else:
        jump_is_allowed = False

    if y > size[1]:
        death = True

    return x, y, v_speed, jump_height, death, jump_is_allowed, get_coins


def check_collide_x(x, y, old_x, old_y, h_speed, jump_height, block_size, trampoline_h, jump_is_allowed):
    rect_character = pygame.Rect(x, y, block_size, block_size)

    ## collide
    collide = False
    get_coins = False

    ## rectangles of the blocks in the game_map
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            if game_map[i][j] == 'g' or game_map[i][j] == 'm' or game_map[i][j] == 'b':
                rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                if rect_character.colliderect(rect_block):
                    r_from_left = block_size * (j - 1)
                    r_from_right = block_size * (j + 1)
                    collide = True
                    jump_height = 30
            if game_map[i][j] == 't':
                rect_tramp = pygame.Rect(block_size * j, trampoline_h + block_size * i, block_size, trampoline_h)
                if rect_character.colliderect(rect_tramp):
                    # we need them to eluminate the residual distances
                    # r_from_left = block_size * (j - 1)
                    # r_from_right = block_size * (j + 1)
                    # collide = True
                    jump_height = 40
            if game_map[i][j] == 'c':
                rect_coin = pygame.Rect(coin_size//2 + block_size * j, coin_size//2 + block_size * i, coin_size, coin_size)
                if rect_character.colliderect(rect_coin):
                    get_coins = True
                    ### after that player took the coin, the line below removes it from the map
                    game_map[i] = game_map[i][:j] + " " + game_map[i][j + 1:]

    if collide:
        x = old_x
        if h_speed > 0:
            delta_r_x = r_from_left - old_x
            x += delta_r_x
        
        if h_speed < 0:
            delta_r_x = old_x - r_from_right
            x -= delta_r_x

    return x, y, h_speed, jump_height, jump_is_allowed, get_coins
    

    


# NEED TO UPGRADE1: we should use several types of blocks and for each of them assign unique name in game_map, for example block from mario is called 'b' in the game_map.

state_start = "welcome"
state_play = "play"
state_game_over = "game over"

# game parameters
size = (1024, 768)
fps = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False
block_size = 52
gun_size = block_size*2
coin_size = block_size//2
trampoline_h = block_size//2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
RED = (200, 0, 0)

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 40, True, False)
text_start = font.render("Press space to start", True, RED)
text_game_over = font.render("Game Over", True, RED)

# load images
# NEED TO UPGRADE: to use our own pictures (more than 5, to make it more realistic (I mean, when he is walking and so on))
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

# standartize the size
hero_right = pygame.transform.scale(hero_right, (block_size, block_size))
hero_left = pygame.transform.scale(hero_left, (block_size, block_size))
ground = pygame.transform.scale(ground, (block_size, block_size))
mud = pygame.transform.scale(mud, (block_size, block_size))
brick = pygame.transform.scale(brick, (block_size, block_size))
trampoline = pygame.transform.scale(trampoline, (block_size, trampoline_h))
coin = pygame.transform.scale(coin, (coin_size, coin_size))
gun_right = pygame.transform.scale(gun_right, (gun_size, gun_size))
gun_left = pygame.transform.scale(gun_left, (gun_size, gun_size))
enemy1_left = pygame.transform.scale(enemy1_left, (block_size, block_size))
enemy1_right = pygame.transform.scale(enemy1_right, (block_size, block_size))


# game variables
game_map = []
gravity = 2
state = state_start

while not done:
    screen.fill((30, 140, 255))

    if state == state_start:
        load_game_map()
        camera_x = 0
        camera_y = 0
        player = Player(hero_right, hero_left, 100, 300, block_size, block_size)
        enemy1 = Enemy(enemy1_right, enemy1_left, 500, 200, block_size, block_size)
        gun = Weapon(gun_right, gun_left, player.x, player.y)
        screen.blit(text_start, (50, 50))
        charachters = [player, enemy1]
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = state_play

    if state == state_play:
        for charachter in charachters:

            # change player.v_speed (gravity)
            charachter.v_speed = charachter.v_speed + gravity

            # restriction to not go throw the walls (when landing with big speed)
            if charachter.v_speed > 25:
                charachter.v_speed = 25

        # save x and y
        for charachter in charachters:
            charachter.old_x, charachter.old_y = charachter.x, charachter.y

            
            charachter.y += charachter.v_speed
            charachter.x, charachter.y, charachter.v_speed, charachter.jump_height, charachter.death, charachter.jump_is_allowed, charachter.add_pionts = check_collide_y(charachter.x, charachter.y, charachter.old_x, charachter.old_y, charachter.v_speed, charachter.jump_height, block_size, trampoline_h, charachter.jump_is_allowed)        
            if charachter == player and charachter.get_coins == True:
                charachter.add_points()
            if charachter.death == True:
                state = state_game_over

            charachter.x += charachter.h_speed
            charachter.x, charachter.y, charachter.h_speed, charachter.jump_height, charachter.jump_is_allowed, charachter.get_coins = check_collide_x(charachter.x, charachter.y, charachter.old_x, charachter.old_y, charachter.h_speed, charachter.jump_height, block_size, trampoline_h, charachter.jump_is_allowed)        
            if charachter.get_coins == True:
                charachter.add_points()

        # moving camera in x direction
        if player.x + camera_x > size[0]*0.65:
            camera_x -= 10
        if player.x + camera_x < size[0]*0.35:
            camera_x += 10

        # moving camera in y direction
        camera_y = -player.y + size[1] * 0.5

        # blitting the blocks according to the game_map
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == 'g':
                    screen.blit(ground, (block_size * j + camera_x, block_size * i + int(camera_y * 0.3)))
                if game_map[i][j] == 'm':
                    screen.blit(mud, (block_size * j + camera_x, block_size * i + int(camera_y * 0.3)))
                if game_map[i][j] == 'b':
                    screen.blit(brick, (block_size * j + camera_x, block_size * i + int(camera_y * 0.3)))
                if game_map[i][j] == 't':
                    screen.blit(trampoline, (block_size * j + camera_x, trampoline_h + block_size * i + int(camera_y * 0.3)))
                if game_map[i][j] == 'c':
                    screen.blit(coin, (coin_size//2 + block_size * j + camera_x, coin_size//2 + block_size * i + int(camera_y * 0.3)))

        if player.look_left:
            screen.blit(player.image_left, (player.x + camera_x, player.y + int(camera_y * 0.3)))
            screen.blit(gun.image_left, (player.x - block_size//2 + camera_x, player.y - block_size//2 + int(camera_y * 0.3)))
        else:
            screen.blit(player.image_right, (player.x + camera_x, player.y + int(camera_y * 0.3)))
            screen.blit(gun.image_right, (player.x - block_size//2 + camera_x, player.y - block_size//2 + int(camera_y * 0.3)))


        screen.blit(enemy1.image_left, (enemy1.x + camera_x, enemy1.y + int(camera_y * 0.3)))
        screen.blit(coin, (10, 10), )
        score = font.render(f"{player.get_points()}", True, (255,204,0))
        screen.blit(score, (40, -10))

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if gun.look_left:
                        gun.rotate(gun.image_left)
                    else:
                        gun.rotate(gun.image_right)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if player.jump_is_allowed == True:
                        player.v_speed = -player.jump_height
                        player.jump_is_allowed = False

                if event.key == pygame.K_LEFT:
                    player.h_speed = -10
                    player.look_left = True
                    gun.look_left = True

                if event.key == pygame.K_RIGHT:
                    player.h_speed = 10
                    player.look_left = False
                    gun.look_left = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if player.h_speed > 0:
                        player.h_speed = 0

                if event.key == pygame.K_LEFT:
                    if player.h_speed < 0:
                        player.h_speed = 0

    if state == state_game_over:
        screen.blit(text_game_over, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = state_start


    pygame.display.flip()
    clock.tick(fps)

pygame.quit()


#### UPDATE 30.10.2020, 19:17 BY ALIBEK.
#### THE MAIN UPDATE: now Mario lands correctly and there is no any space between his legs and the groung 
#### PROBLEM (ACTUALLY IT IS NOT BUT...) : If I set the restriction to bigger values (line 59 and line 60) Mario will go jump through the block --- I DON'T KNOW WHY, but have some guesses

##### TASK1 OT GULIM: КОРОЧЕ МАРИО ДОЛЖЕН СТРЕЛЯТЬ USING SPRITE (TO READ AND TO DO)
##### TASK2 ВРАГИ ДОЛЖНЫ УМЕТЬ СТРЕЛЯТЬ ТОЖЕ
# ANIMATION 'RUNNING', 'WALKING' READ
# SAVE game_mapS IN THE OTHER FILE AND CALL IT BY TECHNIQUE LIKE "with open 'r'"
# ROTATION OF GUN
#MAIN PAGE 