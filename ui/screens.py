# ui/screens.py
import pygame
from ui.helpers import draw_order_line, draw_ui_button
from settings   import ORDER_POS, WIDTH, HEIGHT


def draw_order_panel(screen, order_font, current_order, order_visible):
    """
    Draw order text only — no background panel.
    The background image already has the order card panel baked in.
    """
    if not current_order:
        return

    if order_visible:
        line_h = order_font.get_height() + 10
        draw_order_line(screen, order_font,
                        "BASE:",     current_order["base"],
                        ORDER_POS[0], ORDER_POS[1])
        draw_order_line(screen, order_font,
                        "FLAVOR:",   current_order["flavor"],
                        ORDER_POS[0], ORDER_POS[1] + line_h)
        draw_order_line(screen, order_font,
                        "TOPPINGS:", current_order["topping"],
                        ORDER_POS[0], ORDER_POS[1] + line_h * 2)
    else:
        hint = order_font.render("Memorize the order!", True, (180, 60, 100))
        screen.blit(hint, (ORDER_POS[0], ORDER_POS[1] + 25))


def draw_hearts(screen, lives: int, max_lives: int = 3):
    """Draw filled/empty hearts below the score at (90, 212)."""
    HEART_Y  = 212
    HEART_W  = 28
    SPACING  = 36
    START_X  = 90

    for i in range(max_lives):
        x     = START_X + i * SPACING
        color = (220, 50, 80) if i < lives else (160, 160, 160)
        r     = HEART_W // 4

        surf = pygame.Surface((HEART_W, HEART_W), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (r,         r), r)
        pygame.draw.circle(surf, color, (r * 3,     r), r)
        pygame.draw.polygon(surf, color, [
            (0,       r),
            (HEART_W, r),
            (HEART_W // 2, HEART_W - 2),
        ])
        screen.blit(surf, (x, HEART_Y))


def draw_hud(screen, order_font, current_order, order_visible,
             round_number, total_rounds, score, time_left,
             lives, max_lives):
    """
    Draw all in-game HUD text.
    No background panels drawn here — they are part of the background image.
    """
    draw_order_panel(screen, order_font, current_order, order_visible)

    # Round & Score — positions match the baked-in panels on the background
    screen.blit(
        order_font.render(f"ROUND: {round_number}/{total_rounds}", True, (0, 0, 0)),
        (90, 126),
    )
    screen.blit(
        order_font.render(f"SCORE: {score}", True, (0, 0, 0)),
        (90, 126 + order_font.get_height() + 4),
    )

    # Hearts
    draw_hearts(screen, lives, max_lives)

    # Timer
    timer_color = (200, 0, 0) if time_left <= 5 else (0, 0, 0)
    screen.blit(
        order_font.render(f"TIME: {max(0, int(time_left))}s", True, timer_color),
        (1221, 125),
    )


def _draw_panel(screen, title_text, lines, message_font, order_font,
                play_img, play_rect, mouse_pos, title_color, border_color):
    """Shared panel renderer for win / game over screens."""
    pw, ph = 660, 380
    px     = WIDTH  // 2 - pw // 2
    py     = HEIGHT // 2 - ph // 2

    panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
    pygame.draw.rect(panel, (30, 10, 40, 220), panel.get_rect(), border_radius=24)
    screen.blit(panel, (px, py))
    pygame.draw.rect(screen, border_color, (px, py, pw, ph), width=4, border_radius=24)

    title_surf = message_font.render(title_text, True, title_color)
    screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, py + 80)))

    for i, (text, color) in enumerate(lines):
        surf = order_font.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(WIDTH // 2, py + 160 + i * 55)))

    draw_ui_button(screen, play_img, play_rect, mouse_pos)


def draw_game_over(screen, order_font, message_font, play_img, play_rect,
                   score, mouse_pos):
    """Dark panel — player ran out of lives."""
    _draw_panel(
        screen,
        title_text   = "GAME OVER",
        lines        = [
            (f"Final Score: {score}",          (255, 220, 100)),
            ("Thanks for playing Sweet Stack!", (255, 200, 220)),
        ],
        message_font = message_font,
        order_font   = order_font,
        play_img     = play_img,
        play_rect    = play_rect,
        mouse_pos    = mouse_pos,
        title_color  = (255, 220, 240),
        border_color = (230, 100, 160),
    )


def draw_win_screen(screen, order_font, message_font, play_img, play_rect,
                    score, mouse_pos):
    """Green celebratory panel — all 3 rounds completed."""
    _draw_panel(
        screen,
        title_text   = "YOU WIN!",
        lines        = [
            (f"Final Score: {score}",    (255, 240, 80)),
            ("Amazing job, Sweet Chef!", (200, 255, 180)),
        ],
        message_font = message_font,
        order_font   = order_font,
        play_img     = play_img,
        play_rect    = play_rect,
        mouse_pos    = mouse_pos,
        title_color  = (200, 255, 160),
        border_color = (100, 220, 130),
    )