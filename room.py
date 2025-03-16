import random 
from inventory import Character_Inventory, Item

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
    ("Wall Panel", 'shield, 0, 0, 3'),
    ("Fire Extinguisher", 'weapon', 0, random.randint(2, 4), 0),
    ("Corpse", 'shield', 0, 0, random.randint(4, 5)),
]

class Room: #create rooms and keep track of whether they've been visited
    global current_room_index

    def __init__(self, room_id, room_type = None):
        self.room_id = room_id
        self.room_type = room_type
        self.visited = False
        self.effect = None
        self.small_loot_count = 0
        self.large_loot_count = 0
        self.enemy = None

    def apply_random_effect(self, character, rooms):
        from enemy import encounter_enemy
        effects = ["hazardous waste", "burning", "stim_shot", "enemy_encounter", "nothing"]
        chosen_effect = random.choice(effects)

        if chosen_effect == "hazardous waste":
            hazardous_waste = random.randint(5, 15)
            character.health -= hazardous_waste
            print(f"You step in spilled waste. You take {hazardous_waste} damage and are now at {character.health} health.")
        elif chosen_effect == "burning":
            burning = random.randint(3, 7)
            character.health -= burning
            print(f"As you walk into the room, you begin to choke on the smoke that billows out from it. Ever fearless, you push through the flames that have engulfed the room. \nYou take {burning} damage and are now at {character.health} health.")
        elif chosen_effect == "stim_shot":
            stim_shot = random.randint(6, 10)
            character.health += stim_shot
            print(f"As you enter the room, you begin to feel rejuvenated. \nA surge of energy washes over you and you realize you are now at {character.health} health.")
        elif chosen_effect == "enemy_encounter":
            encounter_enemy(character, rooms)
        elif chosen_effect == "nothing":
            print("You enter the room and feel... nothing? This seems like a safe place to get your bearings.")

    def visit(self, character, rooms):
        if not self.visited:
            self.visited = True
            self.apply_random_effect(character, rooms)
            self.generate_loot()
    
    def search_room(self, character):
        if self.small_loot_count > 0 or self.large_loot_count > 0:
            print(f"You search the room...")

            for _ in range(self.small_loot_count):
                loot_item_data = random.choice(small_loot_pool)
                loot_item = Item(loot_item_data[0], 'small', loot_item_data[1], 
                                 effect=loot_item_data[2], heal=loot_item_data[2], 
                                 attack=loot_item_data[3], defense=loot_item_data[4])
                character.inventory.add_item(loot_item)

            for _ in range(self.large_loot_count):
                loot_item_data = random.choice(large_loot_pool)
                loot_item = Item(loot_item_data[0], 'large', loot_item_data[1], 
                                 effect=loot_item_data[2], heal=loot_item_data[2], 
                                 attack=loot_item_data[3], defense=loot_item_data[4])
                character.inventory.add_item(loot_item)
            
            self.small_loot_count = 0
            self.large_loot_count = 0

        else:
            print("You do not find anything in the room.")

    def generate_loot(self):
        self.small_loot_count = random.randint(1, 3) 
        self.large_loot_count = random.randint(0, 1) 