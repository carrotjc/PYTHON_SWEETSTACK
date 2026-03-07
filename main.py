import pygame
import sys
import math
import random
from logic import IceCreamStack, IceCreamOrder

pygame.init()

# ---------------------------
# Screen
# ---------------------------
WIDTH, HEIGHT = 1440, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sweet Stack")
clock = pygame.time.Clock()

# ---------------------------
# Game State
# ---------------------------
game_state = "start"
round_number = 1
score = 0
time_left = 20

# ---------------------------
# Font
# ---------------------------
order_font = pygame.font.Font("assets/fonts/PixelOperator.ttf", 32)
message_font = pygame.font.Font("assets/fonts/PixelOperator.ttf", 40)

# ---------------------------
# Background
# ---------------------------
background = pygame.image.load("assets/backgroundfinal.png").convert()

# ---------------------------
# Start Screen
# ---------------------------
title_img = pygame.image.load("assets/sweetstack.png").convert_alpha()
title_img = pygame.transform.scale(title_img, (922, 375))
title_rect = title_img.get_rect(topleft=(259, 250))

play_img = pygame.image.load("assets/playbutton.png").convert_alpha()
play_img = pygame.transform.scale(play_img, (483, 107))
play_rect = play_img.get_rect(topleft=(478, 667))

# ---------------------------
# Machine
# ---------------------------
machine = pygame.image.load("assets/machine.png").convert_alpha()
machine = pygame.transform.scale(machine, (230, 343))
machine_x, machine_y = 859, 63

# ---------------------------
# Order System
# ---------------------------
order_system = IceCreamOrder()
current_order = None
customer_img = None
customer_base_pos = (1048, 369)
customer_size = (240, 269)
customer_float_offset = 0
customer_time = 0

order_pos = (141, 347)
message_text = ""
message_timer = 0

