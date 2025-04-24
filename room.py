import random 
from inventory import Character_Inventory, Item
current_room_index = 0

small_loot_pool = [
    ("Bandages", 'heal', 10, 0, 0),
    ("Syringe", 'heal', 7, random.randint(2, 5), 0),
    ("Experimental Ammunition", 'weapon', 0, random.randint(1, 3), 0),
    ("Duct Tape", 'heal', 3, 0, 0),
    ("MedKit", 'heal', 15, 0, 0),
    ("Wrappings", 'heal', 2, 0, 1),
]

large_loot_pool = [
    ("Riot Shield", 'shield', 0, 0, 7),
    ("Repair Kit", 'heal', random.randint(15, 30), 0, 0),
    ("Assault Rifle", 'weapon', 0, random.randint(7, 10), 0),
    ("Flamethrower", 'weapon', 0, random.randint(5, 7), 0),
    ("Broken Pipe", 'weapon', 0, random.randint(3, 6), 0),
    ("Wall Panel", 'shield', 0, 0, 3),
    ("Fire Extinguisher", 'weapon', 0, random.randint(2, 4), 0),
    ("Corpse", 'shield', 0, 0, random.randint(4, 5)),
]

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

        effects = {
            "hazardous waste": self.apply_hazardous_waste,
            "burning": self.apply_burning,
            "stim_shot": self.apply_stim_shot,
            "enemy_encounter": self.apply_enemy_encounter,
            "nothing": self.apply_nothing
        }
        chosen_effect = random.choice(list(effects.keys()))

        if chosen_effect == "enemy_encounter":
            effects[chosen_effect](character, rooms, current_room_index)
        else:
            effects[chosen_effect](character, rooms)

    def apply_hazardous_waste(self, character, _):
        damage = random.randint(5, 15)
        character.takes_damage(damage)
        print(f"You step in spilled waste. You take {damage} damage and are now at {character.health}/{character.max_health} health.")

    def apply_burning(self, character, _):
        damage = random.randint(3, 7)
        character.takes_damage(damage)
        print(f"You push through flames engulfing the room.\nYou take {damage} damage and are now at {character.health}/{character.max_health} health.")

    def apply_stim_shot(self, character, _):
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
                loot_item = Item.from_loot_data(random.choice(small_loot_pool), 'small')
                character.inventory.add_item(loot_item)

            for _ in range(self.large_loot_count):
                loot_item = Item.from_loot_data(random.choice(large_loot_pool), 'large')
                character.inventory.add_item(loot_item)

            self.small_loot_count = 0
            self.large_loot_count = 0
        else:
            print("You do not find anything in the room.")

    def generate_loot(self):
        self.small_loot_count = random.randint(1, 3) 
        self.large_loot_count = random.randint(0, 1) 