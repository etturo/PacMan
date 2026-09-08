from enum import Enum, auto


class SpriteType(Enum):
    # WALL SPRITES
    EMPTY_WALL = auto()
    UP_WALL = auto()
    RIGHT_WALL = auto()
    UP_RIGHT_WALL = auto()
    DOWN_WALL = auto()
    VERTICAL_WALL = auto()
    DOWN_RIGHT_WALL = auto()
    VERTICAL_RIGHT_WALL = auto()
    LEFT_WALL = auto()
    UP_LEFT_WALL = auto()
    HORIZONTAL_WALL = auto()
    HORIZONTAL_UP_WALL = auto()
    DOWN_LEFT_WALL = auto()
    VERTICAL_LEFT_WALL = auto()
    HORIZONTAL_DOWN_WALL = auto()
    CROSS_WALL = auto()
    FULL_WALL = auto()

    # FONT SPRITES
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

    # NUMERIC SPRITES
    NUM_0 = auto()
    NUM_1 = auto()
    NUM_2 = auto()
    NUM_3 = auto()
    NUM_4 = auto()
    NUM_5 = auto()
    NUM_6 = auto()
    NUM_7 = auto()
    NUM_8 = auto()
    NUM_9 = auto()

    # SPECIAL CHARACTER SPRITE
    CH_SLASH = auto()
    CH_ESCL = auto()
    CH_LINE = auto()
    CH_CPR = auto()
    CH_DOT = auto()
    CH_QUOTE = auto()
    CH_SPACE = auto()
    CH_COLON = auto()

    # UI SPRITES
    # # CORNERS
    TOP_LEFT = DOWN_RIGHT_WALL
    TOP_RIGHT = DOWN_LEFT_WALL
    BOTTOM_LEFT = UP_RIGHT_WALL
    BOTTOM_RIGHT = UP_LEFT_WALL
    # # EDGES
    HORIZONTAL_EDGE = HORIZONTAL_WALL
    VERTICAL_EDGE = VERTICAL_WALL
    # # SELECTING ARROWS
    LEFT_ARROW = auto()
    RIGHT_ARROW = auto()

    GHOST_EYE_RIGHT_1 = auto()
    GHOST_EYE_RIGHT_2 = auto()
    GHOST_EYE_LEFT_1 = auto()
    GHOST_EYE_LEFT_2 = auto()
    GHOST_EYE_DOWN_1 = auto()
    GHOST_EYE_DOWN_2 = auto()
    GHOST_EYE_UP_1 = auto()
    GHOST_EYE_UP_2 = auto()

    FRIGHTENED_GHOST_1 = auto()
    FRIGHTENED_GHOST_2 = auto()

    PACMAN_RIGHT_1 = auto()
    PACMAN_RIGHT_2 = auto()
    PACMAN_LEFT_1 = auto()
    PACMAN_LEFT_2 = auto()
    PACMAN_DOWN_1 = auto()
    PACMAN_DOWN_2 = auto()
    PACMAN_UP_1 = auto()
    PACMAN_UP_2 = auto()
    PACMAN_FULL = auto()

    PACMAN_DEATH_1 = auto()
    PACMAN_DEATH_2 = auto()
    PACMAN_DEATH_3 = auto()
    PACMAN_DEATH_4 = auto()
    PACMAN_DEATH_5 = auto()
    PACMAN_DEATH_6 = auto()
    PACMAN_DEATH_7 = auto()
    PACMAN_DEATH_8 = auto()
    PACMAN_DEATH_9 = auto()
    PACMAN_DEATH_10 = auto()
    PACMAN_DEATH_11 = auto()
    PACMAN_DEATH_12 = auto()

    LIVES_SPRITE = auto()

    PACGUM = auto()
    SUPER_PACGUMS = auto()

    TWO_HUND_POINTS = auto()
    FOUR_HUND_POINTS = auto()
    EIGHT_HUND_POINTS = auto()
    SIXTEEN_HUND_POINTS = auto()


CHAR_MAPPING: dict[str, SpriteType] = {
    'A': SpriteType.L_A,
    'B': SpriteType.L_B,
    'C': SpriteType.L_C,
    'D': SpriteType.L_D,
    'E': SpriteType.L_E,
    'F': SpriteType.L_F,
    'G': SpriteType.L_G,
    'H': SpriteType.L_H,
    'I': SpriteType.L_I,
    'J': SpriteType.L_J,
    'K': SpriteType.L_K,
    'L': SpriteType.L_L,
    'M': SpriteType.L_M,
    'N': SpriteType.L_N,
    'O': SpriteType.L_O,
    'P': SpriteType.L_P,
    'Q': SpriteType.L_Q,
    'R': SpriteType.L_R,
    'S': SpriteType.L_S,
    'T': SpriteType.L_T,
    'U': SpriteType.L_U,
    'V': SpriteType.L_V,
    'W': SpriteType.L_W,
    'X': SpriteType.L_X,
    'Y': SpriteType.L_Y,
    'Z': SpriteType.L_Z,
    '0': SpriteType.NUM_0,
    '1': SpriteType.NUM_1,
    '2': SpriteType.NUM_2,
    '3': SpriteType.NUM_3,
    '4': SpriteType.NUM_4,
    '5': SpriteType.NUM_5,
    '6': SpriteType.NUM_6,
    '7': SpriteType.NUM_7,
    '8': SpriteType.NUM_8,
    '9': SpriteType.NUM_9,
    '/': SpriteType.CH_SLASH,
    '!': SpriteType.CH_ESCL,
    '-': SpriteType.CH_LINE,
    '©': SpriteType.CH_CPR,
    '.': SpriteType.CH_DOT,
    "\"": SpriteType.CH_QUOTE,
    " ": SpriteType.CH_SPACE,
    ">": SpriteType.RIGHT_ARROW,
    "<": SpriteType.LEFT_ARROW,
    ":": SpriteType.CH_COLON,
}
