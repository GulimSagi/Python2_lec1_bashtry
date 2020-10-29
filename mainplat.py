import pygame

pygame.init()
size = (1024, 768)
fps = 20
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False
block_size = 64

# load images
mario_right = pygame.image.load('mario_right.png')

# standartize the size
mario_right = pygame.transform.scale(mario_right, (block_size, block_size))

while not done:
    screen.fill((30, 140, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(mario_right, (50, 50))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
