"""
animations.py
-------------
All animation classes and shared UI helpers for Sweet Stack.

Classes
    CloudManager     — idle float + exit-left/right on play press
    CustomerAnimator — walk-in from right + idle float bob
    DropEffect       — single drip that falls from the machine nozzle and fades
    DropManager      — spawns / updates / draws all active DropEffects
    ScorePop         — floating "+N" text that rises and fades on correct order

Helpers
    draw_ui_button   — hover-scale effect for any button image
    draw_message     — themed toast notification (pill with border)
    draw_order_line  — coloured label + value pair for the order card
"""

import pygame
import math
import random


# ─────────────────────────────────────────────────────────────
#  CloudManager
# ─────────────────────────────────────────────────────────────
class CloudManager:
    """
    Loads and animates all clouds on the start screen.

    Idle state  : gentle sine-wave drift (x and y independently)
    Exit state  : clouds 1-3 slide left, clouds 4-6 slide right
                  until fully off screen, then `all_gone` → True
    """

    EXIT_SPEED = 8   # pixels per frame during exit

    _CLOUD_DATA = [
        {"path": "assets/clouds/cloud1.png", "ox": 378,  "oy": 67,  "w": 183,    "h": 113, "exit": "left"},
        {"path": "assets/clouds/cloud2.png", "ox": -64,  "oy": 195, "w": 304.35, "h": 170, "exit": "left"},
        {"path": "assets/clouds/cloud3.png", "ox": -34,  "oy": 622, "w": 380,    "h": 133, "exit": "left"},
        {"path": "assets/clouds/cloud4.png", "ox": 1014, "oy": 0,   "w": 499,    "h": 255, "exit": "right"},
        {"path": "assets/clouds/cloud5.png", "ox": 1200, "oy": 429, "w": 313,    "h": 193, "exit": "right"},
        {"path": "assets/clouds/cloud6.png", "ox": 317,  "oy": 844, "w": 806.04, "h": 120, "exit": "right"},
    ]

    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.exiting      = False
        self.all_gone     = False
        self.clouds       = []

        for cd in self._CLOUD_DATA:
            img = pygame.image.load(cd["path"]).convert_alpha()
            img = pygame.transform.scale(img, (int(cd["w"]), int(cd["h"])))
            self.clouds.append({
                "image":   img,
                "ox":      cd["ox"],
                "oy":      cd["oy"],
                "w":       int(cd["w"]),
                "h":       int(cd["h"]),
                "exit":    cd["exit"],
                "cx":      float(cd["ox"]),
                "float_t": random.uniform(0, 2 * math.pi),
                "gone":    False,
            })

    def start_exit(self):
        """Call when the play button is pressed."""
        self.exiting  = True
        self.all_gone = False
        for c in self.clouds:
            c["cx"]   = float(c["ox"])
            c["gone"] = False

    def reset(self):
        """Restore clouds to their resting positions (for returning to start)."""
        self.exiting  = False
        self.all_gone = False
        for c in self.clouds:
            c["cx"]   = float(c["ox"])
            c["gone"] = False

    def update_and_draw(self, screen):
        """
        Call once per frame while game_state == 'start'.
        Returns True when all clouds have exited (time to switch state).
        """
        gone_count = 0

        for c in self.clouds:
            if self.exiting and not c["gone"]:
                if c["exit"] == "left":
                    c["cx"] -= self.EXIT_SPEED
                    if c["cx"] + c["w"] < 0:
                        c["gone"] = True
                else:
                    c["cx"] += self.EXIT_SPEED
                    if c["cx"] > self.screen_width:
                        c["gone"] = True

            if c["gone"]:
                gone_count += 1
                continue

            # Choose draw position
            if not self.exiting:
                # Gentle idle float
                c["float_t"] += 0.01
                draw_x = c["cx"] + math.sin(c["float_t"])            * 4
                draw_y = c["oy"]  + math.sin(c["float_t"] * 0.7 + 1) * 5
            else:
                draw_x = c["cx"]
                draw_y = c["oy"]

            screen.blit(c["image"], (int(draw_x), int(draw_y)))

        if self.exiting and gone_count == len(self.clouds):
            self.reset()   # resets exiting + positions for next visit
            return True    # signal to main: transition now

        return False


