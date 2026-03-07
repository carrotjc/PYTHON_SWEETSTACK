# main.py
import pygame
import sys
import math
import random
from logic import IceCreamStack

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
game_state = "start"   # start | game | end

# ---------------------------
# Background
# ---------------------------
background = pygame.image.load("assets/backgroundfinal.png").convert()

# ---------------------------
# Start Screen Assets
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

machine_x = 859
machine_y = 63

# ---------------------------
# Buttons Data
# ---------------------------
buttons_data = [

    # BASES
    {"type": "base", "button_path": "assets/buttons/base_cone.png",
     "product_path": "assets/product/cone.png",
     "button_pos": (422, 811), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},

    {"type": "base", "button_path": "assets/buttons/base_cup.png",
     "product_path": "assets/product/cup.png",
     "button_pos": (422, 877), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},

    {"type": "base", "button_path": "assets/buttons/base_bowl.png",
     "product_path": "assets/product/bowl.png",
     "button_pos": (422, 942), "button_size": (51, 50),
     "product_pos": (902, 532), "product_size": (145, 143)},

    # FLAVORS
    {"type": "flavor", "button_path": "assets/buttons/flavor_caramel.png",
     "product_path": "assets/product/caramel.png",
     "button_pos": (556, 833), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},

    {"type": "flavor", "button_path": "assets/buttons/flavor_chocolate.png",
     "product_path": "assets/product/chocolate.png",
     "button_pos": (551, 914), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},

    {"type": "flavor", "button_path": "assets/buttons/flavor_strawberry.png",
     "product_path": "assets/product/strawberry.png",
     "button_pos": (633, 833), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},

    {"type": "flavor", "button_path": "assets/buttons/flavor_avocado.png",
     "product_path": "assets/product/avocado.png",
     "button_pos": (633, 914), "button_size": (70, 50),
     "product_pos": (906, 475), "product_size": (136, 98)},

    # TOPPINGS
    {"type": "topping", "button_path": "assets/buttons/toppings_cherry.png",
     "product_path": "assets/product/cherry.png",
     "button_pos": (858, 832), "button_size": (82, 59),
     "product_pos": (906, 440), "product_size": (136, 98)},

    {"type": "topping", "button_path": "assets/buttons/toppings_syrup.png",
     "product_path": "assets/product/syrup.png",
     "button_pos": (759, 832), "button_size": (82, 59),
     "product_pos": (906, 475), "product_size": (136, 98)},

    {"type": "topping", "button_path": "assets/buttons/toppings_matcha.png",
     "product_path": "assets/product/matcha.png",
     "button_pos": (758, 907), "button_size": (82, 59),
     "product_pos": (906, 475), "product_size": (136, 98)},

    {"type": "topping", "button_path": "assets/buttons/toppings_nuts.png",
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
# Ice Cream Stack System
# ---------------------------
icecream_stack = IceCreamStack()

time_passed = 0
running = True

# ---------------------------
# GAME LOOP
# ---------------------------
while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # START SCREEN
            if game_state == "start":

                if play_rect.collidepoint(mouse_pos):

                    icecream_stack.reset_stack()
                    game_state = "game"

            # GAME SCREEN
            elif game_state == "game":

                for button in buttons:

                    if button["button_rect"].collidepoint(mouse_pos):

                        icecream_stack.add_layer(
                            button["type"],
                            button["product_path"],
                            button["product_pos"],
                            button["product_size"]
                        )

    # ---------------------------
    # DRAW BACKGROUND
    # ---------------------------
    screen.blit(background, (0, 0))

    # ---------------------------
    # START SCREEN
    # ---------------------------
    if game_state == "start":

        screen.blit(title_img, title_rect)
        screen.blit(play_img, play_rect)

    # ---------------------------
    # GAME SCREEN
    # ---------------------------
    elif game_state == "game":

        icecream_stack.update()

        time_passed += 0.05

        machine_angle = math.sin(time_passed) * 1.5
        rotated_machine = pygame.transform.rotate(machine, machine_angle)

        # BUTTONS
        for button in buttons:

            t = time_passed + button["time_offset"]

            wiggle_x = math.sin(t * 2) * 2
            wiggle_y = math.cos(t * 2) * 2

            pos_x = button["button_pos"][0] + wiggle_x
            pos_y = button["button_pos"][1] + wiggle_y

            mouse_hover = pygame.Rect(
                pos_x, pos_y,
                *button["button_size"]
            ).collidepoint(mouse_pos)

            scale = 1.15 if mouse_hover else 1.0

            w = int(button["button_size"][0] * scale)
            h = int(button["button_size"][1] * scale)

            scaled_img = pygame.transform.scale(
                button["button_image"], (w, h)
            )

            scaled_rect = scaled_img.get_rect(
                center=(pos_x + button["button_size"][0] // 2,
                        pos_y + button["button_size"][1] // 2)
            )

            button["button_rect"] = scaled_rect

            screen.blit(scaled_img, scaled_rect.topleft)

        # ICE CREAM STACK
        for layer in icecream_stack.get_layers_in_order():
            screen.blit(layer["image"], layer["pos"])

        # MACHINE
        rect = rotated_machine.get_rect(
            center=(machine_x + 115, machine_y + 171)
        )

        screen.blit(rotated_machine, rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()