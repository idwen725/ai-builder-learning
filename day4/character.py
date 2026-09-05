class character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack
    def show_status(self):
        print(f"{self.name} HP:{self.hp} ATTACK:{self.attack}")
    def take_damage(self, damage):
        self.hp -= damage
    def heal(self, heal):
        self.hp += heal
player = character("Knight", 100, 20)

player.show_status()

player.take_damage(30)
player.show_status()

player.heal(10)
player.show_status()