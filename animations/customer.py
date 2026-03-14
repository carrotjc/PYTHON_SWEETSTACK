import pygame
import math
from settings import (
    CUSTOMER_TARGET_X, CUSTOMER_START_X,
    CUSTOMER_Y, CUSTOMER_SIZE, CUSTOMER_WALK_SPEED,
)

REACTIONS = {
    "hello":      ("assets/customers/hello.png",      (1157, 414), (70,  65),  90),
    "heart":      ("assets/customers/heart.png",      (1151, 389), (78,  72), 110),
    "huh":        ("assets/customers/huh.png",        (1145, 398), (83,  65), 110),
    "frustrated": ("assets/customers/frustrated.png", (1172, 389), (57,  72), 110),
}


class CustomerAnimator:

    def __init__(self):
        self.image        = None
        self.cx           = float(CUSTOMER_START_X)
        self.walking      = False
        self.walking_out  = False
        self.walked_out   = False
        self.float_time   = 0.0
        self.float_offset = 0.0

        # Reaction state
        self._reaction_images: dict = {}  
        self._reaction_key    = None       
        self._reaction_timer  = 0          

        # Pre-load all reaction images
        for key, (path, pos, size, _dur) in REACTIONS.items():
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, size)
                self._reaction_images[key] = (img, pos)
            except FileNotFoundError:
                self._reaction_images[key] = None

    def load(self, path: str):
        img        = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, CUSTOMER_SIZE)
        self.cx          = float(CUSTOMER_START_X)
        self.walking     = True
        self.walking_out = False
        self.walked_out  = False
        self.float_time   = 0.0
        self.float_offset = 0.0
        self._reaction_key   = None
        self._reaction_timer = 0

    def walk_out(self):
        self.walking_out = True
        self.walking     = False

    def show_reaction(self, key: str):
        if key in REACTIONS:
            self._reaction_key   = key
            self._reaction_timer = REACTIONS[key][3]
            
    def update_and_draw(self, screen):
        if self.image is None:
            return

        # ── Movement ─────────────────────────────────────────
        if self.walking_out:
            self.cx += CUSTOMER_WALK_SPEED
            if self.cx > CUSTOMER_START_X + 20:
                self.walked_out  = True
                self.walking_out = False
            self.float_offset = 0.0

        elif self.walking:
            self.cx -= CUSTOMER_WALK_SPEED
            if self.cx <= CUSTOMER_TARGET_X:
                self.cx      = float(CUSTOMER_TARGET_X)
                self.walking = False
                # Auto-show hello reaction on arrival
                self.show_reaction("hello")

        else:
            self.float_time   += 0.03
            self.float_offset  = math.sin(self.float_time) * 6

        # ── Draw character ───────────────────────────────────
        if not self.walked_out:
            screen.blit(self.image,
                        (int(self.cx), CUSTOMER_Y + int(self.float_offset)))

        # ── Draw reaction bubble ─────────────────────────────
        if self._reaction_key and self._reaction_timer > 0 and not self.walked_out:
            entry = self._reaction_images.get(self._reaction_key)
            if entry:
                img, (rx, ry) = entry
                # Slight bounce using remaining timer
                bounce = math.sin(self._reaction_timer * 0.2) * 3
                screen.blit(img, (rx, int(ry + bounce)))

            self._reaction_timer -= 1
            if self._reaction_timer <= 0:
                self._reaction_key = None