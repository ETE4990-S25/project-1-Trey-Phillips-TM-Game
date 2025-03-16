class Enemy:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
    
    def takes_damage(self, damage):
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        if self.health < 0:
            self.health = 0
        print(f"{self.name} is hit for {damage_taken} and has {self.health} health remaining.")
        
    def attacks_player(self, character):
        damage_dealt = max(0, self.attack - character.defense)
        character.health -= damage_dealt
        if character.health < 0:
            character.health = 0
        print(f"{self.name} swings for {damage_dealt} damage. You have {character.health} health left.")
    
    def lives(self):
        return self.health > 0
