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
    def __init__(self,x,y,gun):
        self.x = x
        self.y = y
        self.XP = 100
        self.gun = gun

    def death(self):
        if self.XP==0:
            return True
        else:
            return False

# Functions
def load_game_map():
    global game_map
    game_map.clear()
    with open('map.txt', 'r') as f:
        for line in f:
            game_map.append(line)


# NEED TO UPGRADE1: we should use several types of blocks and for each of them assign unique name in game_map, for example block from mario is called 'b' in the game_map.
# NEED TO UPGRADE2: we should save the game_map in another file and call it using techniques like "with open" and so on.

# game_map = [
#     # "                                                  bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb                                                                    ",
#     "                                              bbbbb b                                                                       ",
#     "                                          bbbbbb                                                                            ",
#     "                                       bbbbb                                                                               ",
#     "                                   bbbbb                                                                                   ",
#     "                                bbbb     bbbb                                                                                 ",
#     "         bbb   bb            bbbbb            bbbbbb                                                                                     ",
#     "              b             b                                                                                           ",
#     "            bb             bbb                          bbbbbbbbbb                                                                   ",
#     "          bbbbb     bbbbbb                 bbbbbbbbbb            bbbbbb                                                   ",
#     "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb  bbbb bbbbbbbbbbbbbbb bbbbbbbbbbbbbbbb    bbbbbbbbbbbb      bbbbbbbbbbbbbbbbbbbb",
#     "                                                                                                                      ",
#     "                                                                                                                      ",
# ]

state_start = "welcome"
state_play = "play"
state_game_over = "game over"

# game parameters
size = (1024, 768)
fps = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False
block_size = 42
coin_size = block_size

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
RED = (200, 0, 0)


pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 50, True, False)
text_start = font.render("Press space to start", True, RED)
text_game_over = font.render("Game Over", True, RED)


# load images
# NEED TO UPGRADE: to use our own pictures (more than 5, to make it more realistic (I mean, when he is walking and so on))
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
game_map = []
gravity = 2
state = state_start

while not done:
    screen.fill((30, 140, 255))

    if state == state_start:
        load_game_map()
        camera_x = 0
        camera_y = 0
        player = Player(int(0.22*size[0]), 300, block_size, block_size, 'gun')
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
        rect_player = pygame.Rect(player.x + 5, player.y, block_size - 8, block_size)
        collide = False

        ## rectangles of the blocks in the game_map
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == 'b':
                    rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                    if rect_player.colliderect(rect_block):
                        # we need them to eluminate the residual distances
                        r_from_up = block_size * (i - 1)
                        r_from_below = block_size * (i + 1)
                        collide = True
                if game_map[i][j] == 'c':
                    rect_coin = pygame.Rect(block_size * j, block_size * i, coin_size, coin_size)
                    if rect_player.colliderect(rect_coin):
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
        rect_player = pygame.Rect(player.x, player.y, player.w, player.h)

        ## collide
        collide = False

        ## rectangles of the blocks in the game_map
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == 'b':
                    rect_block = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                    if rect_player.colliderect(rect_block):
                        r_from_left = block_size * (j - 1)
                        r_from_right = block_size * (j + 1)
                        collide = True

                if game_map[i][j] == 'c':
                    rect_coin = pygame.Rect(block_size * j, block_size * i, coin_size, coin_size)
                    if rect_player.colliderect(rect_coin):
                        player.add_points()
                        ### after that player took the coin, the line below removes it from the map
                        game_map[i] = game_map[i][:j] + " " + game_map[i][j + 1:]

        if collide:
            player.x = save_x
            if player.h_speed > 0:
                delta_r_x = r_from_left - save_x
                player.x += delta_r_x
            
            if player.h_speed < 0:
                delta_r_x = save_x - r_from_right
                player.x -= delta_r_x

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




        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if player.jump_is_allowed== True:
                        player.v_speed = -30
                        player.jump_is_allowed= False
                        
                if event.key == pygame.K_LEFT:
                    player.h_speed = -10
                    player.look_left = True

                if event.key == pygame.K_RIGHT:
                    player.h_speed = 10
                    player.look_left = False
                
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if player.h_speed > 0:
                        player.h_speed = 0
                
                if event.key == pygame.K_LEFT:
                    if player.h_speed < 0:
                        player.h_speed = 0

        # blitting the blocks according to the game_map
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == 'b':
                    screen.blit(block1, (block_size * j + camera_x, block_size * i + int(camera_y * 0.3)))
                if game_map[i][j] == 'c':
                    screen.blit(coin, (block_size * j + camera_x, block_size * i + int(camera_y * 0.3)))

        if player.look_left:
            screen.blit(hero_left, (player.x + camera_x, player.y + int(camera_y * 0.3)))
        else:
            screen.blit(hero_right, (player.x + camera_x, player.y + int(camera_y * 0.3)))

        screen.blit(coin, (10, 10))
        score = font.render(f"{player.get_points()}", True, (255,204,0))
        screen.blit(score, (60, 0))
        # screen.blit(mario_right, (player.x + camera_x, player.y + int(camera_y * 0.3)))

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