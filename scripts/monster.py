import random

class monster:
    name = None
    spritePath = None
    health = 100
    lowest_Attack = 1
    highest_Attack = 10

    def __init__(self, name, sprite) -> None:
        self.name = name
        self.spritePath = sprite
        
    def LaunchAttack(self):
        pass
    
    def Dead(self):
        pass