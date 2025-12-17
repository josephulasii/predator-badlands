from agents.base_agent import BaseAgent
from utils.constants import CREATURE_HEALTH


class Creature(BaseAgent):
    
    
    def __init__(self, x, y):
        super().__init__(x, y, CREATURE_HEALTH)
        self.name = "Creature"
    
    def attack(self):
        return 10  