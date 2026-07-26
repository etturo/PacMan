import pygame
from src.sprite_sheet import SpriteSheet

pygame.init()
screen = pygame.display.set_mode((800, 600))

red_sprite_sheet = SpriteSheet("assets/sprites/red-sprite-sheet.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    screen.blit(red_sprite_sheet['one'], (100, 300))
    screen.blit(red_sprite_sheet['two'], (200, 300))
    screen.blit(red_sprite_sheet['three'], (300, 300))
    screen.blit(red_sprite_sheet['four'], (400, 300))
    screen.blit(red_sprite_sheet['five'], (500, 300))

    pygame.display.flip()

pygame.quit()
