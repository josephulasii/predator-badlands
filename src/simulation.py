
from grid import Grid
from agents.predator import Predator
from agents.boss import Adversary
from utils.constants import PREDATOR, ADVERSARY, EMPTY


class Simulation:
    
    def __init__(self):
        
        self.grid = Grid()
        self.dek = Predator(1, 1)
        self.adversary = Adversary(18,18)
        self.grid.set_cell(1, 1 ,PREDATOR)
        self.grid.set_cell(18, 18, ADVERSARY)    
        self.turncount = 0 
    
    def run_turn(self):
        self.turncount = self.turncount + 1
       
        old_x, old_y = self.dek.get_position()  
        self.dek.move(1, 0)
        new_x, new_y = self.dek.get_position()  
       
    
        self.grid.clear_cell(old_x, old_y)
        self.grid.set_cell(new_x, new_y, PREDATOR)

        if self.dek.get_position() == self.adversary.get_position():
            dek_damage = self.dek.attack()
            self.adversary.take_damage(dek_damage)
            adversary_damage = self.adversary.attack()
            self.dek.take_damage(adversary_damage)
                
            
    
    
    def display(self):
        print(f"Turn Number: {self.turncount}") 
        print(f"Stamina: {self.dek.stamina} Position: {self.dek.get_position()}  Health: {self.dek.health}")
        print(f" Position: {self.adversary.get_position()}  Health: {self.adversary.health}")
        self.grid.display()
        
   