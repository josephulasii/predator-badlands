from agents.base_agent import BaseAgent
from utils.constants import THIA_HEALTH




class Synthetic(BaseAgent):
   
    def __init__(self, x, y, name="Thia"):
      super().__init__(x, y, THIA_HEALTH)
      self.name = name
      self.damaged = True

 
    def can_move(self):
      return False
    

    def intel(self, position):
       return f"Thia: I detect something at position {position}"
    

    def repair(self, amount):
       self.health = self.health + amount
       if self.health > THIA_HEALTH:
          self.health = THIA_HEALTH
          
       

      