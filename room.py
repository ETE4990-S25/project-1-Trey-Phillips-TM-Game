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
            if self.room_type == 'left_generator_room':
                self.fix_generator(character, 'left')
            elif self.room_type == 'right_generator_room':
                self.fix_generator(character, 'right')
            elif self.room_type == 'reactor_room':
                self.start_reactor_meltdown(character)
    
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

    def fix_generator(self, character, side):
            if side == 'left':
                self.solve_generator_puzzle(character, 'left')
            elif side == 'right':
                self.solve_generator_puzzle(character, 'right')

    def solve_generator_puzzle(self, character, side):
        if not character.left_generator_fixed and side == "left":
            solved = character.solve_generator_puzzle("left")
            if solved:
                print(f"The left generator is now fixed.")
        elif not character.right_generator_fixed and side == "right":
            solved = character.solve_generator_puzzle("right")
            if solved:
                print(f"The right generator is now fixed.")
                
    def start_reactor_meltdown(self, character):
        character.start_reactor_meltdown()