import random 
from inventory import Item
current_room_index = 0

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