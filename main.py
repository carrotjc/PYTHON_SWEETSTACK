import pygame
import sys
import math
import random
 
from settings import (
    WIDTH, HEIGHT, MACHINE_X, MACHINE_Y,
    ROUND_TIMES, ORDER_HIDE_AFTER, TOTAL_ROUNDS,
    SCORE_BASE, SCORE_TIME_BONUS, BUTTONS_DATA,
)
from logic import IceCreamStack, IceCreamOrder
from animations import CloudManager, CustomerAnimator, DropManager, ScorePop
from ui import draw_ui_button, draw_message, draw_hud, draw_game_over
 
pygame.init()
 
# ── Window ───────────────────────────────────────────────────
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sweet Stack")
clock  = pygame.time.Clock()
 
# ── Fonts ────────────────────────────────────────────────────
order_font   = pygame.font.Font("assets/fonts/PixelOperator.ttf", 32)
message_font = pygame.font.Font("assets/fonts/PixelOperator.ttf", 40)
 
# ── Static assets ────────────────────────────────────────────
background  = pygame.image.load("assets/backgroundfinal.png").convert()
 
title_img   = pygame.transform.scale(
    pygame.image.load("assets/sweetstack.png").convert_alpha(), (922, 375))
title_rect  = title_img.get_rect(topleft=(259, 250))
 
play_img    = pygame.transform.scale(
    pygame.image.load("assets/playbutton.png").convert_alpha(), (483, 107))
play_rect   = play_img.get_rect(topleft=(478, 667))
 
machine_img = pygame.transform.scale(
    pygame.image.load("assets/machine.png").convert_alpha(), (230, 343))
 
reset_img   = pygame.transform.scale(
    pygame.image.load("assets/resetbutton.png").convert_alpha(), (246, 84))
reset_rect  = reset_img.get_rect(topleft=(60, 919))
 
submit_img  = pygame.transform.scale(
    pygame.image.load("assets/submitbutton.png").convert_alpha(), (233, 81))
submit_rect = submit_img.get_rect(topleft=(1149, 923))
 
# ── Ingredient buttons ───────────────────────────────────────
buttons = []
for data in BUTTONS_DATA:
    img  = pygame.transform.scale(
        pygame.image.load(data["button_path"]).convert_alpha(),
        data["button_size"])
    data["button_image"] = img
    data["button_rect"]  = img.get_rect(topleft=data["button_pos"])
    data["time_offset"]  = random.uniform(0, 2 * math.pi)
    buttons.append(data)
 
# ── Animation objects ────────────────────────────────────────
clouds     = CloudManager(screen_width=WIDTH)
customer   = CustomerAnimator()
drops      = DropManager()
score_pops: list[ScorePop] = []
 
# ── Game objects ─────────────────────────────────────────────
order_system   = IceCreamOrder()
icecream_stack = IceCreamStack()
current_order  = None
 
# ── Game state ───────────────────────────────────────────────
game_state       = "start"
round_number     = 1
score            = 0
time_left        = 20.0
time_passed      = 0.0
order_visible    = True
order_hide_timer = 0.0
selected         = {"base": None, "flavor": None, "topping": None}
message_text     = ""
message_timer    = 0
 
 
# ─────────────────────────────────────────────────────────────
#  Round helpers
# ─────────────────────────────────────────────────────────────
 
def start_round(rnum: int):
    global current_order, time_left, order_visible, order_hide_timer, selected
 
    icecream_stack.reset_stack()
    drops.clear()
    selected = {"base": None, "flavor": None, "topping": None}
 
    current_order = order_system.generate_order()
    customer.load(current_order["customer"])
 
    time_left        = float(ROUND_TIMES[rnum - 1])
    order_visible    = True
    hide_after       = ORDER_HIDE_AFTER[rnum - 1]
    order_hide_timer = float(hide_after) if hide_after is not None else 0.0
 
 
def advance_round():
    global round_number, game_state
    round_number += 1
    if round_number > TOTAL_ROUNDS:
        game_state = "game_over"
    else:
        start_round(round_number)
 
 
# ─────────────────────────────────────────────────────────────
#  GAME LOOP
# ─────────────────────────────────────────────────────────────
running = True
 
