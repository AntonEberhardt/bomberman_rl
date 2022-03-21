import time

def setup(self):
    pass
    
def act(self, game_state):
    path = find_path(self, game_state, [1,1], [15,15])
    
    coord = game_state['self'][3]
    self.logger.info(f'danger of current tile {danger_of_tile(game_state, coord)}')   
    
    return 'BOMB'


def danger_of_tile(game_state, coord):
    danger = 0
    
    for xy, t in game_state['bombs']:
        # Check if the bomb in on the same collum or row of the agent 
        if not set(xy).intersection(coord): continue
        
        # Check how close the bomb is close enough
        if manhattan_dist(coord, xy) > 3: continue
        
        danger_ = t
        if danger_ > danger: danger = danger_
            
    return danger

def manhattan_dist(origin, goal):
    '''manhattan_dist(origin: list, goal: list)
    Calculate the distance between two points in the game environment,
    according to the manhattan metric.
    
    Inputs:
    original: The coordinates of the starting point
    goal: The coordinates of the end point
    
    Output:
    int , the manhattan distance between the points
    '''
    
    return abs(origin[0] - goal[0]) + abs(origin[1] - goal[1])


def find_path(self, game_state, origin, goal):
    '''fing_path(self: agent, game_state: dict, origin: list, goal: list)
    Attempts to find the path between the origin and goal points according to the A* algorithm. 
    
    Inputs:
    self: the agent for logging
    game_state: the game state in which to search a path
    original: the coordinates of the starting point
    goal: the coordinates of the starting points
    
    Output:
    None , if there is no path
    list , a list of coordinates that lead from the origin to the goal
    '''
    
    start_time = time.time_ns()
    
    #self.logger.info(f'Attempt to find the path from ({origin}) to ({goal})')
    
    # Define a Tile class to contain the path, costs and current final tile of the explored paths
    class Tile:
        def __init__(self, coord: list):
            self.coord = coord
            self.parent = None
            
            self.h = 0
            self.g = 0
            self.f = 0
    
    # Initialize A*
    origin_tile = Tile(origin)
    goal_tile = Tile(goal)
    
    open_list = [origin_tile,]
    closed_list = []
    
    # Explore paths until the goal tile is reached or no more paths are available
    while open_list:
        # find tile with lowest total cost
        open_list.sort(key = lambda tile: tile.f)
        
        # move the current tile to the closed list
        current_tile = open_list.pop(0)
        closed_list.append(current_tile)
        
        # Check termination criterion
        if current_tile.coord == goal_tile.coord:
            path = []
            last = current_tile
            while last.parent != None:
                path.append(last.coord)
                last = last.parent
            #self.logger.info(f'   found the path {path[::-1]}')
            #self.logger.info(f'   total time: {(time.time_ns() - start_time) * 1e-3 :.0f} millisec')
            return path[::-1]
        
        # Generate the children of the current tile
        children = []
        
        # Generate valid moves
        for move in zip([1,0,-1,0],[0,1,0,-1]):
            coord = [current_tile.coord[i] + move[i] for i in [0,1]]
            
            # Check if this is a valid move
            ## Not a wall or crate
            if not game_state['field'][tuple(coord)] == 0:
                continue
            
            ## Not a player
            if coord in [xy for (n, s, b, xy) in game_state['others']]:
                continue
            
            ## Not a bomb
            if coord in [xy for (xy, t) in game_state['bombs']]:
                continue
            
            child = Tile(coord = coord)
            child.parent = current_tile
        
            children.append(child)
        
        # Check the children against the closed_list and other instances of it in the open_list
        for child in children:
            # Filter for tiles that were already discarde
            if child.coord in [closed_tile.coord for closed_tile in closed_list]:
                continue
            
            # Calculate the costs
            child.g = current_tile.g + 1
            child.h = manhattan_dist(child.coord, goal_tile.coord)
            child.f = child.g + child.h
            
            # Check if tile was reached ealier with lower cost
            for open_tile in open_list:
                if child.coord == open_tile.coord and child.g > open_tile.g:
                    continue
            
            open_list.append(child)
    
    #self.logger.info(f'   there is no path')
    #self.logger.info(f'   total time: {(time.time_ns() - start_time) * 1e-3 :.0f} millisec')
    return None