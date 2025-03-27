import random
from room import Room
from inventory import Item, Character_Inventory
from character import Character_Class

def create_rooms():
    rooms = []
    for i in range(1, 1000):
        room = Room(i)
        rooms.append(room)

    random.shuffle(rooms) 
    return rooms

class Enemy:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
    
    def take_damage(self, damage):
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        if self.health < 0:
            self.health = 0
        print(f"{self.name} is hit for {damage_taken} and has {self.health} health remaining.")
        
    def attack_character(self, character):
        damage_dealt = max(0, self.attack - character.defense)
        character.health -= damage_dealt
        if character.health < 0:
            character.health = 0
        print(f"{self.name} swings for {damage_dealt} damage. You have {character.health} health left.")
    
    def lives(self):
        return self.health > 0
    
enemy_stats = {
    "Drone": {
        "health_range": (30, 50),
        "attack_range": (5, 10),
        "defense_range": (0, 5)
    },
    "Grunt": {
        "health_range": (50, 70),
        "attack_range": (10, 15),
        "defense_range": (3, 8)
    },
    "Elite": {
        "health_range": (70, 90),
        "attack_range": (15, 20),
        "defense_range": (5, 12)
    },
    "Abomination": {
        "health_range": (90, 120),
        "attack_range": (20, 30),
        "defense_range": (8, 15)
    }
}

def encounter_enemy(character, rooms):
    print("Something stares at you in the darkness.")

    enemy_name = random.choice(["Drone", "Grunt", "Elite", "Abomination"])
    stats = enemy_stats[enemy_name]
    enemy_health = random.randint(stats["health_range"][0], stats["health_range"][1])
    enemy_attack = random.randint(stats["attack_range"][0], stats["attack_range"][1])
    enemy_defense = random.randint(stats["defense_range"][0], stats["defense_range"][1])
    enemy = Enemy(name=enemy_name, health=enemy_health, attack=enemy_attack, defense=enemy_defense)
    
    print(f"You step into the room and the {enemy.name} attacks.")

    while enemy.lives() and character.lives():
        print(f"\n{character.name} (Health: {character.health}) vs {enemy.name} (Health: {enemy.health})")

        action = input("Do you want to attack (1), use an item (2), or run (3)? ")
        if action == '1':
            damage = random.randint(character.attack - 5, character.attack + 5) - enemy.defense
            damage = max(damage, 0) 
            enemy.take_damage(damage)
            if not enemy.lives():
                print(f"{enemy.name} has been defeated!")
                break
        elif action == '2':
            character.inventory.view_inventory()
            print("Choose an item to use.")
            if character.inventory.small_items or character.inventory.large_items:
                print("Your inventory: ")
                if character.inventory.small_items:
                    print("Small Items:")
                    for idx, item in enumerate(character.inventory.small_items, 1):
                        print(f"{idx}. {item.name}")
                if character.inventory.large_items:
                    print("Large Items:")
                    for idx, item in enumerate(character.inventory.large_items, 1):
                        print(f"{idx}. {item.name}")
                
                item_choice = input("Choose an item number to use (or press Enter to cancel): ").strip()

                if item_choice: 
                    try:
                        item_idx = int(item_choice) - 1
                        if 0 <= item_idx < len(character.inventory.small_items):
                            item = character.inventory.small_items[item_idx]
                            character.use_item(item) 
                            character.inventory.remove_item(item)  
                        elif 0 <= item_idx < len(character.inventory.large_items):
                            item = character.inventory.large_items[item_idx]
                            character.use_item(item)  
                            character.inventory.remove_item(item) 
                        else:
                            print("Invalid choice, please select a valid item.")
                    except ValueError:
                        print("Invalid input, please enter a number.")
            else:
                print("Your inventory is empty. Nothing to use.")
        elif action == '3':
            print("You attempt to run past the monster.")
            escape_chance = random.randint(1, 100)
            success_threshold = 40

            if escape_chance <= success_threshold:
                print(f"{character.name} successfully runs away from the {enemy.name}!")
                if current_room_index < len(rooms) - 1:
                    current_room_index += 1
                    print(f"\nMoving to Room {rooms[current_room_index].room_id}...")
                else:
                    print("You realize you're at the last room")
                    current_room_index -= 1
                    print(f"\nMoving to Room {rooms[current_room_index].room_id}...")
                break
        else:
            print("Not a valid choice. Choose between 1, 2, or 3")
            continue

        if enemy.lives():
            enemy.attack_character(character)
            if not character.lives():
                return

