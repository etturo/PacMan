import pygame

from src.sprite_sheet import SpriteSheet, SpriteType

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PacMan')

red_sprite_sheet = SpriteSheet("assets/sprites/red-sprite-sheet.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    screen.blit(red_sprite_sheet[SpriteType.ZERO], (100, 300))
    screen.blit(red_sprite_sheet[SpriteType.ONE], (200, 300))
    screen.blit(red_sprite_sheet[SpriteType.TWO], (300, 300))
    screen.blit(red_sprite_sheet[SpriteType.THREE], (400, 300))
    screen.blit(red_sprite_sheet[SpriteType.FOUR], (500, 300))

    pygame.display.flip()

pygame.quit()
