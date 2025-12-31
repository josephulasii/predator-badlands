from agents.base_agent import BaseAgent
from utils.constants import PREDATOR_HEALTH, PREDATOR_STAMINA, MOVE_COST,STAMINA_RESTORE,STARTING_HONOUR


class Predator(BaseAgent):
    
    def __init__(self, x, y, name="Dek", health=105, stamina=110, attack_damage=25):
        self.x = x
        self.y = y
        self.name = name
        self.health = health
        self.stamina = stamina
        self.honour = 0
        self.carrying_thia = False
        self.attack_damage = attack_damage 
        self.has_repair_kit = False
       
        
       
    
    def move(self, dx, dy):
      
        if self.carrying_thia:
            move_cost = MOVE_COST + 5
        else:
            move_cost = MOVE_COST
            
        if self.stamina >= move_cost:
            super().move(dx, dy)
            self.stamina = self.stamina - move_cost
        else:
            print("No Stamina to Move")
            if self.honour > 0:
                self.honour = self.honour - 3
                print(f"Lost 3 honour for exhaustion! Current honour: {self.honour}")

    def rest(self):
        self.stamina = self.stamina + STAMINA_RESTORE
        if self.stamina > PREDATOR_STAMINA:  
            self.stamina = PREDATOR_STAMINA


    def attack(self):
        return self.attack_damage 
    

    def gain_honour(self, amount):
        self.honour = self.honour + amount
        print(f"{self.name} Gained {amount} Honour! Total: {self.honour}")
        
        
    def lose_honour(self, amount):
        self.honour = self.honour - amount
        if self.honour < 0:  
            self.honour = 0
        print(f"{self.name} Lost {amount} Honour! Total: {self.honour}")
              
            
        
      
            
            
            

    
    
  