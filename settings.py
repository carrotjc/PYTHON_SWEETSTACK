# settings.py
# ─────────────────────────────────────────────────────────────
# All game-wide constants, positions, and button data.
# Import from here instead of scattering magic numbers everywhere.
# ─────────────────────────────────────────────────────────────

# ── Screen ───────────────────────────────────────────────────
WIDTH  = 1440
HEIGHT = 1024

# ── Machine ──────────────────────────────────────────────────
MACHINE_X = 859
MACHINE_Y = 63

# ── Order card position ──────────────────────────────────────
ORDER_POS = (141, 347)

# ── Customer walk-in ─────────────────────────────────────────
CUSTOMER_TARGET_X  = 1048
CUSTOMER_START_X   = 1240
CUSTOMER_Y         = 368
CUSTOMER_SIZE      = (240, 269)
CUSTOMER_WALK_SPEED = 6

# ── Round config ─────────────────────────────────────────────
#   Round 1 (20s) — order always visible
#   Round 2 (15s) — order hides after 8s
#   Round 3  (8s) — order hides after 3s
ROUND_TIMES      = [20, 15, 8]
ORDER_HIDE_AFTER = [None, 8, 3]
TOTAL_ROUNDS     = 3

# ── Score ────────────────────────────────────────────────────
SCORE_BASE       = 100   # flat points per correct order
SCORE_TIME_BONUS = 5     # extra points per second remaining

# ── Cloud positions ──────────────────────────────────────────
CLOUD_DATA = [
    {"path": "assets/clouds/cloud1.png", "ox": 378,  "oy": 67,  "w": 183,    "h": 113, "exit": "left"},
    {"path": "assets/clouds/cloud2.png", "ox": -64,  "oy": 195, "w": 304.35, "h": 170, "exit": "left"},
    {"path": "assets/clouds/cloud3.png", "ox": -34,  "oy": 622, "w": 380,    "h": 133, "exit": "left"},
    {"path": "assets/clouds/cloud4.png", "ox": 1014, "oy": 0,   "w": 499,    "h": 255, "exit": "right"},
    {"path": "assets/clouds/cloud5.png", "ox": 1200, "oy": 429, "w": 313,    "h": 193, "exit": "right"},
    {"path": "assets/clouds/cloud6.png", "ox": 317,  "oy": 844, "w": 806.04, "h": 120, "exit": "right"},
]
CLOUD_EXIT_SPEED = 8

# ── Drop nozzle ──────────────────────────────────────────────
NOZZLE_X = 975
NOZZLE_Y = 390

DROP_PATHS = {
    "caramel":    "assets/drops/drops_caramel.png",
    "chocolate":  "assets/drops/drops_chocolate.png",
    "strawberry": "assets/drops/drops_strawberry.png",
    "avocado":    "assets/drops/drops_avocado.png",
}

# ── Ingredient buttons ───────────────────────────────────────
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