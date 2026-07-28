from enum import Enum, auto

import pygame

from src.utils.settings import Settings


class SpriteCoord(tuple[int, int], Enum):
    PACMAN_DEATH_ANIMATION_1_COORDINATES = (1, 134)
    PACMAN_DEATH_ANIMATION_2_COORDINATES = (18, 134)
    PACMAN_DEATH_ANIMATION_3_COORDINATES = (35, 134)
    PACMAN_DEATH_ANIMATION_4_COORDINATES = (52, 134)
    PACMAN_DEATH_ANIMATION_5_COORDINATES = (69, 134)
    PACMAN_DEATH_ANIMATION_6_COORDINATES = (86, 134)

    PACMAN_DEATH_ANIMATION_7_COORDINATES = (1, 151)
    PACMAN_DEATH_ANIMATION_8_COORDINATES = (18, 151)
    PACMAN_DEATH_ANIMATION_9_COORDINATES = (35, 151)
    PACMAN_DEATH_ANIMATION_10_COORDINATES = (52, 151)
    PACMAN_DEATH_ANIMATION_11_COORDINATES = (69, 151)
    PACMAN_DEATH_ANIMATION_12_COORDINATES = (86, 151)

    PACMAN_VERTICAL_STEP_1_COORDINATES = (120, 151)
    PACMAN_VERTICAL_STEP_2_COORDINATES = (120, 134)
    PACMAN_HORIZONTAL_STEP_1_COORDINATES = (103, 151)
    PACMAN_HORIZONTAL_STEP_2_COORDINATES = (103, 134)

    FULL_PACMAN_COORDINATES = (103, 168)
    BLOWN_PACMAN_COORDINATES = (120, 168)

    GHOST_RIGHT_1_COORDINATES = (1, 83)
    GHOST_RIGHT_2_COORDINATES = (18, 83)
    GHOST_LEFT_1_COORDINATES = (69, 83)
    GHOST_LEFT_2_COORDINATES = (86, 83)
    GHOST_UP_1_COORDINATES = (103, 83)
    GHOST_UP_2_COORDINATES = (120, 83)
    GHOST_DOWN_1_COORDINATES = (35, 83)
    GHOST_DOWN_2_COORDINATES = (52, 83)
    FRIGHTENED_GHOST_1_COORDINATES = (1, 168)
    FRIGHTENED_GHOST_2_COORDINATES = (18, 168)

    TWO_H_POINTS_COORDINATES = (35, 168)
    FOUR_H_POINTS_COORDINATES = (52, 168)
    EIGHT_H_POINTS_COORDINATES = (69, 168)
    SIXTEEN_H_POINTS_COORDINATES = (86, 168)

    CHERRIES_COORDINATES = (1, 117)
    STRAWBERRY_COORDINATES = (18, 117)
    PEACH_COORDINATES = (35, 117)
    APPLE_COORDINATES = (52, 117)
    GRAPE_COORDINATES = (69, 117)
    GALAXIAN_COORDINATES = (86, 117)
    BELL_COORDINATES = (103, 117)
    KEY_COORDINATES = (120, 117)


