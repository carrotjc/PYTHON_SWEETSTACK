import pygame
import sys
import math
import random

from logic      import IceCreamStack, IceCreamOrder
from animations import (
    CloudManager, CustomerAnimator, DropManager, ScorePop,
    draw_ui_button, draw_message, draw_order_line,
)

pygame.init()

#  Screen

WIDTH, HEIGHT = 1440, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sweet Stack")
clock  = pygame.time.Clock()

#  Fonts
order_font   = pygame.font.Font("assets/fonts/PixelOperator.ttf", 32)
message_font = pygame.font.Font("assets/fonts/PixelOperator.ttf", 40)


#  Background
background = pygame.image.load("assets/backgroundfinal.png").convert()

#  Start-screen assets
title_img  = pygame.image.load("assets/sweetstack.png").convert_alpha()
title_img  = pygame.transform.scale(title_img, (922, 375))
title_rect = title_img.get_rect(topleft=(259, 250))

play_img  = pygame.image.load("assets/playbutton.png").convert_alpha()
play_img  = pygame.transform.scale(play_img, (483, 107))
play_rect = play_img.get_rect(topleft=(478, 667))

# ─────────────────────────────────────────────────────────────
#  Machine
# ─────────────────────────────────────────────────────────────
machine_img = pygame.image.load("assets/machine.png").convert_alpha()
machine_img = pygame.transform.scale(machine_img, (230, 343))
MACHINE_X, MACHINE_Y = 859, 63

# ─────────────────────────────────────────────────────────────
#  Reset & Submit buttons
# ─────────────────────────────────────────────────────────────
reset_img  = pygame.image.load("assets/resetbutton.png").convert_alpha()
reset_img  = pygame.transform.scale(reset_img, (246, 84))
reset_rect = reset_img.get_rect(topleft=(60, 919))

submit_img  = pygame.image.load("assets/submitbutton.png").convert_alpha()
submit_img  = pygame.transform.scale(submit_img, (233, 81))
submit_rect = submit_img.get_rect(topleft=(1149, 923))

# ─────────────────────────────────────────────────────────────
#  Ingredient buttons
# ─────────────────────────────────────────────────────────────
BUTTONS_DATA = [
    {"type": "base",    "name": "Cone",
     "button_path": "assets/buttons/base_cone.png",
     "product_path": "assets/product/cone.png",
     "button_pos": (422, 811), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},
    {"type": "base",    "name": "Cup",
     "button_path": "assets/buttons/base_cup.png",
     "product_path": "assets/product/cup.png",
     "button_pos": (422, 877), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},
    {"type": "base",    "name": "Bowl",
     "button_path": "assets/buttons/base_bowl.png",
     "product_path": "assets/product/bowl.png",
     "button_pos": (422, 942), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},
    {"type": "flavor",  "name": "Caramel",
     "button_path": "assets/buttons/flavor_caramel.png",
     "product_path": "assets/product/caramel.png",
     "button_pos": (556, 833), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "flavor",  "name": "Chocolate",
     "button_path": "assets/buttons/flavor_chocolate.png",
     "product_path": "assets/product/chocolate.png",
     "button_pos": (551, 914), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "flavor",  "name": "Strawberry",
     "button_path": "assets/buttons/flavor_strawberry.png",
     "product_path": "assets/product/strawberry.png",
     "button_pos": (633, 833), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "flavor",  "name": "Avocado",
     "button_path": "assets/buttons/flavor_avocado.png",
     "product_path": "assets/product/avocado.png",
     "button_pos": (633, 914), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "topping", "name": "Cherry",
     "button_path": "assets/buttons/toppings_cherry.png",
     "product_path": "assets/product/cherry.png",
     "button_pos": (858, 832), "button_size": (82, 59),
     "product_pos": (906, 440), "product_size": (136, 98)},
    {"type": "topping", "name": "Syrup",
     "button_path": "assets/buttons/toppings_syrup.png",
     "product_path": "assets/product/syrup.png",
     "button_pos": (759, 832), "button_size": (82, 59),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "topping", "name": "Matcha",
     "button_path": "assets/buttons/toppings_matcha.png",
     "product_path": "assets/product/matcha.png",
     "button_pos": (758, 907), "button_size": (82, 59),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "topping", "name": "Nuts",
     "button_path": "assets/buttons/toppings_nuts.png",
     "product_path": "assets/product/nuts.png",
     "button_pos": (857, 907), "button_size": (83, 60),
     "product_pos": (906, 475), "product_size": (136, 98)},
]

