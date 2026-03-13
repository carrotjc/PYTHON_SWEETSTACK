# animations/drops.py
import pygame
from settings import NOZZLE_X, NOZZLE_Y, DROP_PATHS


class DropEffect:
    """
    A single flavor drip that falls from the machine nozzle.

    Phases:
        falling → squash → fade → done (auto-removed by DropManager)

    Visual tricks:
        • Stretches vertically while falling (speed-proportional)
        • Squashes wide + flat on landing
        • Alpha-fades out over FADE_FRAMES frames
    """

    GRAVITY       = 0.7
    INITIAL_SPEED = 3.0
    SQUASH_FRAMES = 8
    FADE_FRAMES   = 12

    def __init__(self, image, start_x, start_y, target_x, target_y):
        self._base_image = image
        self.x           = float(start_x)
        self.y           = float(start_y)
        self.target_x    = float(target_x)
        self.target_y    = float(target_y)
        self.speed       = self.INITIAL_SPEED
        self.phase       = "falling"
        self.squash_t    = 0
        self.alpha       = 255
        self.done        = False
        self.base_w, self.base_h = image.get_size()

    def update(self):
        if self.done:
            return

        if self.phase == "falling":
            self.speed += self.GRAVITY
            self.y     += self.speed
            self.x     += (self.target_x - self.x) * 0.12
            if self.y >= self.target_y:
                self.y    = self.target_y
                self.phase = "squash"

        elif self.phase == "squash":
            self.squash_t += 1
            if self.squash_t >= self.SQUASH_FRAMES:
                self.phase = "fade"

        elif self.phase == "fade":
            self.alpha -= int(255 / self.FADE_FRAMES)
            if self.alpha <= 0:
                self.alpha = 0
                self.done  = True

    def draw(self, screen):
        if self.done:
            return

        if self.phase == "falling":
            stretch = min(self.speed / 12, 0.4)
            w = int(self.base_w * (1.0 - stretch * 0.4))
            h = int(self.base_h * (1.0 + stretch * 0.6))
        elif self.phase == "squash":
            prog = self.squash_t / self.SQUASH_FRAMES
            w    = int(self.base_w * (1.0 + prog * 0.5))
            h    = int(self.base_h * (1.0 - prog * 0.3))
        else:
            w, h = self.base_w, self.base_h

        scaled = pygame.transform.scale(self._base_image, (max(1, w), max(1, h)))
        scaled.set_alpha(self.alpha)
        rect = scaled.get_rect(midbottom=(int(self.x), int(self.y)))
        screen.blit(scaled, rect.topleft)


class DropManager:
    """
    Spawns, updates, and draws all active DropEffect instances.
    Call spawn() on flavor selection, update_and_draw() every frame.
    """

    def __init__(self):
        self._drops  = []
        self._images = {}   # cached surfaces keyed by flavor name

    def _get_image(self, flavor_name: str):
        key = flavor_name.lower()
        if key not in self._images:
            path = DROP_PATHS.get(key, DROP_PATHS["avocado"])
            img  = pygame.image.load(path).convert_alpha()
            img  = pygame.transform.scale(img, (48, 64))
            self._images[key] = img
        return self._images[key]

    def spawn(self, flavor_name: str, target_pos: tuple):
        tx, ty = target_pos
        drop   = DropEffect(
            image    = self._get_image(flavor_name),
            start_x  = NOZZLE_X,
            start_y  = NOZZLE_Y,
            target_x = tx + 40,
            target_y = ty + 30,
        )
        self._drops.append(drop)

    def update_and_draw(self, screen):
        for drop in self._drops:
            drop.update()
            drop.draw(screen)
        self._drops = [d for d in self._drops if not d.done]

    def clear(self):
        self._drops.clear()