class BaseAgent:
   
    
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health

    
        
    def move(self, dx, dy):

        self.x = self.x + dx
        self.y = self.y + dy
        
        
        

    def take_damage(self, amount):
        self.health = self.health - amount
        if self.health < 0:
            self.health = 0
             

        
    
    def is_alive(self):
       if self.health > 0:
           return True
       else:
           return False
    


    def get_position(self):
       return (self.x, self.y)