import pygame
pygame.init()

#Classes
class Player:
    def __init__(self, x, y, w, h, gun):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v_speed = -5
        self.h_speed = 0
        self.jump_is_allowed = False
        self.look_left = False
        self.XP = 100
        self.points = 0
        self.gun = gun

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
    def __init__(self, x, y, gun):
        self.x = x
        self.y = y
        self.XP = 100
        self.gun = gun

    def death(self):
        if self.XP == 0:
            return True
        else:
            return False

# Functions
def load_map():
    global map
    map.clear()
    with open('map.txt', 'r') as f:
        for line in f:
            map.append(line)

# Level
# map = [
#     "                                    ccccc                                                                             ",
#     "                            cccc    bbbbb                                                                             ",
#     "                            bbbb                                                                                      ",
#     "                       ccc                ccccccc                                                                     ",
#     "         ccc  ccc      bbb                bbbbbbb                                                                     ",
#     "         bbb  bbb               ccc       b ccc b      cccccc                                                         ",
#     "                                bbb       b     b      bbbbbb                                                         ",
#     "          ccccc    cccccc                 cccccccccc            cccccc                                                ",
#     "     cccccbbbbbccccbbbbbbcccccc      cccc bbbbbbbbbbccccc ccccccbbbbbbcccc                                            ",
#     "bbbb bbbbbbbbbbbbbbbbbbbbbbbbbb      bbbb bbbbbbbbbbbbbbb bbbbbbbbbbbbbbbb    bbbbbbbbbbbb     bbbbbbbbbbbbbbbbbbbb   ",
#     "                                                                                                                      ",
#     "                                                                                                                      ",
# ]

state_start = "welcome"
state_play = "play"
state_game_over = "game over"

size = (1024, 768)
fps = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
RED = (200, 0, 0)

block_size = 50
coin_size = block_size

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 50, True, False)
text_start = font.render("Press space to start", True, RED)
text_game_over = font.render("Game Over", True, RED)

# load images
hero_right = pygame.image.load('mario_right.png')
hero_left = pygame.image.load('mario_left.png')
block1 = pygame.image.load('mario_block.png')
coin = pygame.image.load('coin.png')

# standartize the size
hero_right = pygame.transform.scale(hero_right, (block_size, block_size))
hero_left = pygame.transform.scale(hero_left, (block_size, block_size))
block1 = pygame.transform.scale(block1, (block_size, block_size))
coin = pygame.transform.scale(coin, (coin_size, coin_size))

# game variables
map = []
gravity = 3
done = False
state = state_start

while not done:
    screen.fill((30, 140, 255))

    if state == state_start:
        load_map()
        camera_x = 0
        camera_y = 0
        player = Player(100, 0, 50, 50, 'gun')
        screen.blit(text_start, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = state_play

    if state == state_play:
        player.v_speed += gravity

        if player.v_speed > 20:
            player.v_speed = 20

        # save x and y
        save_x, save_y = player.x, player.y
        player.y += player.v_speed

        rect_player = pygame.Rect(player.x, player.y, player.w, player.h)
        collide = False

        # rectangles of the blocks in the map
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 'b':
                    rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                    if rect_player.colliderect(rect_block):
                        collide = True
                        r_from_up = block_size * (i - 1)
                        r_from_below = block_size * (i + 1)
                if map[i][j] == 'c':
                    rect_coin = pygame.Rect(block_size * j, block_size * i, coin_size, coin_size)
                    if rect_player.colliderect(rect_coin):
                        player.add_points()
                        map[i] = map[i][:j] + " " + map[i][j+1:]

        if collide:
            player.y = save_y
            if player.v_speed > 0:
                player.y += r_from_up - save_y
                player.jump_is_allowed = True
            elif player.v_speed < 0 and player.jump_is_allowed == False:
                player.y -= save_y - r_from_below + 1
                player.v_speed = 0
            else:
                player.v_speed = 0

        if player.y > size[1]:
            state = state_game_over

        player.x += player.h_speed

        rect_player = pygame.Rect(player.x, player.y, player.w, player.h)
        collide = False

        # rectangles of the blocks in the map
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 'b':
                    rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                    if rect_player.colliderect(rect_block):
                        collide = True
                        r_from_up = block_size * (i - 1)
                        r_from_below = block_size * (i + 1)
                if map[i][j] == 'c':
                    rect_coin = pygame.Rect(block_size * j, block_size * i, coin_size, coin_size)
                    if rect_player.colliderect(rect_coin):
                        player.add_points()
                        map[i] = map[i][:j] + " " + map[i][j + 1:]

        if collide:
            player.x = save_x

        if player.x + camera_x > size[0]*0.7:
            camera_x = camera_x - 10
        if player.x + camera_x < size[0]*0.3:
            camera_x = camera_x + 10
        # if player.y + camera_y > size[1]*0.1:
        #     camera_y = camera_y - 10
        # if player.y + camera_y < size[1]*0.6:
        #     camera_y = camera_y + 10
        camera_y = -player.y + size[1] * 0.5

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if player.jump_is_allowed == True:
                        player.v_speed = -40
                        player.jump_is_allowed = False

                if event.key == pygame.K_RIGHT:
                    player.h_speed = 10
                    player.look_left = False

                if event.key == pygame.K_LEFT:
                    player.h_speed = -10
                    player.look_left = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if player.h_speed > 0:
                        player.h_speed = 0

                if event.key == pygame.K_LEFT:
                    if player.h_speed < 0:
                        player.h_speed = 0

        # blitting the blocks according to the map
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 'b':
                    screen.blit(block1, (block_size * j + camera_x, block_size * i + camera_y))
                if map[i][j] == 'c':
                    screen.blit(coin, (block_size * j + camera_x, block_size * i + camera_y))

        if player.look_left:
            screen.blit(hero_left, (player.x + camera_x, player.y + camera_y))
        else:
            screen.blit(hero_right, (player.x + camera_x, player.y + camera_y))

        screen.blit(coin, (10, 10))
        score = font.render(f"{player.get_points()}", True, (255,204,0))
        screen.blit(score, (60, 0))

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