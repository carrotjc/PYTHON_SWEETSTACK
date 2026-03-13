# animations/effects.py
import pygame


class ScorePop:
    RISE_SPEED   = 1.8
    TOTAL_FRAMES = 55

    def __init__(self, font, text: str, x: int, y: int,
                 color=(255, 220, 60)):
        self.surf  = font.render(text, True, color)
        self.x     = float(x)
        self.y     = float(y)
        self.frame = 0
        self.done  = False

    def update_and_draw(self, screen):
        if self.done:
            return
        self.y     -= self.RISE_SPEED
        self.frame += 1
        alpha = max(0, int(255 * (1 - self.frame / self.TOTAL_FRAMES)))
        self.surf.set_alpha(alpha)
        screen.blit(self.surf, (int(self.x), int(self.y)))
        if self.frame >= self.TOTAL_FRAMES:
            self.done = True