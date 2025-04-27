import random
import time
from room import Room
from character import Character_Class 

def create_rooms() -> list[Room]:
    """Create rooms"""

    rooms = [Room(i) for i in range(1, 1000)]
    return rooms

class Enemy:
    def __init__(self, name: str, health: int, attack: int, defense: int):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense

    def __str__(self):
        return f"{self.name} (Health: {self.health}, Attack: {self.attack}, Defense: {self.defense})"
    
    def takes_damage(self, damage):
        """Enemy health after taking damage, reduced by enemy defense"""

        damage_taken = max(0, damage - self.defense)
        self.health = max(0, self.health - damage_taken)
        if self.health == 0:
            print(f"{self.name} takes {damage_taken} damage and falls limply to the ground")
        else:
            print(f"{self.name} was hit for {damage_taken} and has {self.health}/{self.max_health} health remaining.")
        
    def attack_character(self, character):
        """Attack player using character's takes_damage logic"""

        character.takes_damage(self.attack)
    
    def lives(self):
        return self.health > 0
    
enemy_stats = {
    "Drone":        {"health_range": (30, 50), "attack_range": (5, 10), "defense_range": (0, 5)},
    "Grunt":        {"health_range": (50, 70), "attack_range": (10, 15), "defense_range": (3, 8)},
    "Elite":        {"health_range": (70, 90), "attack_range": (15, 20), "defense_range": (5, 12)},
    "Abomination":  {"health_range": (90, 120), "attack_range": (20, 30), "defense_range": (8, 15)}
}

def generate_enemy(current_room_index: int):
    """Randomly generate an enemy"""
    
    if current_room_index < 10:
        enemy_name = random.choice(["Drone", "Grunt"])
    elif current_room_index < 20:
        enemy_name = random.choice(["Drone", "Grunt", "Elite"])
    else:
        enemy_name = random.choice(["Grunt", "Elite", "Abomination"])

    stats = enemy_stats[enemy_name]
    scaling_factor = max(1, current_room_index // 5)
    health = random.randint(*stats["health_range"]) + (scaling_factor * 4)
    attack = random.randint(*stats["attack_range"]) + (scaling_factor * 2)
    defense = random.randint(*stats["defense_range"]) + (scaling_factor * 1)
    
    new_enemy = Enemy(
        name = enemy_name,
        health = health,
        attack = attack,
        defense = defense
    )
    print(f"A {new_enemy} appears from the shadows...")
    return new_enemy

def user_attacks_enemy(character: Character_Class, enemy: Enemy):
    """Character attacks enemy"""

    damage = max(0, random.randint(character.attack - 5, character.attack + 5))
    enemy.takes_damage(damage)

def combat_item_use(character: Character_Class):
    """Use item in combat"""

    character.inventory.view_inventory()
    if not character.inventory.small_items and not character.inventory.large_items:
        print("Your inventory is empty. Nothing to use.")
        return

    print("Choose an item to use:")
    all_items = character.inventory.small_items + character.inventory.large_items
    for idx, item in enumerate(all_items, 1):
        print(f"{idx}. {item.name}")

    item_choice = input("Choose an item number to use (or press Enter to cancel): ").strip()
    if not item_choice:
        return
    try:
        item_index = int(item_choice) - 1
        chosen_item = all_items[item_index]
        character.use_item(chosen_item)
        character.inventory.remove_item(chosen_item)
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid item number.")  

def encounter_enemy(character: Character_Class, rooms: list[Room], current_room_index: int) -> int:
    """Handles combat and interaction when encountering an enemy. Returns the updated room index."""
    
    enemy = generate_enemy(current_room_index)

    while enemy.lives() and character.lives():
        print(f"\n{character.name} (Health: {character.health}) vs {enemy.name} (Health: {enemy.health})")
        time.sleep(0.5)
        action = input("Do you want to attack (1), use an item (2), or run (3)? ")

        if action == '1':
            user_attacks_enemy(character, enemy)
        elif action == '2':
            combat_item_use(character)
        elif action == '3':
            base_escape_chance = 40
            escape_penalty = (current_room_index // 10) * 5  # lose 5% every 10 rooms
            escape_chance = max(5, base_escape_chance - escape_penalty)

            if random.randint(1, 100) <= escape_chance:
                print(f"{character.name} successfully runs away from the {enemy.name}!")
                current_room_index += 1 if current_room_index < len(rooms) - 1 else -1
                print(f"\nMoving to Room {rooms[current_room_index].room_id}")
                return current_room_index
            else:
                print("You failed to escape!")
        else:
            print("Not a valid choice. Choose between 1, 2, or 3")
            continue

        if enemy.lives():
            enemy.attack_character(character)

    if not enemy.lives():
        print(f"{enemy.name} has been defeated!")
    elif not character.lives():
        print("This expedition will be deemed a failure. We expected more from you.")

    return current_room_index

