class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(grid, start_pos, goal_pos, obstacles=None):
    if obstacles is None:
        obstacles = []
    
    start_node = Node(start_pos[0], start_pos[1])
    goal_node = Node(goal_pos[0], goal_pos[1])
    
    if start_node == goal_node:
        return [start_pos]
    
    open_list = []
    closed_list = []
    
    open_list.append(start_node)
    
    max_iterations = 1000
    iterations = 0
    
    while len(open_list) > 0 and iterations < max_iterations:
        iterations = iterations + 1
        
        current_node = open_list[0]
        current_index = 0
        
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index
        
        open_list.pop(current_index)
        closed_list.append(current_node)
        
        if current_node == goal_node:
            path = []
            current = current_node
            while current is not None:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for direction in directions:
            neighbor_x = current_node.x + direction[0]
            neighbor_y = current_node.y + direction[1]
            
            neighbor_x = neighbor_x % 20
            neighbor_y = neighbor_y % 20
            
            if (neighbor_x, neighbor_y) in obstacles:
                continue
            
            neighbor = Node(neighbor_x, neighbor_y, current_node)
            
            if neighbor in closed_list:
                continue
            
            neighbor.g = current_node.g + 1
            neighbor.h = manhattan_distance(neighbor_x, neighbor_y, goal_node.x, goal_node.y)
            neighbor.f = neighbor.g + neighbor.h
            
            skip = False
            for open_node in open_list:
                if neighbor == open_node and neighbor.g >= open_node.g:
                    skip = True
                    break
            
            if not skip:
                open_list.append(neighbor)
    
    return None