buttons = []
for data in BUTTONS_DATA:
    img  = pygame.image.load(data["button_path"]).convert_alpha()
    img  = pygame.transform.scale(img, data["button_size"])
    data["button_image"] = img
    data["button_rect"]  = img.get_rect(topleft=data["button_pos"])
    data["time_offset"]  = random.uniform(0, 2 * math.pi)
    buttons.append(data)

# ─────────────────────────────────────────────────────────────
#  Animation objects
# ─────────────────────────────────────────────────────────────
clouds   = CloudManager(screen_width=WIDTH)
customer = CustomerAnimator()
drops    = DropManager()
score_pops: list[ScorePop] = []

# ─────────────────────────────────────────────────────────────
#  Order system
# ─────────────────────────────────────────────────────────────
order_system  = IceCreamOrder()
current_order = None
order_pos     = (141, 347)

# ─────────────────────────────────────────────────────────────
#  Game state
# ─────────────────────────────────────────────────────────────
game_state   = "start"
round_number = 1
score        = 0
time_left    = 20.0
time_passed  = 0.0     # drives machine wobble + button wiggle

# Per-round config
# Round 1 (20s) — order always visible
# Round 2 (15s) — order hides after 8 s
# Round 3  (8s) — order hides after 3 s
ROUND_TIMES      = [20, 15, 8]
ORDER_HIDE_AFTER = [None, 8, 3]
order_visible    = True
order_hide_timer = 0.0

# Selected ingredient names for the current round
selected = {"base": None, "flavor": None, "topping": None}

# Toast message
message_text  = ""
message_timer = 0

icecream_stack = IceCreamStack()
running        = True


# ─────────────────────────────────────────────────────────────
#  Helper functions
# ─────────────────────────────────────────────────────────────

def start_round(rnum: int):
    global current_order, time_left, order_visible, order_hide_timer, selected

    icecream_stack.reset_stack()
    drops.clear()
    selected = {"base": None, "flavor": None, "topping": None}

    current_order = order_system.generate_order()
    customer.load(current_order["customer"])

    time_left    = float(ROUND_TIMES[rnum - 1])
    order_visible = True
    hide_after    = ORDER_HIDE_AFTER[rnum - 1]
    order_hide_timer = float(hide_after) if hide_after is not None else 0.0


def advance_round():
    global round_number, game_state
    round_number += 1
    if round_number > 3:
        game_state = "game_over"
    else:
        start_round(round_number)


