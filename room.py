import json
from jsonparse import parse_value
import random 
from inventory import Item
current_room_index = 0

def loot_lists_json(filepath, size):
    """load small and large items from jsons"""

    try:
        with open(filepath, 'r') as f:
            loot_data = json.load(f)
            item_list = []
            for item in loot_data:
                item_list.append(Item(
                    name = item['name'],
                    size = size,
                    item_type = item['type'],
                    heal = parse_value(item.get('heal', 0)),
                    attack = parse_value(item.get('attack', 0)),
                    defense = parse_value(item.get('defense', 0))
                ))
            return item_list
    except Exception as e:
        print(f"Could not load loot from {filepath}: {e}")
        return []
    
small_loot_pool = loot_lists_json('small_loot_list.json', 'small')
large_loot_pool = loot_lists_json('large_loot_list.json', 'large')     

class Room: 
    """Create rooms and keep track of whether they've been visited"""

    def __init__(self, room_id, room_type = None):
        self.room_id = room_id
        self.room_type = room_type
        self.visited = False
        self.effect = None
        self.small_loot_count = 0
        self.large_loot_count = 0
        self.enemy = None
    
    def apply_random_effect(self, character, rooms, current_room_index):
        """Random chance events as the user enters new rooms"""

        effect = random.choice(["hazardous waste", "burning", "stim_shot", "enemy_encounter", "nothing"])
        if effect == "hazardous waste":
            self.apply_hazardous_waste(character)
        elif effect == "burning":
            self.apply_burning(character)
        elif effect == "stim_shot":
            self.apply_stim_shot(character)
        elif effect == "enemy_encounter":
            self.apply_enemy_encounter(character, rooms, current_room_index)
        elif effect == "nothing":
            self.apply_nothing(character)

    def apply_hazardous_waste(self, character):
        damage = random.randint(5, 15)
        actual_damage = character.takes_damage(damage)
        print(f"You step in spilled waste. You take {actual_damage} damage and are now at {character.health}/{character.max_health} health.")

    def apply_burning(self, character):
        damage = random.randint(3, 7)
        actual_damage = character.takes_damage(damage)
        print(f"You push through flames engulfing the room.\nYou take {actual_damage} damage and are now at {character.health}/{character.max_health} health.")

    def apply_stim_shot(self, character):
        stim_shot = random.randint(6, 10)
        character.heal(stim_shot)
        print(f"As you enter the room, you begin to feel rejuvenated. \nA surge of energy washes over you and you realize you are now at {character.health}/{character.max_health} health.")

    def apply_enemy_encounter(self, character, rooms, current_room_index):
        from enemy import encounter_enemy
        encounter_enemy(character, rooms, current_room_index)

    def apply_nothing(self, character):
        print("You scan the room. It looks to be safe.")

    def visit(self, character, rooms, current_room_index):
        """As user visits new room, apply random room effect with a chance for an enemy encounter on top of that"""

        if not self.visited:
            self.visited = True
            self.apply_random_effect(character, rooms, current_room_index)
            self.generate_loot()
            if random.randint(1, 60) <= 40:
                print("You sense something lurking in the darkness")
                from enemy import encounter_enemy
                encounter_enemy(character, rooms, current_room_index)
    
    def search_room(self, character):
        """Search the room, adding a randomly determined number of small and large items only once"""

        if self.small_loot_count > 0 or self.large_loot_count > 0:
            print(f"You search the room...")

            for _ in range(self.small_loot_count):
                loot_item = random.choice(small_loot_pool)
                character.inventory.add_item(loot_item)

            for _ in range(self.large_loot_count):
                loot_item = random.choice(large_loot_pool)
                character.inventory.add_item(loot_item)

            self.small_loot_count = 0
            self.large_loot_count = 0
        else:
            print("You do not find anything in the room.")

    def generate_loot(self):
        if small_loot_pool and large_loot_pool:
            self.small_loot_count = random.randint(1, 3) 
            self.large_loot_count = random.randint(0, 1)
        else:
            print("Loot pools are empty. No loot will be generated.")