# ─────────────────────────────────────────────────────────────
#  CustomerAnimator
# ─────────────────────────────────────────────────────────────
class CustomerAnimator:
    """
    Manages a single customer sprite:
      - walk-in  : slides from START_X → TARGET_X at WALK_SPEED px/frame
      - idle bob : gentle vertical sine float once in position
    """

    TARGET_X   = 1048
    START_X    = 1240
    Y          = 368
    SIZE       = (240, 269)
    WALK_SPEED = 6

    def __init__(self):
        self.image        = None
        self.cx           = float(self.START_X)
        self.walking      = False
        self.float_time   = 0.0
        self.float_offset = 0.0

    def load(self, path):
        """Load a new customer image and kick off the walk-in."""
        img        = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, self.SIZE)
        self.cx      = float(self.START_X)
        self.walking = True
        self.float_time   = 0.0
        self.float_offset = 0.0

    def update_and_draw(self, screen):
        if self.image is None:
            return

        # Walk-in
        if self.walking:
            self.cx -= self.WALK_SPEED
            if self.cx <= self.TARGET_X:
                self.cx      = float(self.TARGET_X)
                self.walking = False

        # Idle bob (only after arrival)
        if not self.walking:
            self.float_time   += 0.03
            self.float_offset  = math.sin(self.float_time) * 6
        else:
            self.float_offset = 0.0

        screen.blit(self.image, (int(self.cx), self.Y + int(self.float_offset)))


# ─────────────────────────────────────────────────────────────
#  DropEffect  (single drip instance)
# ─────────────────────────────────────────────────────────────
class DropEffect:
    """
    A single drip blob that:
      1. Spawns at the machine nozzle (start_x, start_y)
      2. Falls toward (target_x, target_y) with accelerating gravity
      3. Slightly stretches vertically while falling
      4. On arrival: squashes wide + flat for a few frames
      5. Fades out (alpha → 0) then marks itself done

    Phases: "falling" → "squash" → "fade" → done
    """

    GRAVITY       = 0.7    # px added to speed each frame
    INITIAL_SPEED = 3.0    # starting downward speed
    SQUASH_FRAMES = 8      # frames to hold the squash shape
    FADE_FRAMES   = 12     # frames for alpha fade-out

    def __init__(self, image, start_x, start_y, target_x, target_y):
        self._base_image = image          # original loaded surface
        self.x           = float(start_x)
        self.y           = float(start_y)
        self.target_x    = float(target_x)
        self.target_y    = float(target_y)
        self.speed       = self.INITIAL_SPEED
        self.phase       = "falling"
        self.squash_t    = 0
        self.alpha        = 255
        self.done        = False

        # Base draw size (match the image's natural size)
        w, h             = image.get_size()
        self.base_w      = w
        self.base_h      = h

    def update(self):
        if self.done:
            return

        if self.phase == "falling":
            self.speed += self.GRAVITY
            self.y     += self.speed

            # Horizontal drift toward target_x
            dx          = self.target_x - self.x
            self.x     += dx * 0.12

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
            # Stretch: narrow + taller as speed increases
            stretch = min(self.speed / 12, 0.4)
            w = int(self.base_w * (1.0 - stretch * 0.4))
            h = int(self.base_h * (1.0 + stretch * 0.6))

        elif self.phase == "squash":
            # Squash: wider + shorter
            prog = self.squash_t / self.SQUASH_FRAMES
            w    = int(self.base_w * (1.0 + prog * 0.5))
            h    = int(self.base_h * (1.0 - prog * 0.3))

        else:  # fade
            w = self.base_w
            h = self.base_h

        scaled = pygame.transform.scale(self._base_image, (max(1, w), max(1, h)))
        scaled.set_alpha(self.alpha)
        rect = scaled.get_rect(midbottom=(int(self.x), int(self.y)))
        screen.blit(scaled, rect.topleft)