class SmallSpriteCoord(tuple[int, int], Enum):
    NUMBER_ZERO_COORDINATES = (1, 19)
    NUMBER_ONE_COORDINATES = (10, 19)
    NUMBER_TWO_COORDINATES = (19, 19)
    NUMBER_THREE_COORDINATES = (28, 19)
    NUMBER_FOUR_COORDINATES = (37, 19)
    NUMBER_FIVE_COORDINATES = (46, 19)
    NUMBER_SIX_COORDINATES = (55, 19)
    NUMBER_SEVEN_COORDINATES = (64, 19)
    NUMBER_EIGHT_COORDINATES = (73, 19)
    NUMBER_NINE_COORDINATES = (82, 19)

    LETTER_A_COORDINATES = (1, 28)
    LETTER_B_COORDINATES = (10, 28)
    LETTER_C_COORDINATES = (19, 28)
    LETTER_D_COORDINATES = (28, 28)
    LETTER_E_COORDINATES = (37, 28)
    LETTER_F_COORDINATES = (46, 28)
    LETTER_G_COORDINATES = (55, 28)
    LETTER_H_COORDINATES = (64, 28)
    LETTER_I_COORDINATES = (73, 28)
    LETTER_J_COORDINATES = (82, 28)
    LETTER_K_COORDINATES = (91, 28)
    LETTER_L_COORDINATES = (100, 28)
    LETTER_M_COORDINATES = (109, 28)
    LETTER_N_COORDINATES = (1, 37)
    LETTER_O_COORDINATES = (10, 37)
    LETTER_P_COORDINATES = (19, 37)
    LETTER_Q_COORDINATES = (28, 37)
    LETTER_R_COORDINATES = (37, 37)
    LETTER_S_COORDINATES = (46, 37)
    LETTER_T_COORDINATES = (55, 37)
    LETTER_U_COORDINATES = (64, 37)
    LETTER_V_COORDINATES = (73, 37)
    LETTER_W_COORDINATES = (82, 37)
    LETTER_X_COORDINATES = (91, 37)
    LETTER_Y_COORDINATES = (100, 37)
    LETTER_Z_COORDINATES = (109, 37)

    PACGUMS_COORDINATES = (136, 19)
    SUPER_PACGUMS_COORDINATES = (136, 28)

    VERTICAL_WALL_LEFT_COORDINATES = (190, 10)
    VERTICAL_WALL_RIGHT_COORDINATES = (172, 10)


class SpriteType(Enum):
    # NUMBERS
    ZERO = auto()
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    # LETTERS
    L_A = auto()
    L_B = auto()
    L_C = auto()
    L_D = auto()
    L_E = auto()
    L_F = auto()
    L_G = auto()
    L_H = auto()
    L_I = auto()
    L_J = auto()
    L_K = auto()
    L_L = auto()
    L_M = auto()
    L_N = auto()
    L_O = auto()
    L_P = auto()
    L_Q = auto()
    L_R = auto()
    L_S = auto()
    L_T = auto()
    L_U = auto()
    L_V = auto()
    L_W = auto()
    L_X = auto()
    L_Y = auto()
    L_Z = auto()
    # PACMAN DEATH ANIMATION
    PACMAN_DEATH_ANIMATION_1 = auto()
    PACMAN_DEATH_ANIMATION_2 = auto()
    PACMAN_DEATH_ANIMATION_3 = auto()
    PACMAN_DEATH_ANIMATION_4 = auto()
    PACMAN_DEATH_ANIMATION_5 = auto()
    PACMAN_DEATH_ANIMATION_6 = auto()
    PACMAN_DEATH_ANIMATION_7 = auto()
    PACMAN_DEATH_ANIMATION_8 = auto()
    PACMAN_DEATH_ANIMATION_9 = auto()
    PACMAN_DEATH_ANIMATION_10 = auto()
    PACMAN_DEATH_ANIMATION_11 = auto()
    PACMAN_DEATH_ANIMATION_12 = auto()
    # PACMAN WALKING ANIMATION
    PACMAN_VERTICAL_STEP_1 = auto()
    PACMAN_VERTICAL_STEP_2 = auto()
    PACMAN_HORIZONTAL_STEP_1 = auto()
    PACMAN_HORIZONTAL_STEP_2 = auto()
    # PACMAN SPECIAL
    FULL_PACMAN = auto()
    BLOWN_PACMAN = auto()
    # GHOST WALKING ANIMATION
    GHOST_RIGHT_1 = auto()
    GHOST_RIGHT_2 = auto()
    GHOST_LEFT_1 = auto()
    GHOST_LEFT_2 = auto()
    GHOST_UP_1 = auto()
    GHOST_up_2 = auto()
    GHOST_DOWN_1 = auto()
    GHOST_DOWN_2 = auto()
    # FRIGHTENED GHOST ANIMATION
    FRIGHTENED_GHOST_1 = auto()
    FRIGHTENED_GHOST_2 = auto()
    # USER INTERFACE
    TWO_H_POINTS = auto()
    FOUR_H_POINTS = auto()
    EIGHT_H_POINTS = auto()
    SIXTEEN_H_POINTS = auto()
    # FRUITS
    CHERRIES = auto()
    STRAWBERRY = auto()
    PEACH = auto()
    APPLE = auto()
    GRAPE = auto()
    GALAXIAN = auto()
    BELL = auto()
    KEY = auto()
    # PACGUMS
    PACGUMS = auto()
    SUPER_PACGUMS = auto()
    # MAZE WALLS
    # TODO
    VERTICAL_WALL_LEFT = auto()
    VERTICAL_WALL_RIGHT = auto()
    HORIZONTAL_WALL_UP = auto()
    HORIZONTAL_WALL_DOWN = auto()
    VERITCAL_WALL = auto()


