import pygame
import sys
import math
import random

from settings import (
    WIDTH, HEIGHT, MACHINE_X, MACHINE_Y,
    ROUND_TIMES, ORDER_HIDE_AFTER, TOTAL_ROUNDS,
    SCORE_BASE, SCORE_TIME_BONUS, BUTTONS_DATA, MAX_LIVES,
)
from logic import IceCreamStack, IceCreamOrder
from animations import CloudManager, CustomerAnimator, DropManager, ScorePop, DecorationManager
from ui import (
    draw_ui_button, draw_message, draw_hud,
    draw_game_over, draw_win_screen, SoundManager,
)

pygame.init()

# ── Background Music ─────────────────────────────────────────
try:
    pygame.mixer.music.load("assets/music/bgm.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except (FileNotFoundError, pygame.error):
    pass

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

# ── Animation & sound objects ────────────────────────────────
clouds     = CloudManager(screen_width=WIDTH)
customer   = CustomerAnimator()
drops      = DropManager()
decos      = DecorationManager()
score_pops: list[ScorePop] = []
sfx        = SoundManager()

# ── Game objects ─────────────────────────────────────────────
order_system   = IceCreamOrder()
icecream_stack = IceCreamStack()
current_order  = None

# ── Game state ───────────────────────────────────────────────
game_state       = "start"
round_number     = 1
score            = 0
lives            = MAX_LIVES
time_left        = 20.0
time_passed      = 0.0
order_visible    = True
order_hide_timer = 0.0
selected         = {"base": None, "flavor": None, "topping": None}
message_text     = ""
message_timer    = 0
timer_warned     = False
pending_round    = None   # set during customer walk-out, triggers start_round when done


# ─────────────────────────────────────────────────────────────
#  Round helpers
# ─────────────────────────────────────────────────────────────

def start_round(rnum: int):
    global current_order, time_left, order_visible, order_hide_timer
    global selected, timer_warned, pending_round

    icecream_stack.reset_stack()
    drops.clear()
    selected      = {"base": None, "flavor": None, "topping": None}
    timer_warned  = False
    pending_round = None

    current_order = order_system.generate_order()
    customer.load(current_order["customer"])

    time_left        = float(ROUND_TIMES[rnum - 1])
    order_visible    = True
    hide_after       = ORDER_HIDE_AFTER[rnum - 1]
    order_hide_timer = float(hide_after) if hide_after is not None else 0.0


def lose_life(reason: str = ""):
    """Deduct a life. If 0 remain → game over, else restart current round."""
    global lives, game_state
    lives -= 1
    if lives <= 0:
        sfx.play("gameover")
        game_state = "game_over"
    else:
        sfx.play("wrong")
        # Walk current customer out then restart the same round
        customer.walk_out()
        global pending_round
        pending_round = round_number


def advance_round():
    """Called on correct order. Walk out customer then go to next round."""
    global round_number, game_state, pending_round
    if round_number >= TOTAL_ROUNDS:
        # Completed all rounds → WIN
        sfx.play("correct")
        game_state = "win"
    else:
        sfx.play("correct")
        round_number += 1
        customer.walk_out()
        pending_round = round_number


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

            # START SCREEN
            if game_state == "start":
                if play_rect.collidepoint(mouse_pos) and not clouds.exiting:
                    sfx.play("start")
                    clouds.start_exit()

            # GAME SCREEN
            elif game_state == "game":
                if reset_rect.collidepoint(mouse_pos):
                    sfx.play("reset")
                    icecream_stack.reset_stack()
                    drops.clear()
                    selected = {"base": None, "flavor": None, "topping": None}

                elif submit_rect.collidepoint(mouse_pos):
                    b, f, t = selected["base"], selected["flavor"], selected["topping"]
                    if b is None or f is None or t is None:
                        sfx.play("wrong")
                        message_text, message_timer = "Incomplete order!", 120
                    elif (b.lower() == current_order["base"].lower()   and
                          f.lower() == current_order["flavor"].lower() and
                          t.lower() == current_order["topping"].lower()):
                        earned = SCORE_BASE + int(time_left) * SCORE_TIME_BONUS
                        score += earned
                        score_pops.append(ScorePop(order_font, f"+{earned}", x=90, y=255))
                        customer.show_reaction("heart")
                        advance_round()
                    else:
                        message_text, message_timer = "Sorry, wrong order!", 120
                        customer.show_reaction("huh")
                        lose_life()

                else:
                    for button in buttons:
                        if button["button_rect"].collidepoint(mouse_pos):
                            cat = button["type"]
                            if selected[cat] is not None:
                                sfx.play("wrong")
                                message_text, message_timer = "Sorry, reset to change option", 120
                            else:
                                sfx.play("click")
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

            # WIN / GAME OVER SCREEN — play again
            elif game_state in ("game_over", "win"):
                if play_rect.collidepoint(mouse_pos):
                    sfx.play("start")
                    round_number = 1
                    score        = 0
                    lives        = MAX_LIVES
                    pending_round = None
                    game_state   = "game"
                    start_round(round_number)

    # ── Draw ─────────────────────────────────────────────────
    screen.blit(background, (0, 0))

    # START SCREEN
    if game_state == "start":
        if clouds.update_and_draw(screen):
            round_number  = 1
            score         = 0
            lives         = MAX_LIVES
            pending_round = None
            game_state    = "game"
            start_round(round_number)
        screen.blit(title_img, title_rect)
        draw_ui_button(screen, play_img, play_rect, mouse_pos)

    # GAME SCREEN
    elif game_state == "game":
        icecream_stack.update()

        # Decorations drawn first (behind everything)
        decos.update_and_draw(screen)
        customer.update_and_draw(screen)

        # When customer finishes walking out, start the pending round
        if pending_round is not None and customer.walked_out:
            start_round(pending_round)

        # Order hide timer (difficulty)
        if ORDER_HIDE_AFTER[round_number - 1] is not None and order_visible:
            order_hide_timer -= dt
            if order_hide_timer <= 0:
                order_visible = False

        # HUD — now includes lives
        draw_hud(screen, order_font, current_order, order_visible,
                 round_number, TOTAL_ROUNDS, score, time_left,
                 lives, MAX_LIVES)

        # Countdown — only tick when not waiting for walk-out
        if pending_round is None:
            time_left -= dt
            if time_left <= 5 and not timer_warned:
                sfx.play("timer_warn")
                timer_warned = True
            if time_left <= 0:
                message_text, message_timer = "Time's up!", 90
                customer.show_reaction("frustrated")
                lose_life()

        # Machine wobble
        time_passed += 0.05
        rot_machine  = pygame.transform.rotate(machine_img, math.sin(time_passed) * 1.5)
        mrect        = rot_machine.get_rect(center=(MACHINE_X + 115, MACHINE_Y + 171))

        # Ingredient buttons (wiggle + hover + grey-out when picked)
        for button in buttons:
            t       = time_passed + button["time_offset"]
            pos_x   = button["button_pos"][0] + math.sin(t * 2) * 2
            pos_y   = button["button_pos"][1] + math.cos(t * 2) * 2
            already = selected[button["type"]] is not None
            hovered = pygame.Rect(pos_x, pos_y, *button["button_size"]).collidepoint(mouse_pos)
            scale   = 1.15 if (hovered and not already) else 1.0
            w = int(button["button_size"][0] * scale)
            h = int(button["button_size"][1] * scale)
            img = pygame.transform.scale(button["button_image"], (w, h))
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

#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
    # WIN SCREEN
    elif game_state == "win":
        draw_win_screen(screen, order_font, message_font,
                        play_img, play_rect, score, mouse_pos)

    # GAME OVER SCREEN
    elif game_state == "game_over":
        draw_game_over(screen, order_font, message_font,
                       play_img, play_rect, score, mouse_pos)

    pygame.display.update()

pygame.quit()
sys.exit()
