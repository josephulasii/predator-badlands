from agents.base_agent import BaseAgent
from utils.constants import ADVERSARY_HEALTH


class Adversary(BaseAgent):
    
    def __init__(self, x, y, name="Ultimate Boss"):
        super().__init__(x, y, ADVERSARY_HEALTH)
        self.name = name
        
    
    def attack(self):
        return (50)
       
       