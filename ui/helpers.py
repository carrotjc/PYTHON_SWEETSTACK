# ui/helpers.py
import pygame


def draw_ui_button(screen, img, rect, mouse_pos, hover_scale=1.08):
    """Render a button that scales up slightly on hover."""
    if rect.collidepoint(mouse_pos):
        w      = int(rect.width  * hover_scale)
        h      = int(rect.height * hover_scale)
        scaled = pygame.transform.scale(img, (w, h))
        srect  = scaled.get_rect(center=rect.center)
        screen.blit(scaled, srect.topleft)
    else:
        screen.blit(img, rect.topleft)


def draw_message(screen, font, msg: str, timer: int,
                 screen_w: int, screen_h: int):
    """
    Draw a themed pill-shaped toast centred on screen.
    Returns (msg, timer) — store the returned values back in the caller.
    Clears itself when timer reaches 0.
    """
    if msg and timer > 0:
        surf         = font.render(msg, True, (255, 255, 255))
        pad_x, pad_y = 30, 16
        w            = surf.get_width()  + pad_x * 2
        h            = surf.get_height() + pad_y * 2
        bx           = screen_w // 2 - w // 2
        by           = screen_h // 2 - h // 2

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (30, 10, 40, 210), overlay.get_rect(), border_radius=18)
        screen.blit(overlay, (bx, by))
        pygame.draw.rect(screen, (230, 100, 160), (bx, by, w, h), width=3, border_radius=18)
        screen.blit(surf, (bx + pad_x, by + pad_y))

        timer -= 1
        if timer <= 0:
            return "", 0
    return msg, timer


def draw_order_line(screen, font, label: str, value: str, x: int, y: int,
                    label_color=(0, 0, 0), value_color=(200, 0, 0)):
    """Render a coloured label + value pair, e.g. 'BASE:  Cone'."""
    label_surf = font.render(label, True, label_color)
    value_surf = font.render(value, True, value_color)
    screen.blit(label_surf, (x, y))
    screen.blit(value_surf, (x + label_surf.get_width() + 10, y))