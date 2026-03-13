# animations/customer.py
import pygame
import math
from settings import (
    CUSTOMER_TARGET_X, CUSTOMER_START_X,
    CUSTOMER_Y, CUSTOMER_SIZE, CUSTOMER_WALK_SPEED,
)


class CustomerAnimator:
    """
    Manages a single customer sprite.

    Walk-in : slides from START_X → TARGET_X at WALK_SPEED px/frame.
    Idle bob: gentle vertical sine float once the character has arrived.
    """

    def __init__(self):
        self.image        = None
        self.cx           = float(CUSTOMER_START_X)
        self.walking      = False
        self.float_time   = 0.0
        self.float_offset = 0.0

    def load(self, path: str):
        """Load a new character image and trigger the walk-in animation."""
        img        = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, CUSTOMER_SIZE)
        self.cx           = float(CUSTOMER_START_X)
        self.walking      = True
        self.float_time   = 0.0
        self.float_offset = 0.0

    def update_and_draw(self, screen):
        if self.image is None:
            return

        if self.walking:
            self.cx -= CUSTOMER_WALK_SPEED
            if self.cx <= CUSTOMER_TARGET_X:
                self.cx      = float(CUSTOMER_TARGET_X)
                self.walking = False

        if not self.walking:
            self.float_time   += 0.03
            self.float_offset  = math.sin(self.float_time) * 6
        else:
            self.float_offset = 0.0

        screen.blit(self.image, (int(self.cx), CUSTOMER_Y + int(self.float_offset)))