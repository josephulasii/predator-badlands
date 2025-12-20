import random
from grid import Grid
from agents.predator import Predator
from agents.boss import Adversary
from agents.Creature import Creature  
from agents.synthetic import Synthetic
from utils.constants import PREDATOR, ADVERSARY, EMPTY, CREATURE,TRAP, FATHER, BROTHER, SYNTHETIC, FATHER_HEALTH, FATHER_STAMINA, BROTHER_HEALTH, BROTHER_STAMINA, HONOUR_KILL_CREATURE, HONOUR_KILL_BOSS
class Simulation:
    def __init__(self):
        self.grid = Grid()


        dek_pos = self.get_random_empty_position()
        self.dek = Predator(dek_pos[0], dek_pos[1])
        self.grid.set_cell(dek_pos[0], dek_pos[1], PREDATOR)


        adversary_pos = self.get_random_empty_position()
        self.adversary = Adversary(adversary_pos[0], adversary_pos[1])
        self.grid.set_cell(adversary_pos[0], adversary_pos[1], ADVERSARY)


        father_pos = self.get_random_empty_position()
        self.father = Predator(father_pos[0], father_pos[1], name="Father", health=FATHER_HEALTH,stamina=FATHER_STAMINA)
        self.grid.set_cell(father_pos[0], father_pos[1], FATHER)


        brother_pos = self.get_random_empty_position()
        self.brother = Predator(brother_pos[0], brother_pos[1], name="Brother", health=BROTHER_HEALTH, stamina=BROTHER_STAMINA)
        self.grid.set_cell(brother_pos[0], brother_pos[1], BROTHER)


        thia_pos = self.get_random_empty_position()
        self.thia = Synthetic(thia_pos[0], thia_pos[1])
        self.grid.set_cell(thia_pos[0], thia_pos[1], SYNTHETIC)


        self.creatures = []
        for i in range(3):
            creature_pos = self.get_random_empty_position()
            creature = Creature(creature_pos[0], creature_pos[1])
            self.creatures.append(creature)
            self.grid.set_cell(creature_pos[0], creature_pos[1], TRAP)

        self.traps = []
        for i in range(7):
            trap_pos = self.get_random_empty_position()
            self.traps.append(trap_pos)
            self.grid.set_cell(trap_pos[0], trap_pos[1], TRAP)

        self.turncount = 0
    def get_random_empty_position(self):

        while True:
            random_x = random.randint(0,19)
            random_y = random.randint(0, 19)
            if self.grid.get_cell(random_x, random_y) == EMPTY:
                return random_x, random_y











    def run_turn(self):
        self.turncount = self.turncount + 1
       
        old_x, old_y = self.dek.get_position()  
        self.dek.move(1, 0)
        new_x, new_y = self.dek.get_position()  
       
    
        self.grid.clear_cell(old_x, old_y)
        self.grid.set_cell(new_x, new_y, PREDATOR)


        for trap_pos in self.traps:
             if self.dek.get_position() == trap_pos:
                print(" Dek Stepped on a trap")
                self.dek.stamina = self.dek.stamina - 15
                self.dek.lose_honour(5)
                print(f"Lost 15 stamina! Current stamina: {self.dek.stamina}")
                self.traps.remove(trap_pos)
                self.grid.clear_cell(trap_pos[0], trap_pos[1])
                break


        
        for creature in self.creatures:
            if creature.is_alive() and self.dek.get_position() == creature.get_position():
                print("Attacking Creature")
                dek_damage = self.dek.attack()
                creature.take_damage(dek_damage)

                if creature.is_alive() == False:
                    self.dek.gain_honour(HONOUR_KILL_CREATURE)
                    print("Creature is Dead")
                    self.grid.clear_cell(*creature.get_position())


        brother_x, brother_y = self.brother.get_position()
        father_x, father_y = self.father.get_position()
        dek_x, dek_y = self.dek.get_position()

        father_distance_to_dek = abs(dek_x - father_x) + abs(dek_y - father_y)
        if father_distance_to_dek <= 3 and self.dek.honour > 30:
            print("Father: You  Have Brought Honour To Me")
        elif father_distance_to_dek <= 3 and self.dek.honour < 30:
            print("Father: You  Have Shamed me ")

        brother_distance_to_dek = abs(dek_x - brother_x) + abs(dek_y - brother_y)
        if brother_distance_to_dek <= 3 and self.dek.honour > 30:
            print("Brother: You  Have Brought Honour To Me")
        elif brother_distance_to_dek <= 3 and self.dek.honour < 30:
            print("Brother: You  Have Shamed me ")
      

       
        thia_x, thia_y = self.thia.get_position()
        dek_x, dek_y = self.dek.get_position()
        thia_distance = abs(dek_x - thia_x) + abs(dek_y - thia_y)

        if thia_distance <= 5:
            creature_count = 0
            for creature in self.creatures:
                if creature.is_alive():
                    creature_x, creature_y = creature.get_position()
                    creature_distance = abs(dek_x - creature_x) + abs(dek_y - creature_y)
                    
                    if creature_distance < 5:
                        creature_count = creature_count + 1           
            print(f"Thia: I detect {creature_count} creatures nearby")
            boss_x, boss_y = self.adversary.get_position()
            boss_distance = abs(dek_x - boss_x) + abs(dek_y - boss_y)
            print(f"Thia: The adversary is {boss_distance} cells away")
            if self.dek.stamina < 30:
                print("Thia: Warning - your stamina is critically low")
                


        if self.dek.get_position() == self.adversary.get_position():
            dek_damage = self.dek.attack()
            self.adversary.take_damage(dek_damage)
            adversary_damage = self.adversary.attack()
            self.dek.take_damage(adversary_damage)

            if self.adversary.is_alive() == False:
                self.dek.gain_honour(HONOUR_KILL_BOSS)
                print("Boss is Dead!")
                
            
    
    
    def display(self):
        print(f"Turn Number: {self.turncount}") 
        print(f"Dek Stamina: {self.dek.stamina} Dek Position: {self.dek.get_position()}  Dek Health: {self.dek.health}  Dek Honour: {self.dek.honour}")
        print(f"Boss Position: {self.adversary.get_position()}  Boss Health: {self.adversary.health}")
        self.grid.display()
        
   