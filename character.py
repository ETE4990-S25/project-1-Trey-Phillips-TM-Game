from inventory import Character_Inventory
class Character_Class: #initialize character classes/weapons/stats
    def __init__(self, name, weapon, health, attack, defense):
        self.name = name
        self.weapon = weapon
        self.inventory = Character_Inventory()
        self.health = health
        self.attack = attack
        self.defense = defense
        self.reactor_meltdown_started = False
        self.equipped_large_items = []
        self.quest_log = [] 
        self.completed_puzzles = []

    def use_item(self, item):
        if item.item_type == "heal":
            item.use(self)
            if item in self.inventory.small_items:
                self.inventory.remove_item(item)
        elif item.item_type == "weapon":
            self.apply_weapon(item)
            if item in self.inventory.small_items:
                self.inventory.remove_item(item)
        elif item.item_type == "shield":
            self.apply_shield(item)
            if item in self.inventory.small_items:
                self.inventory.remove_item(item)
        else:
            print(f"You are unable to use {item.name} at this time.")
    
    def apply_weapon(self, weapon=None):
        if weapon:
            self.attack += weapon.effect
            print(f"Weapon equipped: {weapon.name}. Attack is now {self.attack}.")
        else:
            print(f"You decide to continue with your current weapon. Attack is {self.attack}.")

    def apply_shield(self, shield=None):
        if shield:
            self.defense += shield.effect
            print(f"You raise your {shield.name}. Defense is now {self.defense}.")
        else:
            print(f"Your arm lays bare. Defense is {self.defense}.")
    
    def equip_large_item(self, item):
        if item.size == "large":
            self.equipped_large_items.append(item)
            self.attack += item.attack
            self.defense += item.defense
            print(f"You equip {item.name}. Your attack is now {self.attack} and defense is {self.defense}.")

    def unequip_large_item(self, item):
        if item in self.equipped_large_items:
            self.equipped_large_items.remove(item)
            self.attack -= item.attack
            self.defense -= item.defense
            print(f"You unequip {item.name}. Your attack is now {self.attack} and defense is {self.defense}.")

    def takes_damage(self, damage):
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        if self.health < 0:
            self.health = 0
        print(f"You are hit for {damage_taken} and have {self.health} health remaining.")

    def lives(self):
        return self.health > 0
    
    def heal(self, healing_amount):
        self.health += healing_amount
        print(f"You heal {healing_amount} and now have {self.health} remaining.")
    
    def update_stats(self):
        self.attack = 10
        self.defense = 5 
        self.apply_weapon()
        self.apply_shield()
    
    def add_quest(self, quest):
        self.quest_log.append(quest)

    def check_quests(self):
        print("Current Objectives:")
        for quest in self.quest_log:
            print(f"{quest.description}: {quest.check_status()}")

    def check_reactor_meltdown(self):
        generator_status = all(quest.is_completed for quest in self.quest_log if "Start the" in quest.description)
    
        if generator_status:
            self.reactor_meltdown_started = True
            print(f"Both generators have been started. Reactor meltdown initiated.")
            return True
        return False

    def start_reactor_meltdown(self):
        if not self.reactor_meltdown_started:
            print("Initiating reactor meltdown.")
            self.reactor_meltdown_started = True
        else:
            print("Stop my child. You've already won.")
    
    def solve_puzzle(self, puzzle):
        print(puzzle.description)
        player_input = input("Enter your answer: ")
        puzzle.attempt_solution(player_input)
        if puzzle.solved:
            self.completed_puzzles.append(puzzle)

class Character_Creator:
    def __init__(self):
        self.classes = {
            1: {"name": "Engineer", "weapon": "Plasma Cutter", "health": 120, "attack": 8, "defense": 4},
            2: {"name": "Overseer", "weapon": "Pistol", "health": 100, "attack": 12, "defense": 5},
            3: {"name": "Scientist", "weapon": "Experimental Rifle", "health": 80, "attack": 16, "defense": 3},
            4: {"name": "Security Guard", "weapon": "Assault Rifle", "health": 150, "attack": 10, "defense": 7}
        }

    def create_character(self):
        print("Choose your character class:")
        for class_id, class_info in self.classes.items():
            print(f"{class_id}. {class_info['name']}")

        while True:
            try:
                class_choice = int(input("Enter the number of your chosen class: "))
                if class_choice in self.classes:
                    chosen_class = self.classes[class_choice]
                    character = Character_Class(
                        name=input("Enter your character's name: "),
                        weapon=chosen_class["weapon"],
                        health=chosen_class["health"],
                        attack=chosen_class["attack"],
                        defense=chosen_class["defense"],
                    )
                    print(f"You have chosen the {chosen_class['name']} class.")
                    return character
                else:
                    print("The company does not hire that profession. Please choose from our existing list.")
            except ValueError:
                print("Please enter a number corresponding to the class.")
        