while running:
    dt        = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()
 
    # ── Events ───────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
 
            if game_state == "start":
                if play_rect.collidepoint(mouse_pos) and not clouds.exiting:
                    clouds.start_exit()
 
            elif game_state == "game":
                if reset_rect.collidepoint(mouse_pos):
                    icecream_stack.reset_stack()
                    drops.clear()
                    selected = {"base": None, "flavor": None, "topping": None}
 
                elif submit_rect.collidepoint(mouse_pos):
                    b, f, t = selected["base"], selected["flavor"], selected["topping"]
                    if b is None or f is None or t is None:
                        message_text, message_timer = "Sorry, wrong order!", 120
                    elif (b.lower() == current_order["base"].lower()    and
                          f.lower() == current_order["flavor"].lower()  and
                          t.lower() == current_order["topping"].lower()):
                        earned  = SCORE_BASE + int(time_left) * SCORE_TIME_BONUS
                        score  += earned
                        score_pops.append(ScorePop(order_font, f"+{earned}", x=90, y=210))
                        advance_round()
                    else:
                        message_text, message_timer = "Sorry, wrong order!", 120
 
                else:
                    for button in buttons:
                        if button["button_rect"].collidepoint(mouse_pos):
                            cat = button["type"]
                            if selected[cat] is not None:
                                message_text, message_timer = "Sorry, reset to change option", 120
                            else:
                                selected[cat] = button["name"]
                                icecream_stack.add_layer(
                                    cat,
                                    button["product_path"],
                                    button["product_pos"],
                                    button["product_size"],
                                )
                                if cat == "flavor":
                                    drops.spawn(button["name"], button["product_pos"])
                            break
 
            elif game_state == "game_over":
                if play_rect.collidepoint(mouse_pos):
                    round_number, score = 1, 0
                    game_state = "game"
                    start_round(round_number)
 
    # ── Draw ─────────────────────────────────────────────────
    screen.blit(background, (0, 0))
 
    # START SCREEN
    if game_state == "start":
        if clouds.update_and_draw(screen):
            round_number, score = 1, 0
            game_state = "game"
            start_round(round_number)
        screen.blit(title_img, title_rect)
        draw_ui_button(screen, play_img, play_rect, mouse_pos)
 
    # GAME SCREEN
    elif game_state == "game":
        icecream_stack.update()
        customer.update_and_draw(screen)
 
        # Order hide timer (difficulty)
        if ORDER_HIDE_AFTER[round_number - 1] is not None and order_visible:
            order_hide_timer -= dt
            if order_hide_timer <= 0:
                order_visible = False
 
        # HUD (order card + round/score/timer)
        draw_hud(screen, order_font, current_order, order_visible,
                 round_number, TOTAL_ROUNDS, score, time_left)
 
        # Countdown
        time_left -= dt
        if time_left <= 0:
            advance_round()
 
        # Machine wobble
        time_passed   += 0.05
        rot_machine    = pygame.transform.rotate(machine_img, math.sin(time_passed) * 1.5)
        mrect          = rot_machine.get_rect(center=(MACHINE_X + 115, MACHINE_Y + 171))
 
        # Ingredient buttons
        for button in buttons:
            t       = time_passed + button["time_offset"]
            pos_x   = button["button_pos"][0] + math.sin(t * 2) * 2
            pos_y   = button["button_pos"][1] + math.cos(t * 2) * 2
            already = selected[button["type"]] is not None
            hovered = pygame.Rect(pos_x, pos_y, *button["button_size"]).collidepoint(mouse_pos)
            scale   = 1.15 if (hovered and not already) else 1.0
            w, h    = int(button["button_size"][0] * scale), int(button["button_size"][1] * scale)
            img     = pygame.transform.scale(button["button_image"], (w, h))
            if already:
                grey = img.copy()
                grey.fill((100, 100, 100, 120), special_flags=pygame.BLEND_RGBA_MULT)
                img = grey
            srect = img.get_rect(center=(pos_x + button["button_size"][0] // 2,
                                          pos_y + button["button_size"][1] // 2))
            button["button_rect"] = srect
            screen.blit(img, srect.topleft)
 
        # Ice cream stack
        for layer in icecream_stack.get_layers_in_order():
            screen.blit(layer["image"], layer["pos"])
 
        # Drop effects → machine → UI buttons
        drops.update_and_draw(screen)
        screen.blit(rot_machine, mrect)
        draw_ui_button(screen, reset_img,  reset_rect,  mouse_pos)
        draw_ui_button(screen, submit_img, submit_rect, mouse_pos)
 
        # Score pops
        for sp in score_pops:
            sp.update_and_draw(screen)
        score_pops[:] = [sp for sp in score_pops if not sp.done]
 
        # Toast message
        message_text, message_timer = draw_message(
            screen, message_font, message_text, message_timer, WIDTH, HEIGHT)
 
    # GAME OVER SCREEN
    elif game_state == "game_over":
        draw_game_over(screen, order_font, message_font,
                       play_img, play_rect, score, mouse_pos)
 
    pygame.display.update()
 
pygame.quit()
sys.exit()