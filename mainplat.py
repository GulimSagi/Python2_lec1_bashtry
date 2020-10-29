import pygame

pygame.init()
size = (1024, 768)
fps = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False
block_size = 64

# load images
mario_right = pygame.image.load('mario_right.png')

#music



# standartize the size
mario_right = pygame.transform.scale(mario_right, (block_size, block_size))

# game variables
x = 150
y = 410
dy = -5
dx = 0
gravity = 2
jump_is_allowed = False


while not done:
    screen.fill((30, 140, 255))
    rect1 = pygame.draw.rect(screen, (245,123,12),(0, 400, 1024, 3), 5)

    dy = dy + gravity
    y += dy

    if y > 400 - block_size:
        y = 400 - block_size
        jump_is_allowed = True



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if jump_is_allowed == True:
                    dy = -25
                    jump_is_allowed = False

    screen.blit(mario_right, (x, y))
    # screen.blit(rect1, (0, 400))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
