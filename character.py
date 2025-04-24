from inventory import Character_Inventory

class Character_Class: 
    """initialize character classes/weapons/stats"""

    def __init__(self, name, weapon, health, attack, defense):
        self.name = name
        self.weapon = weapon
        self.inventory = Character_Inventory()
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.equipped_large_items = []

    def use_item(self, item):
        """Uses item and removes it if it is a small item"""

        item_usage = {
            "heal": lambda: item.use(self),
            "weapon": lambda: item.use(self),
            "shield": lambda: item.use(self)
        }

        item_action = item_usage.get(item.item_type)

        if item_action:
            item_action()
            if item in self.inventory.small_items:
                self.inventory.remove_item(item)
        else:
            print(f"You are unable to use {item.name} at this time.")

    def equip_large_item(self, item):
        """Use large item for boost to attack/defense"""

        if item.size == "large":
            self.equipped_large_items.append(item)
            self.attack += item.attack
            self.defense += item.defense
            print(f"You equip {item.name}. Your attack is now {self.attack} and defense is {self.defense}.")

    def unequip_large_item(self, item):
        """Unequip large item and remove its bonuses"""

        if item in self.equipped_large_items:
            self.equipped_large_items.remove(item)
            self.attack -= item.attack
            self.defense -= item.defense
            print(f"You unequip {item.name}. Your attack is now {self.attack} and defense is {self.defense}.")

    def takes_damage(self, damage):
        """Damage calculations"""

        damage_taken = max(0, damage - self.defense)
        self.health = max(0, self.health - damage_taken)
        print(f"You are hit for {damage_taken} and have {self.health}/{self.max_health} health remaining.")

    def lives(self):
        return self.health > 0
    
    def heal(self, healing_amount):
        """Heal w/o going over max health"""

        current_health = self.health
        self.health = min(self.health + healing_amount, self.max_health)
        healing_amount = self.health - current_health
        print(f"You heal {healing_amount} and are now at {self.health}/{self.max_health} health.")

    def apply_weapon(self, weapon=None):
        """Applies bonus to attack"""

        if weapon:
            self.attack += weapon.effect
            print(f"Weapon equipped: {weapon.name}. Attack is now {self.attack}.")

    def apply_shield(self, shield=None):
        """Applies bonus to defense"""

        if shield:
            self.defense += shield.effect
            print(f"You raise your {shield.name}. Defense is now {self.defense}.")
    
    def __str__(self):
        """Displays character stats"""

        return f"{self.name} - Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Current Weapon: {self.weapon}"

class Character_Creator:
    """User inputted character selection"""

    def __init__(self):
        self.classes = {
            1: {"name": "Engineer", "weapon": "Plasma Cutter", "health": 120, "attack": 8, "defense": 4},
            2: {"name": "Overseer", "weapon": "Pistol", "health": 100, "attack": 12, "defense": 5},
            3: {"name": "Scientist", "weapon": "Experimental Rifle", "health": 80, "attack": 16, "defense": 3},
            4: {"name": "Security Guard", "weapon": "Assault Rifle", "health": 150, "attack": 10, "defense": 7}
        }

    def class_display(self):
        """Displays character classes to user"""

        print("Choose your character class:")
        for class_id, class_info in self.classes.items():
            print(f"{class_id}. {class_info['name']}")

    def class_choice(self):
        """Prompts user to choose class and returns corresponding class"""

        while True:
            try:
                choice = int(input("Enter the number of your chosen class: "))
                if choice in self.classes:
                    return self.classes[choice]
                else:
                    print("The company does not hire that profession. Please choose again.")
            except ValueError:
                print("Input not recognized. Please enter a number")
        
    def create_character(self):
        """Puts it all together and returns proper character"""

        self.class_display()
        chosen_class = self.class_choice()

        name = input("Enter your character's name: ")

        character = Character_Class(
            name=name,
            weapon=chosen_class["weapon"],
            health=chosen_class["health"],
            attack=chosen_class["attack"],
            defense=chosen_class["defense"],
        )

        print(f"You have chosen the {chosen_class['name']} class.")
        return character

if __name__ == "__main__":
    creator = Character_Creator()
    my_character = creator.create_character()
    print(my_character)