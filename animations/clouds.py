# animations/clouds.py
import pygame
import math
import random
from settings import CLOUD_DATA, CLOUD_EXIT_SPEED, WIDTH


class CloudManager:
    """
    Loads and animates all start-screen clouds.

    Idle  : gentle independent sine drift on x and y per cloud.
    Exit  : clouds 1-3 slide left, clouds 4-6 slide right until off-screen.
            update_and_draw() returns True when all are gone.
    """

    def __init__(self, screen_width=WIDTH):
        self.screen_width = screen_width
        self.exiting      = False
        self.clouds       = []

        for cd in CLOUD_DATA:
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
        self.exiting = True
        for c in self.clouds:
            c["cx"]   = float(c["ox"])
            c["gone"] = False

    def reset(self):
        self.exiting = False
        for c in self.clouds:
            c["cx"]   = float(c["ox"])
            c["gone"] = False

    def update_and_draw(self, screen) -> bool:
        """Returns True once every cloud has exited."""
        gone_count = 0

        for c in self.clouds:
            if self.exiting and not c["gone"]:
                if c["exit"] == "left":
                    c["cx"] -= CLOUD_EXIT_SPEED
                    if c["cx"] + c["w"] < 0:
                        c["gone"] = True
                else:
                    c["cx"] += CLOUD_EXIT_SPEED
                    if c["cx"] > self.screen_width:
                        c["gone"] = True

            if c["gone"]:
                gone_count += 1
                continue

            if not self.exiting:
                c["float_t"] += 0.01
                draw_x = c["cx"] + math.sin(c["float_t"])            * 4
                draw_y = c["oy"]  + math.sin(c["float_t"] * 0.7 + 1) * 5
            else:
                draw_x, draw_y = c["cx"], c["oy"]

            screen.blit(c["image"], (int(draw_x), int(draw_y)))

        if self.exiting and gone_count == len(self.clouds):
            self.reset()
            return True

        return False