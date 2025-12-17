from utils.constants import GRID_WIDTH, GRID_HEIGHT, EMPTY


class Grid:
   
    
    def __init__(self):
        self.height = GRID_HEIGHT
        self.width = GRID_WIDTH
        self.grid = [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
        
    
    def wrap_position(self, x, y):
        wrapped_x = x % self.width
        wrapped_y = y % self.height
        return wrapped_x, wrapped_y
        
      
    
    def get_cell(self, x, y):
        wrapped_x, wrapped_y = self.wrap_position(x, y)
        return self.grid[wrapped_y][wrapped_x]
    
    def set_cell(self, x, y, value):
        wrapped_x, wrapped_y = self.wrap_position(x, y)
        self.grid[wrapped_y][wrapped_x] = value

    def is_empty(self, x, y):
        wrapped_x, wrapped_y = self.wrap_position(x, y)
        if self.grid[wrapped_y][wrapped_x] == EMPTY:
            return True
        else:
            return False
        
        
     