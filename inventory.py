from jsonparse import parse_value

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
    
        self.effect_value = {
            "heal": heal,
            "weapon": attack,
            "armor": defense
        }.get(self.item_type, 0)

    def use(self, character):
        if self.item_type == "heal":
            self.heal_character(character)
        elif self.item_type == "weapon":
            self.increase_attack(character)
        elif self.item_type == "armor":
            self.increase_defense(character)
        else:
            print(f"Warning: Unhandled item type '{self.item_type}' for {self.name}")
            print(f"{self.name} has no effect on {character.name}.")

    def heal_character(self, character):
        character.heal(self.effect_value)
        print(f"{character.name} is healed for {self.effect_value} health.")

    def increase_attack(self, character):
        character.attack += self.effect_value
        print(f"{character.name}'s attack increased by {self.effect_value}.")

    def increase_defense(self, character):
        character.defense += self.effect_value
        print(f"{character.name}'s defense increased by {self.effect_value}.")

    def item_description(self):
        return f"{self.name} ({'Large' if self.size == 'large' else 'Small'}) | Heal: {self.heal}, Attack: {self.attack}, Defense: {self.defense}"

class Character_Inventory: 
    """managable inventory system to add/remove gained items"""

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
            print("You can only carry two large items. You've only got two hands after all.")
    
    def remove_item(self, item):
        if item in self.large_items:
            self.large_items.remove(item)
            print(f"You equip the {item.name}.")
        elif item in self.small_items:
            self.small_items.remove(item)
            print(f"You use the {item.name}.")
        else:
            print(f"{item.name} is not in your inventory.")
    
    def view_inventory(self):
        print("You peer into your bag, finding: ")
        if not self.small_items and not self.large_items:
            print("Nothing...You sure you're prepared for this mission?")
            return

        for item in sorted(self.small_items, key=lambda x: x.name):
            print(f" - {item.item_description()}")
        for item in sorted(self.large_items, key=lambda x: x.name):
            print(f" - {item.item_description()}")