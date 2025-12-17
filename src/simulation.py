
from grid import Grid
from agents.predator import Predator
from agents.boss import Adversary
from agents.Creature import Creature  
from utils.constants import PREDATOR, ADVERSARY, EMPTY, CREATURE


class Simulation:
    
    def __init__(self):
        
        self.grid = Grid()
        self.dek = Predator(1, 1)
        self.adversary = Adversary(18,18)
        self.creatures = [
        Creature(5, 5),
        Creature(10, 10),
        Creature(15, 2)]
        self.grid.set_cell(1, 1, PREDATOR)
        self.grid.set_cell(18, 18, ADVERSARY)
        self.grid.set_cell(5, 5, CREATURE)
        self.grid.set_cell(10, 10, CREATURE)
        self.grid.set_cell(15, 2, CREATURE)  
        self.turncount = 0 
    
    def run_turn(self):
        self.turncount = self.turncount + 1
       
        old_x, old_y = self.dek.get_position()  
        self.dek.move(1, 0)
        new_x, new_y = self.dek.get_position()  
       
    
        self.grid.clear_cell(old_x, old_y)
        self.grid.set_cell(new_x, new_y, PREDATOR)

        
        for creature in self.creatures:
            if creature.is_alive() and self.dek.get_position() == creature.get_position():
                print("Attacking Creature")
                dek_damage = self.dek.attack()
                creature.take_damage(dek_damage)

                if creature.is_alive() == False:
                    print("Creature is Dead")
                    self.grid.clear_cell(*creature.get_position())
                    
           
        

        if self.dek.get_position() == self.adversary.get_position():
            dek_damage = self.dek.attack()
            self.adversary.take_damage(dek_damage)
            adversary_damage = self.adversary.attack()
            self.dek.take_damage(adversary_damage)
                
            
    
    
    def display(self):
        print(f"Turn Number: {self.turncount}") 
        print(f"Dek Stamina: {self.dek.stamina} Dek Position: {self.dek.get_position()}  Dek Health: {self.dek.health}")
        print(f"Boss Position: {self.adversary.get_position()}  Boss Health: {self.adversary.health}")
        self.grid.display()
        
   