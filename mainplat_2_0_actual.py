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


class Enemy:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.XP = 100

    def death(self):
        if self.XP==0:
            return True
        else:
            return False

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
block_size = 50
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
        gun = Weapon(gun_right, gun_left, player.x, player.y)
        screen.blit(text_start, (50, 50))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = state_play

    if state == state_play:
        # change player.v_speed (gravity)
        player.v_speed = player.v_speed + gravity

        # restriction to not go throw the walls (when landing with big speed)
        if player.v_speed > 28:
            player.v_speed = 28

        # save x and y
        save_x, save_y = player.x, player.y

        # changing y
        player.y += player.v_speed


        # check the collision with respect to y
        ## rectangle of the player
        player.rect = pygame.Rect(player.x, player.y, block_size, block_size)
        rect_gun = pygame.Rect(player.x, player.y, block_size, block_size)
        collide = False

        ## rectangles of the blocks in the game_map
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == 'g' or game_map[i][j] == 'm' or game_map[i][j] == 'b':
                    rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                    if player.rect.colliderect(rect_block):
                        # we need them to eluminate the residual distances
                        r_from_up = block_size * (i - 1)
                        r_from_below = block_size * (i + 1)
                        collide = True
                        player.jump_height = 30
                if game_map[i][j] == 't':
                    rect_tramp = pygame.Rect(block_size * j , trampoline_h + block_size * i, block_size, trampoline_h)
                    if player.rect.colliderect(rect_tramp):
                        # we need them to eluminate the residual distances
                        r_from_up = block_size * (i - 1) + trampoline_h
                        r_from_below = block_size * (i + 1)
                        collide = True
                        player.jump_height = 40
                if game_map[i][j] == 'c':
                    rect_coin = pygame.Rect(coin_size//2 + block_size * j, coin_size//2 + block_size * i, coin_size, coin_size)
                    if player.rect.colliderect(rect_coin):
                        player.add_points()
                        ### after that player took the coin, the line below removes it from the map
                        game_map[i] = game_map[i][:j] + " " + game_map[i][j+1:]

        if collide:
            player.y = save_y
            if player.v_speed > 0:
                delta_r = r_from_up - save_y
                player.y += delta_r
                player.jump_is_allowed = True
            elif player.jump_is_allowed == False and player.v_speed < 0:
                delta_r = save_y - r_from_below
                player.y -= delta_r
                player.v_speed = 0
            else:
                player.v_speed = 0

        else:
            player.jump_is_allowed = False

        if player.y > size[1]:
            state = state_game_over

        # change x
        player.x += player.h_speed
        
        # check the collision with respect to x
        player.rect = pygame.Rect(player.x, player.y, player.w, player.h)
        rect_gun = pygame.Rect(player.x, player.y, block_size, block_size)

        ## collide
        collide = False

        ## rectangles of the blocks in the game_map
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == 'g' or game_map[i][j] == 'm' or game_map[i][j] == 'b':
                    rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                    if player.rect.colliderect(rect_block):
                        # r_from_left = block_size * (j - 1)
                        # r_from_right = block_size * (j + 1)
                        collide = True
                        player.jump_height = 30
                if game_map[i][j] == 't':
                    rect_tramp = pygame.Rect(block_size * j, trampoline_h + block_size * i, block_size, trampoline_h)
                    if player.rect.colliderect(rect_tramp):
                        # we need them to eluminate the residual distances
                        # r_from_left = block_size * (j - 1)
                        # r_from_right = block_size * (j + 1)
                        collide = True
                        player.jump_height = 40
                if game_map[i][j] == 'c':
                    rect_coin = pygame.Rect(coin_size//2 + block_size * j, coin_size//2 + block_size * i, coin_size, coin_size)
                    if player.rect.colliderect(rect_coin):
                        player.add_points()
                        ### after that player took the coin, the line below removes it from the map
                        game_map[i] = game_map[i][:j] + " " + game_map[i][j + 1:]

        if collide:
            player.x = save_x
            # if player.h_speed > 0:
            #     delta_r_x = r_from_left - save_x
            #     player.x += delta_r_x
            #
            # if player.h_speed < 0:
            #     delta_r_x = save_x - r_from_right
            #     player.x -= delta_r_x

        # moving camera in x direction
        if player.x + camera_x > size[0]*0.8:
            camera_x -= 10
        if player.x + camera_x < size[0]*0.2:
            camera_x += 10

        # moving camera in y direction
        # if player.y + camera_y > size[1]*0.8:
            # camera_y -= 10
        # if player.y + camera_y < size[1]*0.5:
            # camera_y += 10
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
            screen.blit(gun.image_left, (player.x - block_size/2 + camera_x, player.y - block_size/2 + int(camera_y * 0.3)))
        else:
            screen.blit(player.image_right, (player.x + camera_x, player.y + int(camera_y * 0.3)))
            screen.blit(gun.image_right, (player.x - block_size/2 + camera_x, player.y - block_size/2 + int(camera_y * 0.3)))

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