import pygame
import math


# ── Each decoration: path, base pos, size, animation type
_DECO_DATA = [
    {
        "path":   "assets/decorations/sun.png",
        "pos":    (765, 355),
        "size":   (81, 80),
        "anim":   "rotate",
        "speed":  0.08,            # was 0.4, now very slow spin
    },
    {
        "path":   "assets/decorations/sleepingcat.png",
        "pos":    (60, 592),
        "size":   (184, 124),
        "anim":   "breathe",      # gentle scale up/down like sleeping breathing
        "speed":  0.03,
    },
    {
        "path":   "assets/decorations/butterfly.png",
        "pos":    (513, 132),
        "size":   (117, 118),
        "anim":   "flutter",      # figure-8 drift + vertical bob
        "speed":  0.04,
    },
    {
        "path":   "assets/decorations/cat1.png",
        "pos":    (639, 597),
        "size":   (66, 37),
        "anim":   "slide",         # minimal left-right horizontal drift
        "speed":  0.02,
    },
    {
        "path":   "assets/decorations/dolphin.png",
        "pos":    (794, 541),
        "size":   (39, 41),
        "anim":   "fade",          # disappears then reappears smoothly
        "speed":  0.04,
    },
]


class DecorationManager:
    """
    Loads and animates all decorative elements.

    Animations per element:
        sun          → slow clockwise rotation
        sleepingcat  → breathing scale pulse (gentle inhale/exhale)
        butterfly    → figure-8 drift with vertical flutter
        cat1         → tail-wag rotation (tilts left and right)
        dolphin      → smooth vertical bob
    """

    def __init__(self):
        self._decos = []

        for d in _DECO_DATA:
            try:
                img = pygame.image.load(d["path"]).convert_alpha()
                img = pygame.transform.scale(img, d["size"])
            except FileNotFoundError:
                img = None

            self._decos.append({
                "image": img,
                "pos":   d["pos"],
                "size":  d["size"],
                "anim":  d["anim"],
                "speed": d["speed"],
                "t":     0.0,          # individual timer per deco
                "angle": 0.0,          # for rotation-based anims
            })

    def update_and_draw(self, screen):
        for d in self._decos:
            if d["image"] is None:
                continue

            d["t"] += d["speed"]
            t       = d["t"]
            bx, by  = d["pos"]
            img     = d["image"]
            anim    = d["anim"]

            # ── Rotate (sun) ──────────────────────────────────
            if anim == "rotate":
                d["angle"] += 0.03   # ultra minimal, barely noticeable spin
                rotated = pygame.transform.rotate(img, -d["angle"])
                rect    = rotated.get_rect(center=(bx + d["size"][0] // 2,
                                                   by + d["size"][1] // 2))
                screen.blit(rotated, rect.topleft)

            # ── Breathe (sleeping cat) ────────────────────────
            elif anim == "breathe":
                scale  = 1.0 + math.sin(t) * 0.03
                w = int(d["size"][0] * scale)
                h = int(d["size"][1] * scale)
                scaled = pygame.transform.scale(img, (w, h))
                rect   = scaled.get_rect(bottomleft=(bx, by + d["size"][1]))
                screen.blit(scaled, rect.topleft)

            # ── Flutter (butterfly) ───────────────────────────
            elif anim == "flutter":
                off_x = math.sin(t)     * 12
                off_y = math.sin(t * 2) * 7
                flap  = 1.0 + math.sin(t * 6) * 0.08
                w     = int(d["size"][0] * flap)
                h     = d["size"][1]
                scaled = pygame.transform.scale(img, (w, h))
                rect   = scaled.get_rect(topleft=(int(bx + off_x), int(by + off_y)))
                screen.blit(scaled, rect.topleft)

            # ── Slide (cat1) — wide but slow horizontal drift ─
            elif anim == "slide":
                off_x = math.sin(t) * 18   # ±18px wide range, slow speed=0.02
                screen.blit(img, (int(bx + off_x), by))

            # ── Wag (unused) ──────────────────────────────────
            elif anim == "wag":
                angle   = math.sin(t * 3) * 12
                rotated = pygame.transform.rotate(img, angle)
                rect    = rotated.get_rect(midbottom=(bx + d["size"][0] // 2,
                                                      by + d["size"][1]))
                screen.blit(rotated, rect.topleft)

            # ── Fade (dolphin) — appear, pause, disappear ─────
            elif anim == "fade":
                # sin²: stays fully visible longer, disappears sharply
                raw   = math.sin(t)
                alpha = int((raw * raw if raw > 0 else 0) * 255)
                faded = img.copy()
                faded.set_alpha(alpha)
                screen.blit(faded, (bx, by))

            # ── Bob (unused) ───────────────────────────────────
            elif anim == "bob":
                off_y   = math.sin(t * 2) * 6
                tilt    = math.cos(t * 2) * 8
                rotated = pygame.transform.rotate(img, tilt)
                rect    = rotated.get_rect(center=(bx + d["size"][0] // 2,
                                                   by + d["size"][1] // 2 + int(off_y)))
                screen.blit(rotated, rect.topleft)