# ─────────────────────────────────────────────────────────────
#  DropManager
# ─────────────────────────────────────────────────────────────
class DropManager:
    """
    Holds and drives all active DropEffect instances.

    Drop images are mapped by flavor name:
        Caramel / Chocolate / Strawberry / Avocado
    Falls back to avocado if a name isn't found.

    Nozzle position is derived from the machine center.
    """

    # Map flavor name (lowercase) → drop asset path
    _DROP_PATHS = {
        "caramel":    "assets/drops/drops_caramel.png",
        "chocolate":  "assets/drops/drops_chocolate.png",
        "strawberry": "assets/drops/drops_strawberry.png",
        "avocado":    "assets/drops/drops_avocado.png",
    }

    # Machine nozzle position — shift NOZZLE_X to move drops left/right
    NOZZLE_X = 975   # shifted 25px right from original 950
    NOZZLE_Y = 390

    def __init__(self):
        self._drops  = []
        self._images = {}   # cached loaded images keyed by flavor name

    def _get_image(self, flavor_name):
        key  = flavor_name.lower()
        if key not in self._images:
            path = self._DROP_PATHS.get(key, self._DROP_PATHS["avocado"])
            img  = pygame.image.load(path).convert_alpha()
            img  = pygame.transform.scale(img, (48, 64))
            self._images[key] = img
        return self._images[key]

    def spawn(self, flavor_name, target_pos):
        """
        Spawn a drip for the given flavor name.
        target_pos = (x, y) where the scoop will land (product_pos).
        """
        img    = self._get_image(flavor_name)
        tx, ty = target_pos
        drop   = DropEffect(
            image    = img,
            start_x  = self.NOZZLE_X,
            start_y  = self.NOZZLE_Y,
            target_x = tx + 40,
            target_y = ty + 30,
        )
        self._drops.append(drop)

    def update_and_draw(self, screen):
        """Call once per frame inside the game draw block."""
        for drop in self._drops:
            drop.update()
            drop.draw(screen)
        # Remove finished drops
        self._drops = [d for d in self._drops if not d.done]

    def clear(self):
        self._drops.clear()


# ─────────────────────────────────────────────────────────────
#  ScorePop
# ─────────────────────────────────────────────────────────────
class ScorePop:
    """
    A floating "+N" label that rises from a point and fades out.
    Create one each time a correct order is submitted.
    """

    RISE_SPEED  = 1.8   # px per frame upward
    TOTAL_FRAMES = 55

    def __init__(self, font, text, x, y, color=(255, 220, 60)):
        self.surf   = font.render(text, True, color)
        self.x      = float(x)
        self.y      = float(y)
        self.frame  = 0
        self.done   = False

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


# ─────────────────────────────────────────────────────────────
#  UI helpers
# ─────────────────────────────────────────────────────────────

def draw_ui_button(screen, img, rect, mouse_pos, hover_scale=1.08):
    """Render a button that enlarges slightly when hovered."""
    if rect.collidepoint(mouse_pos):
        w       = int(rect.width  * hover_scale)
        h       = int(rect.height * hover_scale)
        scaled  = pygame.transform.scale(img, (w, h))
        srect   = scaled.get_rect(center=rect.center)
        screen.blit(scaled, srect.topleft)
    else:
        screen.blit(img, rect.topleft)


def draw_message(screen, font, msg, timer, screen_w, screen_h):
    """
    Draw a themed pill-shaped toast in the centre of the screen.
    Returns the decremented timer value (caller should store it).
    """
    if msg and timer > 0:
        surf    = font.render(msg, True, (255, 255, 255))
        pad_x, pad_y = 30, 16
        w       = surf.get_width()  + pad_x * 2
        h       = surf.get_height() + pad_y * 2
        bx      = screen_w // 2 - w // 2
        by      = screen_h // 2 - h // 2

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (30, 10, 40, 210), overlay.get_rect(), border_radius=18)
        screen.blit(overlay, (bx, by))
        pygame.draw.rect(screen, (230, 100, 160), (bx, by, w, h), width=3, border_radius=18)
        screen.blit(surf, (bx + pad_x, by + pad_y))

        timer -= 1
        if timer <= 0:
            return "", 0
    return msg, timer


def draw_order_line(screen, font, label, value, x, y,
                    label_color=(0, 0, 0), value_color=(200, 0, 0)):
    """Render a coloured label + value pair (e.g. 'BASE:  Cone')."""
    label_surf = font.render(label, True, label_color)
    value_surf = font.render(value, True, value_color)
    screen.blit(label_surf, (x, y))
    screen.blit(value_surf, (x + label_surf.get_width() + 10, y))