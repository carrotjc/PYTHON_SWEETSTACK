# ui/screens.py
import pygame
from ui.helpers import draw_order_line, draw_ui_button
from settings   import ORDER_POS, WIDTH, HEIGHT, ORDER_HIDE_AFTER


def draw_hud(screen, order_font, current_order, order_visible,
             round_number, total_rounds, score, time_left):
    """
    Draw all in-game HUD elements:
      • Order card (BASE / FLAVOR / TOPPINGS) or 'Memorize' hint
      • ROUND X/Y and SCORE labels
      • Timer (turns red at ≤5 s)
    """
    # Order card
    if current_order:
        if order_visible:
            draw_order_line(screen, order_font,
                            "BASE:",     current_order["base"],
                            ORDER_POS[0], ORDER_POS[1])
            draw_order_line(screen, order_font,
                            "FLAVOR:",   current_order["flavor"],
                            ORDER_POS[0], ORDER_POS[1] + 50)
            draw_order_line(screen, order_font,
                            "TOPPINGS:", current_order["topping"],
                            ORDER_POS[0], ORDER_POS[1] + 100)
        else:
            hint = order_font.render("Memorize the order!", True, (180, 60, 100))
            screen.blit(hint, (ORDER_POS[0], ORDER_POS[1] + 25))

    # Round & Score stacked at (90, 126)
    screen.blit(
        order_font.render(f"ROUND: {round_number}/{total_rounds}", True, (0, 0, 0)),
        (90, 126),
    )
    screen.blit(
        order_font.render(f"SCORE: {score}", True, (0, 0, 0)),
        (90, 126 + order_font.get_height() + 4),
    )

    # Timer at (1221, 125)
    timer_color = (200, 0, 0) if time_left <= 5 else (0, 0, 0)
    screen.blit(
        order_font.render(f"TIME: {max(0, int(time_left))}s", True, timer_color),
        (1221, 125),
    )


def draw_game_over(screen, order_font, message_font, play_img, play_rect,
                   score, mouse_pos):
    """Draw the semi-transparent game over panel with final score."""
    pw, ph = 660, 360
    px     = WIDTH  // 2 - pw // 2
    py     = HEIGHT // 2 - ph // 2

    panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
    pygame.draw.rect(panel, (30, 10, 40, 220), panel.get_rect(), border_radius=24)
    screen.blit(panel, (px, py))
    pygame.draw.rect(screen, (230, 100, 160), (px, py, pw, ph), width=4, border_radius=24)

    for surf, cy in [
        (message_font.render("GAME OVER",                    True, (255, 220, 240)), py + 90),
        (order_font.render(f"Final Score: {score}",          True, (255, 220, 100)), py + 160),
        (order_font.render("Thanks for playing Sweet Stack!", True, (255, 200, 220)), py + 220),
    ]:
        screen.blit(surf, surf.get_rect(center=(WIDTH // 2, cy)))

    draw_ui_button(screen, play_img, play_rect, mouse_pos)