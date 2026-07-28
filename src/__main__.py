import pygame

from src.sprite_sheet import SpriteSheet, SpriteType

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PacMan')

red_sprite_sheet = SpriteSheet("data/assets/sprites/red-sprite-sheet.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    screen.blit(red_sprite_sheet[SpriteType.TWO_H_POINTS], (100, 300))
    screen.blit(red_sprite_sheet[SpriteType.KEY], (200, 300))
    screen.blit(red_sprite_sheet[SpriteType.PACGUMS], (300, 300))
    screen.blit(red_sprite_sheet[SpriteType.GHOST_RIGHT_1], (400, 300))
    screen.blit(red_sprite_sheet[SpriteType.GHOST_UP_1], (500, 300))

    pygame.display.flip()

pygame.quit()
