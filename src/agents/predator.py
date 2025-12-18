from agents.base_agent import BaseAgent
from utils.constants import PREDATOR_HEALTH, PREDATOR_STAMINA, MOVE_COST,STAMINA_RESTORE,STARTING_HONOUR


class Predator(BaseAgent):
    
    def __init__(self, x, y, name="Dek", health=PREDATOR_HEALTH, stamina=PREDATOR_STAMINA):
        super().__init__(x, y, health)
        self.stamina = stamina
        self.name = name
        self.honour = STARTING_HONOUR
       
        
       
    
    def move(self, dx, dy):
        
        if self.stamina >= MOVE_COST:
            super().move(dx,dy)
            self.stamina = self.stamina - MOVE_COST
        else:
            print("No Stamina to Move")


    def rest(self):
        self.stamina = self.stamina + STAMINA_RESTORE
        if self.stamina > PREDATOR_STAMINA:  
            self.stamina = PREDATOR_STAMINA


    def attack(self):
        return (20)
    

    def gain_honour(self, amount):
        self.honour = self.honour + amount
        print(f"{self.name} Gained {amount} Honour! Total: {self.honour}")
              
            
        
      
            
            
            

    
    
  