class SpriteSheet:
    def __init__(self, filename: str,
                 color_key: tuple[int, int, int] = (0, 0, 0)
                 ) -> None:
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sheet.set_colorkey(color_key)
        self.__data: dict[SpriteType, pygame.Surface] = {}

        self._load_numbers()
        self._load_letters()
        self._load_pacman()
        self._load_ghost()
        self._load_interface()
        self._load_fruits()
        self._load_objects()
        self._load_maze()

    def __getitem__(self, key: SpriteType) -> pygame.Surface:
        return self.__data[key]

    def _extract_and_scale(self,
                           coordinates: SpriteCoord | SmallSpriteCoord
                           ) -> pygame.Surface:
        width: float = Settings.SPRITE_WIDTH
        length: float = Settings.SPRITE_LENGHT

        if isinstance(coordinates, SmallSpriteCoord):
            width = Settings.SMALL_SPRITE_WIDTH
            length = Settings.SMALL_SPRITE_LENGHT

        rect = pygame.Rect(
            coordinates.value[0],
            coordinates.value[1],
            width,
            length)
        raw_surface = self.sheet.subsurface(rect)

        return pygame.transform.scale_by(raw_surface, Settings.DEFAULT_SCALE)

    def _load_numbers(self) -> None:
        self.__data[SpriteType.ZERO] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_ZERO_COORDINATES
        )
        self.__data[SpriteType.ONE] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_ONE_COORDINATES
        )
        self.__data[SpriteType.TWO] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_TWO_COORDINATES
        )
        self.__data[SpriteType.THREE] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_THREE_COORDINATES
        )
        self.__data[SpriteType.FOUR] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_FOUR_COORDINATES
        )
        self.__data[SpriteType.FIVE] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_FIVE_COORDINATES
        )
        self.__data[SpriteType.SIX] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_SIX_COORDINATES
        )
        self.__data[SpriteType.SEVEN] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_SEVEN_COORDINATES
        )
        self.__data[SpriteType.EIGHT] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_EIGHT_COORDINATES
        )
        self.__data[SpriteType.NINE] = self._extract_and_scale(
            SmallSpriteCoord.NUMBER_NINE_COORDINATES
        )

    def _load_letters(self) -> None:
        self.__data[SpriteType.L_A] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_A_COORDINATES
        )
        self.__data[SpriteType.L_B] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_B_COORDINATES
        )
        self.__data[SpriteType.L_C] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_C_COORDINATES
        )
        self.__data[SpriteType.L_D] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_D_COORDINATES
        )
        self.__data[SpriteType.L_E] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_E_COORDINATES
        )
        self.__data[SpriteType.L_F] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_F_COORDINATES
        )
        self.__data[SpriteType.L_G] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_G_COORDINATES
        )
        self.__data[SpriteType.L_H] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_H_COORDINATES
        )
        self.__data[SpriteType.L_I] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_I_COORDINATES
        )
        self.__data[SpriteType.L_J] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_J_COORDINATES
        )
        self.__data[SpriteType.L_K] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_K_COORDINATES
        )
        self.__data[SpriteType.L_L] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_L_COORDINATES
        )
        self.__data[SpriteType.L_M] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_M_COORDINATES
        )
        self.__data[SpriteType.L_N] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_N_COORDINATES
        )
        self.__data[SpriteType.L_O] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_O_COORDINATES
        )
        self.__data[SpriteType.L_P] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_P_COORDINATES
        )
        self.__data[SpriteType.L_Q] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_Q_COORDINATES
        )
        self.__data[SpriteType.L_R] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_R_COORDINATES
        )
        self.__data[SpriteType.L_S] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_S_COORDINATES
        )
        self.__data[SpriteType.L_T] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_T_COORDINATES
        )
        self.__data[SpriteType.L_U] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_U_COORDINATES
        )
        self.__data[SpriteType.L_V] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_V_COORDINATES
        )
        self.__data[SpriteType.L_W] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_W_COORDINATES
        )
        self.__data[SpriteType.L_X] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_X_COORDINATES
        )
        self.__data[SpriteType.L_Y] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_Y_COORDINATES
        )
        self.__data[SpriteType.L_Z] = self._extract_and_scale(
            SmallSpriteCoord.LETTER_Z_COORDINATES
        )

    def _load_pacman(self) -> None:
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_1] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_1_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_2] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_2_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_3] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_3_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_4] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_4_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_5] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_5_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_6] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_6_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_7] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_7_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_8] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_8_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_9] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_9_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_10] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_10_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_11] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_11_COORDINATES
        )
        self.__data[SpriteType.PACMAN_DEATH_ANIMATION_12] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_DEATH_ANIMATION_12_COORDINATES
        )
        self.__data[SpriteType.PACMAN_VERTICAL_STEP_1] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_VERTICAL_STEP_1_COORDINATES
        )
        self.__data[SpriteType.PACMAN_VERTICAL_STEP_2] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_VERTICAL_STEP_2_COORDINATES
        )
        self.__data[SpriteType.PACMAN_HORIZONTAL_STEP_1] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_HORIZONTAL_STEP_1_COORDINATES
        )
        self.__data[SpriteType.PACMAN_HORIZONTAL_STEP_2] = \
            self._extract_and_scale(
                SpriteCoord.PACMAN_HORIZONTAL_STEP_2_COORDINATES
        )
        self.__data[SpriteType.FULL_PACMAN] = \
            self._extract_and_scale(
                SpriteCoord.FULL_PACMAN_COORDINATES
            )
        self.__data[SpriteType.BLOWN_PACMAN] = \
            self._extract_and_scale(
                SpriteCoord.BLOWN_PACMAN_COORDINATES
            )

    def _load_ghost(self) -> None:
        self.__data[SpriteType.GHOST_RIGHT_1] = self._extract_and_scale(
            SpriteCoord.GHOST_RIGHT_1_COORDINATES
        )
        self.__data[SpriteType.GHOST_RIGHT_2] = self._extract_and_scale(
            SpriteCoord.GHOST_RIGHT_2_COORDINATES
        )
        self.__data[SpriteType.GHOST_LEFT_1] = self._extract_and_scale(
            SpriteCoord.GHOST_LEFT_1_COORDINATES
        )
        self.__data[SpriteType.GHOST_LEFT_2] = self._extract_and_scale(
            SpriteCoord.GHOST_LEFT_2_COORDINATES
        )
        self.__data[SpriteType.GHOST_UP_1] = self._extract_and_scale(
            SpriteCoord.GHOST_UP_1_COORDINATES
        )
        self.__data[SpriteType.GHOST_up_2] = self._extract_and_scale(
            SpriteCoord.GHOST_UP_2_COORDINATES
        )
        self.__data[SpriteType.GHOST_DOWN_1] = self._extract_and_scale(
            SpriteCoord.GHOST_DOWN_1_COORDINATES
        )
        self.__data[SpriteType.GHOST_DOWN_2] = self._extract_and_scale(
            SpriteCoord.GHOST_DOWN_2_COORDINATES
        )
        self.__data[SpriteType.FRIGHTENED_GHOST_1] = self._extract_and_scale(
            SpriteCoord.FRIGHTENED_GHOST_1_COORDINATES
        )
        self.__data[SpriteType.FRIGHTENED_GHOST_2] = self._extract_and_scale(
            SpriteCoord.FRIGHTENED_GHOST_2_COORDINATES
        )

    def _load_interface(self) -> None:
        self.__data[SpriteType.TWO_H_POINTS] = self._extract_and_scale(
            SpriteCoord.TWO_H_POINTS_COORDINATES
        )
        self.__data[SpriteType.FOUR_H_POINTS] = self._extract_and_scale(
            SpriteCoord.FOUR_H_POINTS_COORDINATES
        )
        self.__data[SpriteType.EIGHT_H_POINTS] = self._extract_and_scale(
            SpriteCoord.EIGHT_H_POINTS_COORDINATES
        )
        self.__data[SpriteType.SIXTEEN_H_POINTS] = self._extract_and_scale(
            SpriteCoord.SIXTEEN_H_POINTS_COORDINATES
        )

    def _load_fruits(self) -> None:
        self.__data[SpriteType.CHERRIES] = self._extract_and_scale(
            SpriteCoord.CHERRIES_COORDINATES
        )
        self.__data[SpriteType.STRAWBERRY] = self._extract_and_scale(
            SpriteCoord.STRAWBERRY_COORDINATES
        )
        self.__data[SpriteType.PEACH] = self._extract_and_scale(
            SpriteCoord.PEACH_COORDINATES
        )
        self.__data[SpriteType.APPLE] = self._extract_and_scale(
            SpriteCoord.APPLE_COORDINATES
        )
        self.__data[SpriteType.GRAPE] = self._extract_and_scale(
            SpriteCoord.GRAPE_COORDINATES
        )
        self.__data[SpriteType.GALAXIAN] = self._extract_and_scale(
            SpriteCoord.GALAXIAN_COORDINATES
        )
        self.__data[SpriteType.BELL] = self._extract_and_scale(
            SpriteCoord.BELL_COORDINATES
        )
        self.__data[SpriteType.KEY] = self._extract_and_scale(
            SpriteCoord.KEY_COORDINATES
        )

    def _load_objects(self) -> None:
        self.__data[SpriteType.PACGUMS] = self._extract_and_scale(
            SmallSpriteCoord.PACGUMS_COORDINATES
        )
        self.__data[SpriteType.SUPER_PACGUMS] = self._extract_and_scale(
            SmallSpriteCoord.SUPER_PACGUMS_COORDINATES
        )

    def _load_maze(self) -> None:
        self.__data[SpriteType.VERTICAL_WALL_LEFT] = self._extract_and_scale(
            SmallSpriteCoord.VERTICAL_WALL_LEFT_COORDINATES
        )
        self.__data[SpriteType.VERTICAL_WALL_RIGHT] = self._extract_and_scale(
            SmallSpriteCoord.VERTICAL_WALL_RIGHT_COORDINATES
        )
        self.__data[SpriteType.VERITCAL_WALL] = \
            self._combine_sprites_2x2(
                self.__data[SpriteType.VERTICAL_WALL_LEFT],
                self.__data[SpriteType.VERTICAL_WALL_RIGHT],
                self.__data[SpriteType.VERTICAL_WALL_LEFT],
                self.__data[SpriteType.VERTICAL_WALL_RIGHT])

    @staticmethod
    def _combine_sprites_2x2(
            top_left: pygame.Surface,
            top_right: pygame.Surface,
            bottom_left: pygame.Surface,
            bottom_right: pygame.Surface) -> pygame.Surface:

        single_width = top_left.get_width()
        single_height = top_left.get_height()

        total_width = single_width * 2
        total_height = single_height * 2

        combined_surface = pygame.Surface(
            (total_width, total_height),
            pygame.SRCALPHA
        )

        combined_surface.blit(top_left, (0, 0))
        combined_surface.blit(top_right, (single_width, 0))
        combined_surface.blit(bottom_left, (0, single_height))
        combined_surface.blit(bottom_right, (single_width, single_height))

        return combined_surface
