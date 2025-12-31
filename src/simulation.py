import random
from grid import Grid
from agents.predator import Predator
from agents.boss import Adversary
from agents.Creature import Creature  
from agents.synthetic import Synthetic
from utils.constants import PREDATOR, ADVERSARY, EMPTY, CREATURE, TRAP, FATHER, BROTHER, SYNTHETIC, FATHER_HEALTH, FATHER_STAMINA, BROTHER_HEALTH, BROTHER_STAMINA, HONOUR_KILL_CREATURE, HONOUR_KILL_BOSS,WEAPON_UPGRADE,REPAIR_KIT
from algorithms.pathfinding import a_star

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
        self.father = Predator(father_pos[0], father_pos[1], name="Father", health=FATHER_HEALTH, stamina=FATHER_STAMINA, attack_damage=15)
        self.grid.set_cell(father_pos[0], father_pos[1], FATHER)

        brother_pos = self.get_random_empty_position()
        self.brother = Predator(brother_pos[0], brother_pos[1], name="Brother", health=BROTHER_HEALTH, stamina=BROTHER_STAMINA, attack_damage=15)
        self.grid.set_cell(brother_pos[0], brother_pos[1], BROTHER)

        thia_pos = self.get_random_empty_position()
        self.thia = Synthetic(thia_pos[0], thia_pos[1])
        self.grid.set_cell(thia_pos[0], thia_pos[1], SYNTHETIC)

        self.creatures = []
        for i in range(3):
            creature_pos = self.get_random_empty_position()
            creature = Creature(creature_pos[0], creature_pos[1])
            self.creatures.append(creature)
            self.grid.set_cell(creature_pos[0], creature_pos[1], CREATURE)

        self.traps = []
        for i in range(7):
            trap_pos = self.get_random_empty_position()
            self.traps.append(trap_pos)
            self.grid.set_cell(trap_pos[0], trap_pos[1], TRAP)

        self.weapon_upgrades = []
        for i in range(2):
            weapon_pos = self.get_random_empty_position()
            self.weapon_upgrades.append(weapon_pos)
            self.grid.set_cell(weapon_pos[0], weapon_pos[1], WEAPON_UPGRADE)
        
        
        self.repair_kits = []
        for i in range(2):
            repair_pos = self.get_random_empty_position()
            self.repair_kits.append(repair_pos)
            self.grid.set_cell(repair_pos[0], repair_pos[1], REPAIR_KIT)

        self.turncount = 0
        
    def get_random_empty_position(self):
        while True:
            random_x = random.randint(0, 19)
            random_y = random.randint(0, 19)
            if self.grid.get_cell(random_x, random_y) == EMPTY:
                return random_x, random_y

    def find_nearest_alive_creature(self):
        
        dek_x, dek_y = self.dek.get_position()
        nearest = None
        min_distance = 999
        
        for creature in self.creatures:
            if creature.is_alive():
                cx, cy = creature.get_position()
                distance = abs(dek_x - cx) + abs(dek_y - cy)
                if distance < min_distance:
                    min_distance = distance
                    nearest = creature
        
        return nearest
    
    def find_nearest_resource(self):
        
        dek_x, dek_y = self.dek.get_position()
        nearest = None
        min_distance = 999
        resource_type = None
        
      
        for weapon_pos in self.weapon_upgrades:
            distance = abs(dek_x - weapon_pos[0]) + abs(dek_y - weapon_pos[1])
            if distance < min_distance:
                min_distance = distance
                nearest = weapon_pos
                resource_type = "weapon"
        
       
        for repair_pos in self.repair_kits:
            distance = abs(dek_x - repair_pos[0]) + abs(dek_y - repair_pos[1])
            if distance < min_distance:
                min_distance = distance
                nearest = repair_pos
                resource_type = "repair"
        
        return nearest, resource_type, min_distance
    
    def collect_resource(self, resource_pos, resource_type):
        
        dek_x, dek_y = self.dek.get_position()
        
        path = a_star(self.grid, (dek_x, dek_y), resource_pos, obstacles=self.traps)
        
        if path and len(path) > 1:
            self.move_dek_along_path(path)
        else:
           
            dx = 1 if dek_x < resource_pos[0] else -1 if dek_x > resource_pos[0] else 0
            dy = 1 if dek_y < resource_pos[1] else -1 if dek_y > resource_pos[1] else 0
            if dx != 0 or dy != 0:
                self.move_dek(dx if dx != 0 else 0, dy if dy != 0 else 0)


    def move_dek(self, dx, dy):
        
        old_x, old_y = self.dek.get_position()
        self.dek.move(dx, dy)
        new_x, new_y = self.dek.get_position()
        
        self.grid.clear_cell(old_x, old_y)
        self.grid.set_cell(new_x, new_y, PREDATOR)

    def move_dek_along_path(self, path):
        
        dek_x, dek_y = self.dek.get_position()
        next_step = path[1]
        dx = next_step[0] - dek_x
        dy = next_step[1] - dek_y
        self.move_dek(dx, dy)

    def hunt_creature(self, creature):
        
        dek_x, dek_y = self.dek.get_position()
        cx, cy = creature.get_position()
        
        path = a_star(self.grid, (dek_x, dek_y), (cx, cy), obstacles=self.traps)
        
        if path and len(path) > 1:
            self.move_dek_along_path(path)

    def flee_from_boss(self):
        
        dek_x, dek_y = self.dek.get_position()
        boss_x, boss_y = self.adversary.get_position()
        
        dx = -1 if dek_x < boss_x else 1 if dek_x > boss_x else 0
        dy = -1 if dek_y < boss_y else 1 if dek_y > boss_y else 0
        
        if dx == 0 and dy == 0:
            dx = 1
        
        self.move_dek(dx if dx != 0 else 0, dy if dy != 0 else 0)

    def pursue_boss(self):
        
        dek_x, dek_y = self.dek.get_position()
        boss_x, boss_y = self.adversary.get_position()
        
        path = a_star(self.grid, (dek_x, dek_y), (boss_x, boss_y), obstacles=self.traps)
        
        if path and len(path) > 1:
            self.move_dek_along_path(path)

    def dek_rule_based_ai(self):
        
        
        dek_x, dek_y = self.dek.get_position()
        boss_x, boss_y = self.adversary.get_position()
        boss_distance = abs(dek_x - boss_x) + abs(dek_y - boss_y)
        
      
        if self.dek.stamina < 30:
            print("RULE 1: Low stamina → RESTING")
            self.dek.rest()
            return
        
       
        if self.dek.honour < 15:
            print("RULE 2: Low honour → HUNTING CREATURES")
            nearest = self.find_nearest_alive_creature()
            if nearest:
                self.hunt_creature(nearest)
            else:
                print("No creatures available, pursuing boss")
                self.pursue_boss()
            return
        
       
        if self.dek.health < 30 and boss_distance < 5:
            print("RULE 3: Low health + boss nearby → FLEEING")
            self.flee_from_boss()
            return
        
      
        if self.dek.health > 40 and boss_distance > 3:
            resource_pos, resource_type, distance = self.find_nearest_resource()
            if resource_pos and distance < 10:
                print(f"RULE 4: {resource_type} upgrade nearby → COLLECTING")
                self.collect_resource(resource_pos, resource_type)
                return
        
        
        print("RULE 5: Pursuing boss")
        self.pursue_boss()

    def run_turn(self):
        self.turncount = self.turncount + 1
       
      
        self.dek_rule_based_ai()
                
        if self.dek.carrying_thia == False:
            dek_x, dek_y = self.dek.get_position()
            thia_x, thia_y = self.thia.get_position()
            distance_to_thia = abs(dek_x - thia_x) + abs(dek_y - thia_y)
            
            if distance_to_thia <= 1:  
                self.dek.carrying_thia = True
                print("Dek picked up Thia")
                self.grid.clear_cell(thia_x, thia_y)
                
        if self.dek.carrying_thia:
            dek_x, dek_y = self.dek.get_position()
            self.thia.x = dek_x
            self.thia.y = dek_y

        for trap_pos in self.traps:
            if self.dek.get_position() == trap_pos:
                print("Dek Stepped on a trap")
                self.dek.stamina = self.dek.stamina - 15
                self.dek.lose_honour(5)
                print(f"Lost 15 stamina! Current stamina: {self.dek.stamina}")
                self.traps.remove(trap_pos)
                self.grid.clear_cell(trap_pos[0], trap_pos[1])
                break
         
        for weapon_pos in self.weapon_upgrades:
            if self.dek.get_position() == weapon_pos:
                print("Dek found a weapon upgrade!")
                self.dek.attack_damage = self.dek.attack_damage + 10
                print(f"Attack damage increased to {self.dek.attack_damage}!")
                self.weapon_upgrades.remove(weapon_pos)
                self.grid.clear_cell(weapon_pos[0], weapon_pos[1])
                break
        
        for repair_pos in self.repair_kits:
            if self.dek.get_position() == repair_pos:
                print("Dek found a repair kit!")
                if self.dek.carrying_thia:
                    print("Thia has been repaired!")
                    self.thia.is_repaired = True
                else:
                    print("Saved for when you pick up Thia!")
                    self.dek.has_repair_kit = True
                self.repair_kits.remove(repair_pos)
                self.grid.clear_cell(repair_pos[0], repair_pos[1])
                break
            
        if self.father.stamina >= 7:
            father_x, father_y = self.father.get_position()
            dek_x, dek_y = self.dek.get_position()
            father_distance = abs(dek_x - father_x) + abs(dek_y - father_y)
        
            if father_distance <= 1 and self.dek.honour < 20:
                print("Father: I Challenge You To Combat")
                father_damage = self.father.attack()
                self.dek.take_damage(father_damage)
                print(f"Father dealt {father_damage} damage! Dek health: {self.dek.health}")
                
                dek_damage = self.dek.attack()
                self.father.take_damage(dek_damage)
                print(f"Dek Dealt {dek_damage} Damage To Father!")
                self.dek.lose_honour(5)
        
            elif father_distance <= 5 and self.dek.honour < 20:
                print("Father pursues you for bringing shame!")
                
                dx = 0
                dy = 0
                if father_x < dek_x:
                    dx = 1 
                elif father_x > dek_x:
                    dx = -1     
                if father_y < dek_y:
                    dy = 1  
                elif father_y > dek_y:
                    dy = -1       
                if dx != 0:
                    move_dir = (dx, 0)
                else:
                    move_dir = (0, dy)
                
                old_father_pos = self.father.get_position()
                self.father.move(move_dir[0], move_dir[1])
                new_father_pos = self.father.get_position()
                
                self.grid.clear_cell(old_father_pos[0], old_father_pos[1])
                self.grid.set_cell(new_father_pos[0], new_father_pos[1], FATHER)
        
            else:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random_direction = random.choice(directions)
                
                old_father_pos = self.father.get_position()
                self.father.move(random_direction[0], random_direction[1])
                new_father_pos = self.father.get_position()
                
                self.grid.clear_cell(old_father_pos[0], old_father_pos[1])
                self.grid.set_cell(new_father_pos[0], new_father_pos[1], FATHER)
            
        if self.brother.stamina >= 7:
            brother_x, brother_y = self.brother.get_position()
            dek_x, dek_y = self.dek.get_position()
            brother_distance = abs(dek_x - brother_x) + abs(dek_y - brother_y)
            
            if brother_distance <= 1 and self.dek.honour < 20:
                print("Brother: I Challenge You To Combat!")
                brother_damage = self.brother.attack()
                self.dek.take_damage(brother_damage)
                print(f"Brother dealt {brother_damage} damage! Dek health: {self.dek.health}")
                
                dek_damage = self.dek.attack()
                self.brother.take_damage(dek_damage)
                print(f"Dek Dealt {dek_damage} Damage To Brother!")
                self.dek.lose_honour(5)
            
            elif brother_distance <= 5 and self.dek.honour < 20:
                print("Brother pursues you for bringing shame!")
                
                dx = 0
                dy = 0
                if brother_x < dek_x:
                    dx = 1 
                elif brother_x > dek_x:
                    dx = -1     
                if brother_y < dek_y:
                    dy = 1  
                elif brother_y > dek_y:
                    dy = -1       
                if dx != 0:
                    move_dir = (dx, 0)
                else:
                    move_dir = (0, dy)
                
                old_brother_pos = self.brother.get_position()
                self.brother.move(move_dir[0], move_dir[1])
                new_brother_pos = self.brother.get_position()
                
                self.grid.clear_cell(old_brother_pos[0], old_brother_pos[1])
                self.grid.set_cell(new_brother_pos[0], new_brother_pos[1], BROTHER)
            
            else:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random_direction = random.choice(directions)
                
                old_brother_pos = self.brother.get_position()
                self.brother.move(random_direction[0], random_direction[1])
                new_brother_pos = self.brother.get_position()
                
                self.grid.clear_cell(old_brother_pos[0], old_brother_pos[1])
                self.grid.set_cell(new_brother_pos[0], new_brother_pos[1], BROTHER)

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
            print("Father: You Have Brought Honour To Me")
        elif father_distance_to_dek <= 3 and self.dek.honour < 30:
            print("Father: You Have Shamed me")

        brother_distance_to_dek = abs(dek_x - brother_x) + abs(dek_y - brother_y)
        if brother_distance_to_dek <= 3 and self.dek.honour > 30:
            print("Brother: You Have Brought Honour To Me")
        elif brother_distance_to_dek <= 3 and self.dek.honour < 30:
            print("Brother: You Have Shamed me")

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

        boss_x, boss_y = self.adversary.get_position()
        dek_x, dek_y = self.dek.get_position()

        boss_path = a_star(self.grid, (boss_x, boss_y), (dek_x, dek_y), obstacles=[])

        if boss_path and len(boss_path) > 1:
            next_step = boss_path[1]
            dx = next_step[0] - boss_x
            dy = next_step[1] - boss_y
            
            old_boss_pos = self.adversary.get_position()
            self.adversary.x = self.adversary.x + dx
            self.adversary.y = self.adversary.y + dy
            new_boss_pos = self.adversary.get_position()
            
            self.grid.clear_cell(old_boss_pos[0], old_boss_pos[1])
            self.grid.set_cell(new_boss_pos[0], new_boss_pos[1], ADVERSARY)
            
            print(f"Boss hunts Dek! Distance: {len(boss_path)-1} cells")
        
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