# ---------------------------
# Buttons Data
# ---------------------------
buttons_data = [
    {"type": "base", "name": "Cone",
     "button_path": "assets/buttons/base_cone.png",
     "product_path": "assets/product/cone.png",
     "button_pos": (422, 811), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},
    {"type": "base", "name": "Cup",
     "button_path": "assets/buttons/base_cup.png",
     "product_path": "assets/product/cup.png",
     "button_pos": (422, 877), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},
    {"type": "base", "name": "Bowl",
     "button_path": "assets/buttons/base_bowl.png",
     "product_path": "assets/product/bowl.png",
     "button_pos": (422, 942), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},
    {"type": "flavor", "name": "Caramel",
     "button_path": "assets/buttons/flavor_caramel.png",
     "product_path": "assets/product/caramel.png",
     "button_pos": (556, 833), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "flavor", "name": "Chocolate",
     "button_path": "assets/buttons/flavor_chocolate.png",
     "product_path": "assets/product/chocolate.png",
     "button_pos": (551, 914), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "flavor", "name": "Strawberry",
     "button_path": "assets/buttons/flavor_strawberry.png",
     "product_path": "assets/product/strawberry.png",
     "button_pos": (633, 833), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},
    {"type": "flavor", "name": "Avocado",
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

# ---------------------------
# Load Buttons
# ---------------------------
buttons = []
for data in buttons_data:
    img = pygame.image.load(data["button_path"]).convert_alpha()
    img = pygame.transform.scale(img, data["button_size"])
    rect = img.get_rect(topleft=data["button_pos"])
    data["button_image"] = img
    data["button_rect"] = rect
    data["time_offset"] = random.uniform(0, 2 * math.pi)
    buttons.append(data)

# ---------------------------
# Reset & Submit Buttons
# ---------------------------
reset_img = pygame.image.load("assets/resetbutton.png").convert_alpha()
reset_img = pygame.transform.scale(reset_img, (246, 84))
reset_rect = reset_img.get_rect(topleft=(60, 919))

submit_img = pygame.image.load("assets/submitbutton.png").convert_alpha()
submit_img = pygame.transform.scale(submit_img, (233, 81))
submit_rect = submit_img.get_rect(topleft=(1149, 923))

# ---------------------------
# Stack & Tracking
# ---------------------------
icecream_stack = IceCreamStack()

# Track which name was selected per category (None = not yet chosen)
selected = {"base": None, "flavor": None, "topping": None}

time_passed = 0
running = True

# ---------------------------
# Round Timer
# ---------------------------
round_times = [20, 15, 8]


# ---------------------------
# Helper: advance to next round or game over
# ---------------------------
def advance_round():
    global round_number, game_state, current_order, customer_img, time_left, selected
    round_number += 1
    if round_number > 3:
        game_state = "game_over"
    else:
        icecream_stack.reset_stack()
        selected = {"base": None, "flavor": None, "topping": None}
        current_order = order_system.generate_order()
        customer_img = pygame.image.load(current_order["customer"]).convert_alpha()
        customer_img = pygame.transform.scale(customer_img, customer_size)
        time_left = round_times[round_number - 1]


# ---------------------------
# Draw Order Line
# ---------------------------
def draw_order_line(label, value, x, y):
    label_text = order_font.render(label, True, (0, 0, 0))
    value_text = order_font.render(value, True, (200, 0, 0))
    screen.blit(label_text, (x, y))
    value_x = x + label_text.get_width() + 10
    screen.blit(value_text, (value_x, y))


# ---------------------------
# Draw Message (toast-style)
# ---------------------------
def draw_message(msg):
    global message_timer
    if msg and message_timer > 0:
        # Semi-transparent pill background
        msg_surf = message_font.render(msg, True, (255, 255, 255))
        pad_x, pad_y = 30, 16
        w = msg_surf.get_width() + pad_x * 2
        h = msg_surf.get_height() + pad_y * 2
        box_x = WIDTH // 2 - w // 2
        box_y = HEIGHT // 2 - h // 2

        # Draw rounded rect background (dark semi-transparent)
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (30, 10, 40, 210), overlay.get_rect(), border_radius=18)
        screen.blit(overlay, (box_x, box_y))

        # Pink border accent
        pygame.draw.rect(screen, (230, 100, 160), (box_x, box_y, w, h), width=3, border_radius=18)

        # Text
        screen.blit(msg_surf, (box_x + pad_x, box_y + pad_y))

        message_timer -= 1
        if message_timer <= 0:
            return ""
    return msg


# ---------------------------
# GAME LOOP
# ---------------------------
while running:
    dt = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # ---- START SCREEN ----
            if game_state == "start":
                if play_rect.collidepoint(mouse_pos):
                    icecream_stack.reset_stack()
                    selected = {"base": None, "flavor": None, "topping": None}
                    round_number = 1
                    current_order = order_system.generate_order()
                    customer_img = pygame.image.load(current_order["customer"]).convert_alpha()
                    customer_img = pygame.transform.scale(customer_img, customer_size)
                    time_left = round_times[round_number - 1]
                    game_state = "game"

            # ---- GAME SCREEN ----
            elif game_state == "game":

                # Reset button
                if reset_rect.collidepoint(mouse_pos):
                    icecream_stack.reset_stack()
                    selected = {"base": None, "flavor": None, "topping": None}

                # Submit button
                elif submit_rect.collidepoint(mouse_pos):
                    b = selected["base"]
                    f = selected["flavor"]
                    t = selected["topping"]

                    if b is None or f is None or t is None:
                        # Incomplete order counts as wrong
                        message_text = "Sorry, wrong order!"
                        message_timer = 120
                    else:
                        base_correct    = b.lower() == current_order["base"].lower()
                        flavor_correct  = f.lower() == current_order["flavor"].lower()
                        topping_correct = t.lower() == current_order["topping"].lower()

                        if base_correct and flavor_correct and topping_correct:
                            advance_round()
                        else:
                            message_text = "Sorry, wrong order!"
                            message_timer = 120

                # Ice cream pick buttons
                else:
                    for button in buttons:
                        if button["button_rect"].collidepoint(mouse_pos):
                            category = button["type"]
                            if selected[category] is not None:
                                # Already picked this category → prompt reset
                                message_text = "Sorry, reset to change option"
                                message_timer = 120
                            else:
                                selected[category] = button["name"]
                                icecream_stack.add_layer(
                                    category,
                                    button["product_path"],
                                    button["product_pos"],
                                    button["product_size"]
                                )
                            break

            # ---- GAME OVER SCREEN ----
            elif game_state == "game_over":
                if play_rect.collidepoint(mouse_pos):
                    # Restart
                    icecream_stack.reset_stack()
                    selected = {"base": None, "flavor": None, "topping": None}
                    round_number = 1
                    current_order = order_system.generate_order()
                    customer_img = pygame.image.load(current_order["customer"]).convert_alpha()
                    customer_img = pygame.transform.scale(customer_img, customer_size)
                    time_left = round_times[round_number - 1]
                    game_state = "game"

    # ==============================
    # DRAW
    # ==============================
    screen.blit(background, (0, 0))

    # ---- START SCREEN ----
    if game_state == "start":
        screen.blit(title_img, title_rect)
        screen.blit(play_img, play_rect)

    # ---- GAME SCREEN ----
    elif game_state == "game":
        icecream_stack.update()

        # Customer float animation
        customer_time += 0.03
        customer_float_offset = math.sin(customer_time) * 6
        if customer_img:
            screen.blit(customer_img, (customer_base_pos[0], customer_base_pos[1] + customer_float_offset))

        # Order card
        if current_order:
            draw_order_line("BASE:",     current_order["base"],    order_pos[0], order_pos[1])
            draw_order_line("FLAVOR:",   current_order["flavor"],  order_pos[0], order_pos[1] + 50)
            draw_order_line("TOPPINGS:", current_order["topping"], order_pos[0], order_pos[1] + 100)

        # ---- ROUND display  (pos: 90x, 126y  |  approx 206w × 62h) ----
        round_text = order_font.render(f"ROUND {round_number}/3", True, (0, 0, 0))
        screen.blit(round_text, (90, 126))

        # ---- TIMER display  (pos: 1221x, 119y  |  approx 184w × 64h) ----
        time_left -= dt
        timer_color = (200, 0, 0) if time_left <= 5 else (0, 0, 0)   # red flash when low
        timer_text = order_font.render(f"TIME: {max(0, int(time_left))}s", True, timer_color)
        screen.blit(timer_text, (1221, 119))

        # Time up → advance (no score penalty, just move on)
        if time_left <= 0:
            advance_round()

        # Machine wobble
        time_passed += 0.05
        machine_angle = math.sin(time_passed) * 1.5
        rotated_machine = pygame.transform.rotate(machine, machine_angle)

        # Buttons with wiggle + hover scale
        for button in buttons:
            t = time_passed + button["time_offset"]
            wiggle_x = math.sin(t * 2) * 2
            wiggle_y = math.cos(t * 2) * 2
            pos_x = button["button_pos"][0] + wiggle_x
            pos_y = button["button_pos"][1] + wiggle_y
            mouse_hover = pygame.Rect(pos_x, pos_y, *button["button_size"]).collidepoint(mouse_pos)

            # Dim button if that category already selected
            already_picked = selected[button["type"]] is not None
            scale = 1.15 if (mouse_hover and not already_picked) else 1.0
            w = int(button["button_size"][0] * scale)
            h = int(button["button_size"][1] * scale)
            scaled_img = pygame.transform.scale(button["button_image"], (w, h))

            # Grey-out already-picked category buttons
            if already_picked:
                grey = scaled_img.copy()
                grey.fill((100, 100, 100, 120), special_flags=pygame.BLEND_RGBA_MULT)
                scaled_img = grey

            scaled_rect = scaled_img.get_rect(
                center=(pos_x + button["button_size"][0] // 2, pos_y + button["button_size"][1] // 2)
            )
            button["button_rect"] = scaled_rect
            screen.blit(scaled_img, scaled_rect.topleft)

        # Ice cream stack layers
        for layer in icecream_stack.get_layers_in_order():
            screen.blit(layer["image"], layer["pos"])

        # Machine on top
        rect = rotated_machine.get_rect(center=(machine_x + 115, machine_y + 171))
        screen.blit(rotated_machine, rect)

        # Reset & Submit
        screen.blit(reset_img, reset_rect)
        screen.blit(submit_img, submit_rect)

        # Message toast
        message_text = draw_message(message_text)

    # ---- GAME OVER SCREEN ----
    elif game_state == "game_over":
        # Reuse background, draw a centred panel
        panel_w, panel_h = 600, 320
        panel_x = WIDTH // 2 - panel_w // 2
        panel_y = HEIGHT // 2 - panel_h // 2
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (30, 10, 40, 220), panel.get_rect(), border_radius=24)
        screen.blit(panel, (panel_x, panel_y))
        pygame.draw.rect(screen, (230, 100, 160), (panel_x, panel_y, panel_w, panel_h), width=4, border_radius=24)

        go_text  = message_font.render("GAME OVER", True, (255, 220, 240))
        sub_text = order_font.render("Thanks for playing Sweet Stack!", True, (255, 200, 220))
        screen.blit(go_text,  go_text.get_rect(center=(WIDTH // 2, panel_y + 100)))
        screen.blit(sub_text, sub_text.get_rect(center=(WIDTH // 2, panel_y + 170)))

        # Reuse play button as "Play Again"
        screen.blit(play_img, play_rect)

    pygame.display.update()

pygame.quit()
sys.exit()