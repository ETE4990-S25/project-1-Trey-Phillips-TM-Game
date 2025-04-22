import random

class Item: 
    """small and large items to be obtained (hold 2 large, any number of small)"""
    
    def __init__(self, name, size = 'small', item_type = None, effect = None, heal = 0, attack = 0, defense = 0):
        self.name = name
        self.size = size 
        self.item_type = item_type
        self.effect = effect
        self.heal = heal
        self.attack = attack
        self.defense = defense
    
        if self.item_type == 'heal':
            self.effect_value = heal
        elif self.item_type == 'weapon':
            self.effect_value = attack
        elif self.item_type == 'shield':
            self.effect_value = defense
        else:
            self.effect_value = 0

    def use(self, character):
        if self.item_type == "heal":
            character.health += self.effect_value
            print(f"{character.name} is healed for {self.effect_value} health.")
        elif self.item_type == "weapon":
            character.attack += self.effect_value
            print(f"{character.name}'s attack increased by {self.effect_value}.")
        elif self.item_type == "shield":
            character.defense += self.effect_value
            print(f"{character.name}'s defense increased by {self.effect_value}.")
        else:
            print(f"{self.name} has no effect on {character.name}.")

class Character_Inventory: #managable inventory system to add/remove gained items
    def __init__(self):
        self.small_items = [] 
        self.large_items = []
    
    def add_item(self, item):
        if item.size == 'large' and len(self.large_items) < 2:
            self.large_items.append(item)
            print(f"You pick up {item.name}. It looks too heavy for the bag, you'll have to put it in your hand.")
        elif item.size == 'small':
            self.small_items.append(item)
            print(f"You pick up {item.name} and add it to your bag.")
        else:
            print("You can can only carry two large items. You've only got two hands after all.")
    
    def remove_item(self, item):
        if item in self.large_items:
            self.large_items.remove(item)
            print(f"You drop the {item.name}.")
        elif item in self.small_items:
            self.small_items.remove(item)
            print(f"You drop the {item.name}.")
        else:
            print(f"{item.name} is not in your inventory.")
    
    def view_inventory(self): 
        print("You peer into your bag, finding: ")
        for item in self.small_items:
            print(f" - {item.name} (Small) | Heal: {item.heal}, Attack: {item.attack}, Defense: {item.defense}")
        for item in self.large_items:
            print(f" - {item.name} (Large) | Heal: {item.heal}, Attack: {item.attack}, Defense: {item.defense}")
