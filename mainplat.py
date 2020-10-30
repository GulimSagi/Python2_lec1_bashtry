import pygame

# game parameters
pygame.init()
size = (1024, 768)
fps = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False
block_size = 42

class Player:
    def __init__(self,x,y,gun):
        self.x=x
        self.y=y
        self.XP=100
        self.gun=gun

    def death(self):
        if self.XP==0:
            return True
        else:
            return False

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


# NEED TO UPGRADE1: we should use several types of blocks and for each of them assign unique name in map, for example block from mario is called 'b' in the map.
# NEED TO UPGRADE2: we should save the map in another file and call it using techniques like "with open" and so on.
map = [
    "                                                                                                                      ",
    "                                                                                                                      ",
    "                                                                                                                      ",
    "                                                                                                                      ",
    "                                                                                                                      ",
    "                                                                                                                      ",
    "         bbb bb                                                                                                             ",
    "                           b                                                                                           ",
    "                                                                                                                      ",
    "          bbbbb     bbbbbb                 bbbbbbbbbb            bbbbbb                                                   ",
    "bbbb bbbbbbbbbbbbbbbbbbbbbbbbbb      bbbb bbbbbbbbbbbbbbb bbbbbbbbbbbbbbbb    bbbbbbbbbbbb      bbbbbbbbbbbbbbbbbbbb",
    "                                                                                                                      ",
    "                                                                                                                      ",
]

# load images
# NEED TO UPGRADE: to use our own pictures (more than 5, to make it more realistic (I mean, when he is walking and so on))
mario_right = pygame.image.load('mario_right.png')
block1 = pygame.image.load('mario_block.png')

# standartize the size
mario_right = pygame.transform.scale(mario_right, (block_size, block_size))
block1 = pygame.transform.scale(block1, (block_size, block_size))


# game variables

dy = -5
dx = 0
gravity = 3
jump_is_allowed = False

mario = Player(150, 300,  'gun')

while not done:
    screen.fill((30, 140, 255))

    # change dy (gravity)
    dy = dy + gravity

    # restriction to not go throw the walls (when landing with big speed)
    if dy > 40:
        dy = 40

    # save x and y
    save_x, save_y = mario.x, mario.y

    # changing y
    mario.y += dy


    # check the collision with respect to y
    ## rectangle of the player
    rect1 = pygame.Rect(mario.x, mario.y, block_size, block_size)
    collide = False

    ## rectangles of the blocks in the map
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'b':
                rect2 = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                if rect1.colliderect(rect2):
                    # we need them to eluminate the residual distances
                    r_from_up = block_size * (i - 1)
                    r_from_below = block_size * (i + 1)
                    collide = True


    if collide:
        mario.y = save_y
        if dy > 0:
            delta_r = r_from_up - save_y
            mario.y += delta_r
            jump_is_allowed = True
        elif jump_is_allowed == False and dy < 0:
            delta_r = save_y - r_from_below + 1
            mario.y -= delta_r
            dy = 0
        else:
            dy = 0


    # change x
    mario.x += dx
    
    # check the collision with respect to x
    rect1 = pygame.Rect(mario.x, mario.y, block_size, block_size)

    ## collide
    collide = False

    ## rectangles of the blocks in the map
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'b':
                rect2 = pygame.Rect(block_size * j, block_size * i, block_size, block_size)
                if rect1.colliderect(rect2):
                    collide = True

    if collide:
        mario.x = save_x


    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if jump_is_allowed == True:
                    dy = -35
                    jump_is_allowed = False

            if event.key == pygame.K_RIGHT:
                dx = 4
            
            if event.key == pygame.K_LEFT:
                dx = -4
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if dx > 0:
                    dx = 0
            
            if event.key == pygame.K_LEFT:
                if dx < 0:
                    dx = 0

    # blitting the blocks according to the map
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'b':
                screen.blit(block1, (block_size * j, block_size * i))
    screen.blit(mario_right, (mario.x, mario.y))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()


#### UPDATE 30.10.2020, 19:17 BY ALIBEK.
#### THE MAIN UPDATE: now Mario lands correctly and there is no any space between his legs and the groung 
#### PROBLEM (ACTUALLY IT IS NOT BUT...) : If I set the restriction to bigger values (line 59 and line 60) Mario will go jump through the block --- I DON'T KNOW WHY, but have some guesses

##### TASK1 OT GULIM: КОРОЧЕ МАРИО ДОЛЖЕН СТРЕЛЯТЬ USING SPRITE (TO READ AND TO DO)
##### TASK2 ВРАГИ ДОЛЖНЫ УМЕТЬ СТРЕЛЯТЬ ТОЖЕ
# ANIMATION 'RUNNING', 'WALKING' READ
# SAVE MAPS IN THE OTHER FILE AND CALL IT BY TECHNIQUE LIKE "with open 'r'"
# ROTATION OF GUN
#MAIN PAGE 