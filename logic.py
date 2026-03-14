import pygame
import random


class IceCreamStack:

    def __init__(self):
        self.stack = {"base": None, "flavor": None, "topping": None}
        self.animations = {}

    def add_layer(self, layer_type, image_path, pos, size):
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.scale(img, size)
        start_y = pos[1] - 50
        self.stack[layer_type] = {"image": img, "pos": [pos[0], start_y], "target_y": pos[1]}
        self.animations[layer_type] = True

    def update(self):
        for layer_type in list(self.animations):
            if self.animations[layer_type]:
                layer = self.stack[layer_type]
                if layer["pos"][1] < layer["target_y"]:
                    layer["pos"][1] += 5
                else:
                    layer["pos"][1] = layer["target_y"]
                    self.animations[layer_type] = False

    def get_layers_in_order(self):
        ordered_layers = []
        for layer in ["base", "flavor", "topping"]:
            if self.stack[layer] is not None:
                ordered_layers.append(self.stack[layer])
        return ordered_layers

    def reset_stack(self):
        self.stack = {"base": None, "flavor": None, "topping": None}
        self.animations = {}


class IceCreamOrder:

    def __init__(self):
        self.bases = ["Cone", "Cup", "Bowl"]
        self.flavors = ["Caramel", "Chocolate", "Strawberry", "Avocado"]
        self.toppings = ["Cherry", "Syrup", "Matcha", "Nuts"]
        self.customers = [
            "assets/customers/character1.png",
            "assets/customers/character2.png",
            "assets/customers/character3.png",
            "assets/customers/character4.png",
            "assets/customers/character5.png"
        ]
        self.order = None

    def generate_order(self):
        self.order = {
            "base": random.choice(self.bases),
            "flavor": random.choice(self.flavors),
            "topping": random.choice(self.toppings),
            "customer": random.choice(self.customers)
        }
        return self.order