# ─────────────────────────────────────────────────────────────
#  GAME LOOP
# ─────────────────────────────────────────────────────────────
while running:
    dt        = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()

    # ── Events ──────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # START SCREEN
            if game_state == "start":
                if play_rect.collidepoint(mouse_pos) and not clouds.exiting:
                    clouds.start_exit()

            # GAME SCREEN
            elif game_state == "game":

                if reset_rect.collidepoint(mouse_pos):
                    icecream_stack.reset_stack()
                    drops.clear()
                    selected = {"base": None, "flavor": None, "topping": None}

                elif submit_rect.collidepoint(mouse_pos):
                    b, f, t = selected["base"], selected["flavor"], selected["topping"]
                    if b is None or f is None or t is None:
                        message_text, message_timer = "Sorry, wrong order!", 120
                    elif (b.lower() == current_order["base"].lower() and
                          f.lower() == current_order["flavor"].lower() and
                          t.lower() == current_order["topping"].lower()):
                        # Correct order — award score
                        earned = 100 + int(time_left) * 5
                        score += earned
                        score_pops.append(ScorePop(
                            order_font, f"+{earned}",
                            x=90, y=210,
                        ))
                        advance_round()
                    else:
                        message_text, message_timer = "Sorry, wrong order!", 120

                else:
                    for button in buttons:
                        if button["button_rect"].collidepoint(mouse_pos):
                            category = button["type"]
                            if selected[category] is not None:
                                message_text  = "Sorry, reset to change option"
                                message_timer = 120
                            else:
                                selected[category] = button["name"]
                                icecream_stack.add_layer(
                                    category,
                                    button["product_path"],
                                    button["product_pos"],
                                    button["product_size"],
                                )
                                if category == "flavor":
                                    drops.spawn(
                                        flavor_name = button["name"],
                                        target_pos  = button["product_pos"],
                                    )
                            break

            # GAME OVER SCREEN
            elif game_state == "game_over":
                if play_rect.collidepoint(mouse_pos):
                    round_number = 1
                    score        = 0
                    game_state   = "game"
                    start_round(round_number)

    # ── Draw ────────────────────────────────────────────────
    screen.blit(background, (0, 0))

    # ── START SCREEN ────────────────────────────────────────
    if game_state == "start":
        finished = clouds.update_and_draw(screen)
        if finished:
            round_number = 1
            score        = 0
            game_state   = "game"
            start_round(round_number)

        screen.blit(title_img, title_rect)
        draw_ui_button(screen, play_img, play_rect, mouse_pos)

    # ── GAME SCREEN ─────────────────────────────────────────
    elif game_state == "game":
        icecream_stack.update()

        # Customer
        customer.update_and_draw(screen)

        # Order visibility (difficulty: hides after N seconds in R2/R3)
        hide_after = ORDER_HIDE_AFTER[round_number - 1]
        if hide_after is not None and order_visible:
            order_hide_timer -= dt
            if order_hide_timer <= 0:
                order_visible = False

        if current_order:
            if order_visible:
                draw_order_line(screen, order_font,
                                "BASE:",     current_order["base"],    order_pos[0], order_pos[1])
                draw_order_line(screen, order_font,
                                "FLAVOR:",   current_order["flavor"],  order_pos[0], order_pos[1] + 50)
                draw_order_line(screen, order_font,
                                "TOPPINGS:", current_order["topping"], order_pos[0], order_pos[1] + 100)
            else:
                hint = order_font.render("Memorize the order!", True, (180, 60, 100))
                screen.blit(hint, (order_pos[0], order_pos[1] + 25))

        # Round & Score (stacked at 90, 126)
        screen.blit(order_font.render(f"ROUND: {round_number}/3", True, (0, 0, 0)), (90, 126))
        screen.blit(order_font.render(f"SCORE: {score}",          True, (0, 0, 0)),
                    (90, 126 + order_font.get_height() + 4))

        # Timer (1221, 125)
        time_left  -= dt
        timer_color = (200, 0, 0) if time_left <= 5 else (0, 0, 0)
        screen.blit(order_font.render(f"TIME: {max(0, int(time_left))}s", True, timer_color),
                    (1221, 125))
        if time_left <= 0:
            advance_round()

        # Machine wobble
        time_passed    += 0.05
        machine_angle   = math.sin(time_passed) * 1.5
        rot_machine     = pygame.transform.rotate(machine_img, machine_angle)

        # Ingredient buttons (wiggle + hover + grey-out when picked)
        for button in buttons:
            t        = time_passed + button["time_offset"]
            pos_x    = button["button_pos"][0] + math.sin(t * 2) * 2
            pos_y    = button["button_pos"][1] + math.cos(t * 2) * 2

            already  = selected[button["type"]] is not None
            hovered  = pygame.Rect(pos_x, pos_y, *button["button_size"]).collidepoint(mouse_pos)
            scale    = 1.15 if (hovered and not already) else 1.0
            w        = int(button["button_size"][0] * scale)
            h        = int(button["button_size"][1] * scale)
            img      = pygame.transform.scale(button["button_image"], (w, h))

            if already:
                grey = img.copy()
                grey.fill((100, 100, 100, 120), special_flags=pygame.BLEND_RGBA_MULT)
                img = grey

            srect = img.get_rect(center=(pos_x + button["button_size"][0] // 2,
                                          pos_y + button["button_size"][1] // 2))
            button["button_rect"] = srect
            screen.blit(img, srect.topleft)

        # Ice cream stack layers
        for layer in icecream_stack.get_layers_in_order():
            screen.blit(layer["image"], layer["pos"])

        # Drop effects (drawn above stack, below machine)
        drops.update_and_draw(screen)

        # Machine (on top of everything in the machine area)
        mrect = rot_machine.get_rect(center=(MACHINE_X + 115, MACHINE_Y + 171))
        screen.blit(rot_machine, mrect)

        # Reset & Submit buttons
        draw_ui_button(screen, reset_img,  reset_rect,  mouse_pos)
        draw_ui_button(screen, submit_img, submit_rect, mouse_pos)

        # Score pop animations
        for sp in score_pops:
            sp.update_and_draw(screen)
        score_pops[:] = [sp for sp in score_pops if not sp.done]

        # Toast message
        message_text, message_timer = draw_message(
            screen, message_font, message_text, message_timer, WIDTH, HEIGHT
        )

#anotherone
#hello hellooo
    # ── GAME OVER SCREEN ────────────────────────────────────
    elif game_state == "game_over":
        pw, ph = 660, 360
        px = WIDTH  // 2 - pw // 2
        py = HEIGHT // 2 - ph // 2

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

    pygame.display.update()

pygame.quit()
sys.exit()
