import streamlit as st
from typing import List, Tuple, Dict, Callable

st.title('A* Search')
st.header('Taylor Hawks')



#global constants
WIDTH = 8
HEIGHT = 8
COSTS  = { '🌾': 1, '🌲': 3, '⛰': 5, '🐊': 7}
MOVES = [(-1,0),(0,-1),(1,0),(0,1)]
TERRAIN_OPTIONS = [ '🌾','🌲','⛰','🐊','🌋']
HEURISTIC_OPTIONS = ['Next Move', 'Manhattan Distance', 'Euclidean Distance']

#small world is the default map
small_world = [
    ['🌾', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'],
    ['🌾', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'],
    ['🌾', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲'],
    ['🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾'],
    ['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾'],
    ['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾'],
    ['🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾']
]

full_world = [
['🌾', '🌾', '🌾', '🌾', '🌾', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🌋', '🌋', '🌋', '🌋', '🌋', '🌋', '🌋', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌋', '🌋', '🌋', '⛰', '⛰', '⛰', '🌋', '🌋', '⛰', '⛰'],
['🌾', '🌾', '🌾', '🌾', '⛰', '🌋', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🐊', '🐊', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '⛰', '⛰', '🌋', '🌋', '⛰', '🌾'],
['🌾', '🌾', '🌾', '⛰', '⛰', '🌋', '🌋', '🌲', '🌲', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '⛰', '🌋', '🌋', '🌋', '⛰', '🌾'],
['🌾', '⛰', '⛰', '⛰', '🌋', '🌋', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🌋', '⛰', '🌾', '🌾'],
['🌾', '⛰', '⛰', '🌋', '🌋', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '⛰', '🌋', '🌋', '🌋', '🐊', '🐊', '🐊', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🌋', '🌋', '🌋', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾'],
['🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🌋', '🌋', '🌾', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '⛰', '🌋', '🌋', '🌋', '🌋', '🌾', '🌾', '🌾', '🐊', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '⛰', '⛰', '🌋', '🌋', '🌋', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🌋', '🌋', '🌋', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🌋', '🌋', '⛰', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🌾', '🌾', '⛰', '🌋', '🌋', '⛰', '🌾', '🌾', '🌾'],
['🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '🌋', '🌋', '⛰', '🌾', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '🌾', '⛰', '🌋', '⛰', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🌲', '🌲', '⛰', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🌋', '🌾', '🌾', '🌲', '🌲', '🌲', '🌲', '⛰', '⛰', '⛰', '⛰', '🌾', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🌋', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌋', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌋', '🌋', '🌋', '⛰', '⛰', '🌾', '🐊', '🌾', '⛰', '🌋', '🌋', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌋', '🌋', '🌋', '🌾', '🌾', '🌋', '🌋', '🌋', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌋', '🌋', '🌋', '🌋', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌋', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🌋', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊'],
['🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '🌋', '🌋', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌋', '🌾', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊'],
['🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🌋', '🌋', '🌋', '🌲', '🌲', '🌋', '🌋', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊'],
['🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🌋', '🌋', '🌋', '🌋', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊'],
['🌾', '⛰', '⛰', '🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🌋', '🌋', '⛰', '⛰', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊'],
['⛰', '🌋', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌋', '🌋', '🌋', '⛰', '⛰', '🌋', '🌋', '🌾', '🌋', '🌋', '⛰', '⛰', '🐊', '🐊', '🐊', '🐊'],
['⛰', '🌋', '🌋', '🌋', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🌋', '🌋', '🌋', '🌋', '⛰', '⛰', '⛰', '⛰', '🌋', '🌋', '🌋', '🐊', '🐊', '🐊', '🐊'],
['⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾']
]

#global vars for a* search
user_defined_map = [[None for x in range(WIDTH)] for y in range(HEIGHT)]
heuristic = None
heuristic_functions = dict()
path = False

#############
# FUNCTIONS #
#############

#function to show map
def render_map(map):
    for row in map:
        st.html('<div style="text-align: center">'+' '.join(row)+'</div>')

#valid position used for search. detects edges and volcanoes
def valid_position(loc: Tuple[int,int], world: List[List[str]]) -> bool:
    world_size = len(world)
    if loc[0] >= 0 and loc[1] >= 0 and loc[0] < world_size and loc[1] < world_size:
        return world[loc[0]][loc[1]] != '🌋'
    else:
        return False

#get valid next moves
def get_successors(loc: Tuple[int,int], world: List[List[str]], moves: List[Tuple[int, int]]) -> dict:
    successors = [(loc[0] + move[0], loc[1] + move[1]) for move in moves]
    return [i for i in successors if valid_position(i, world)]

#get cost of each move
def step_cost(loc: Tuple[int,int], world: List[List[str]], costs: Dict[str,int]) -> int:
    return costs[world[loc[0]][loc[1]]]



#heuristic function: Next move
def heuristic_next(loc: Tuple[int,int], world: List[List[str]], costs: Dict[str,int], goal: Tuple[int,int])->List[int]:
    return 0 if loc==goal else step_cost(loc,world,costs)
    
#heuristic function: Manhattan distance
def heuristic_manhattan(loc: Tuple[int,int], world: List[List[str]], costs: Dict[str,int], goal: Tuple[int,int])->List[int]:
    return abs(x-loc[0])+abs(y-loc[1])

#heuristic function: Euclidean distance
def heuristic_euclidean(loc: Tuple[int,int], world: List[List[str]], costs: Dict[str,int], goal: Tuple[int,int])->List[int]:
    return ((x-loc[0])**2+abs(y-loc[1])**2)**0.5

#frontier function - take highest priority candidate
def next_from_frontier(frontier: dict[int,List[Tuple[int,int]]]) -> Tuple[Tuple[int,int], dict[int,List[Tuple[int,int]]]]:
    frontier_key = min(frontier.keys())
    current_state_queue = frontier[frontier_key]
    current_state = current_state_queue[0]
    current_state_queue.pop(0)
    if len(current_state_queue) == 0:
        del frontier[frontier_key]
    return current_state, frontier

#update frontier
def update_frontier(frontier: dict[int,List[Tuple[int,int]]], node: Tuple[int,int], cost: int) -> dict[int,List[Tuple[int,int]]]:
    if cost in frontier.keys():
        frontier[cost].append(node)
    else:
        frontier[cost] = [node]

#search function
def a_star_search(world: List[List[str]], start: Tuple[int, int], goal: Tuple[int, int], costs: Dict[str, int], 
                  moves: List[Tuple[int, int]], heuristic: Callable) -> List[Tuple[int, int]]:
    paths = {start:{'cost':0,'path':[]}}
    frontier, explored = {0: [start]}, []
    while len(frontier) != 0:
        current_state, frontier = next_from_frontier(frontier)
        if current_state == goal:
            break
        children = [child for child in get_successors(current_state, world, moves) if child not in explored]
        for child in children:
            g_of_x = paths[current_state]['cost']
            f_of_x = g_of_x + heuristic(child, world, COSTS, goal)
            move = (child[0]-current_state[0],child[1]-current_state[1])
            if (child in paths.keys() and f_of_x < paths[child]['cost']):
                paths[child] = {'path':paths[current_state]['path'] + [move], 'cost':g_of_x + step_cost(child,world,costs)}
            if child not in paths.keys():
                paths[child] = {'path':paths[current_state]['path'] + [move], 'cost':g_of_x + step_cost(child,world,costs)}
                update_frontier(frontier, child, f_of_x)
        explored.append(current_state)
    return paths[current_state]['path']

def map_path(start: Tuple[int, int], path: List[Tuple[int, int]]) -> Dict[Tuple[int,int],str]:
    path_coordinates = [start]
    print_path = {}
    arrows = {(1,0): '⏬', (-1,0): '⏫', (0,1): '⏩', (0,-1): '⏪'}
    for move in path:
        path_coordinates.append((path_coordinates[-1][0] + move[0], path_coordinates[-1][1] + move[1]))
        print_path[path_coordinates[-2]] = arrows[move]
    print_path[path_coordinates[-1]] = '❓'
    return print_path

def pretty_print_path( world: List[List[str]], path: List[Tuple[int, int]], start: Tuple[int, int], goal: Tuple[int, int], costs: Dict[str, int]) -> int:
    map_lines = []
    print_path = map_path(start, path)
    for y,row in enumerate(world):
        line = []
        for x, terrain in enumerate(row):
            if (y,x) == goal:
                line.append('🎁')
            elif (y,x) in print_path.keys():
                line.append(print_path[(y,x)])
            else:
                line.append(terrain)
        map_lines.append(line) #changed from print
    return map_lines, sum([step_cost(loc,world,costs) for loc in print_path.keys() if loc != start])

# more global vars for search functionality
path = None
map_lines = None
path_cost = None
path_bool = False

heuristic_func = heuristic_next

#function to update path
def do_path():
    global path, map_lines, path_cost, path_bool
    path = a_star_search(user_defined_map, start_coords, end_coords, COSTS, MOVES, heuristic_func)
    map_lines, path_cost = pretty_print_path(user_defined_map, path, start_coords, end_coords, COSTS)
    path_bool = True
    

with st.form("Map Parameters"):

    #start and finish
    start = st.text_input("Starting Position (comma separated)", "0,0").split(",")

    start_x = int(start[0].strip())
    start_y = int(start[1].strip())

    start_coords = (start_x,start_y)
    
    end = st.text_input("End Position (comma separated)", f"{WIDTH-1}, {HEIGHT-1}").split(",")

    end_x = int(end[0].strip())
    end_y = int(end[1].strip())

    end_coords = (end_x,end_y)
    
    heuristic = st.selectbox(
        label = 'heuristic',
        options = HEURISTIC_OPTIONS,
        index = 0,
        key = 'heuristic',
        placeholder="Choose an option", 
        disabled=False, 
        label_visibility="visible"
    )
    
    #grid selection
    columns = st.columns(WIDTH)
    for x, col in enumerate(columns):
        with col:
            for y in range(HEIGHT):
                user_defined_map[y][x] = st.selectbox(
                  label = f'({x},{y})', 
                  options = TERRAIN_OPTIONS, 
                  index = TERRAIN_OPTIONS.index(full_world[y][x]), 
                  # format_func=special_internal_function, 
                  key = f'{x}_{y}',
                  on_change = None,
                  help=None, 
                  placeholder="Choose an option", 
                  disabled=False, 
                  label_visibility="visible"
                )
    
    #make the search happen
    submitted = st.form_submit_button('A* Search', on_click = do_path)

st.header('Rendered Map')

if !path_bool:
    render_map(user_defined_map)
else:
    render_map(map_lines)
