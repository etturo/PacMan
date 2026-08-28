import random

import pygame

from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.utils.settings import Settings

class ScreenManager:
    def __init__(self) -> None:
        pygame.init()

        self.__virtual_screen_width = Settings.VIRTUAL_WINDOW_WIDTH
        self.__virtual_screen_height = Settings.VIRTUAL_WINDOW_HEIGHT

        self.__screen = pygame.display.set_mode(
            (self.__virtual_screen_width, self.__virtual_screen_height),
            pygame.FULLSCREEN | pygame.SCALED | pygame.RESIZABLE
        )
        pygame.display.set_caption('PacMan')

        self.__crt_overlay = self._apply_crt_overlay()

        self.__is_fullscreen = True

        SpriteLibrary.load()
        SpriteLibrary.add_item('title', 'white_text')
        SpriteLibrary.add_item('wall_skins', 'blue')

    def _apply_crt_overlay(self) -> pygame.Surface:
        overlay = pygame.Surface(
            (self.__virtual_screen_width, self.__virtual_screen_height),
            pygame.SRCALPHA
        )

        for y in range(0, self.__virtual_screen_height, 3):
            pygame.draw.line(
                overlay,
                (0, 0, 0, 70),
                (0, y),
                (self.__virtual_screen_width, y)
            )

        return overlay

    def _apply_glow(self):
        glow_surf = pygame.transform.smoothscale(
            self.__screen,
            (self.__virtual_screen_width // 2,
            self.__virtual_screen_height // 2)
            )
        glow_surf = pygame.transform.smoothscale(
            glow_surf,
            (self.__virtual_screen_width,
            self.__virtual_screen_height)
            )
        glow_surf.set_alpha(100)
        self.__screen.blit(glow_surf, (0, 0))

    def _add_glitch_effect(self):
        intensity = "minimum"
        shift_amount = {"minimum": 10, "medium": 20, "maximum": 40}.get(intensity, 20)
        
        if random.random() < 0.05:
            y_start = random.randint(0, self.__virtual_screen_height - 20)
            slice_height = random.randint(5, 20)
            offset = random.randint(-shift_amount, shift_amount)

            slice_area = pygame.Rect(0, y_start, self.__virtual_screen_width, slice_height)
            slice_copy = self.__screen.subsurface(slice_area).copy()

            self._add_color_separation(slice_copy, intensity)
            
            self.__screen.blit(slice_copy, (offset, y_start))

    def _add_color_separation(self, glitch_surface, intensity) -> None:
        color_shift = {"minimum": 2, "medium": 6, "maximum": 10}.get(intensity, 4)
        
        if random.random() < 0.5:
            for _ in range(3):
                x_offset = random.randint(-color_shift, color_shift)
                y_offset = random.randint(-color_shift, color_shift)
                
                color_shift_surface = glitch_surface.copy()
                color_shift_surface.fill((0, 0, 0))
                color_shift_surface.blit(glitch_surface, (x_offset, y_offset))
                
                glitch_surface.blit(color_shift_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    def _add_rolling_static(self):
        intensity = "minimum"
        static_chance = {"minimum": 0.0001, "medium": 0.3, "maximum": 0.8}.get(intensity, 0.2)
        static_surface = pygame.Surface(
            (self.__virtual_screen_width,
            self.__virtual_screen_height),
            pygame.SRCALPHA
            )

        for y in range(0, self.__virtual_screen_height, 8):
            if random.random() < static_chance:
                pygame.draw.line(
                    static_surface,
                    (255, 255, 255, random.randint(30, 80)),
                    (0, y),
                    (self.__virtual_screen_width, y)
                    )

        self.__screen.blit(static_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    def _generate_flicker_overlay(self) -> None:
        if random.randint(0, 20) == 0:
            flicker = pygame.Surface(
                (self.__virtual_screen_width, self.__virtual_screen_height),
                pygame.SRCALPHA
                )
            flicker.fill((255, 255, 255, 5))
            self.__screen.blit(flicker, (0, 0))

    def getScreen(self) -> pygame.Surface:
        return self.__screen

    def render(
            self,
            surface: pygame.Surface,
            crt: bool = True,
            flicker: bool = True,
            glow: bool = True,
            glitch: bool = True,
            rolling: bool = True,
        ) -> None:
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(surface, (0, 0))

        if glitch:
            self._add_glitch_effect()
        if rolling:
            self._add_rolling_static()
        if flicker:
            self._generate_flicker_overlay()
        if glow:
            self._apply_glow()
        if crt:
            self.__screen.blit(self.__crt_overlay, (0, 0))

        pygame.display.flip()