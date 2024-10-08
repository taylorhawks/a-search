import streamlit as st
from typing import List, Tuple, Dict, Callable

st.title('A* Search')
st.header('Taylor Hawks')
st.write('Edit the map and search parameters, then see the changes in the map below.')


#global constants
WIDTH = 8
HEIGHT = 8
COSTS  = { '🌾': 1, '🌲': 3, '⛰': 5, '🐊': 7}
MOVES = [(-1,0),(0,-1),(1,0),(0,1)]
TERRAIN_OPTIONS = [ '🌾','🌲','⛰','🐊','🌋']
HEURISTIC_OPTIONS = ['Next Move', 'Manhattan Distance', 'Euclidean Distance']

#less than the full world used for the programming assignment
#wanted to do something where dropdowns would fit on the screen
full_world = [
    ['🌾', '🌾', '🌾', '🌾', '🌾', '🌲', '🌲', '🌲'],
    ['🐊', '🐊', '🌾', '🌾', '🌾', '🌾', '🌾', '🌲'],
    ['🐊', '🐊', '🌾', '🌾', '🌋', '🌋', '🌲', '🌲'],
    ['🌾', '🌾', '🌾', '🌾', '⛰', '🌋', '🌋', '🌋'],
    ['🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🌋', '🌲'],
    ['🌾', '⛰', '⛰', '⛰', '🌋', '⛰', '⛰', '⛰'],
    ['🌾', '⛰', '🌲', '🌋', '🌋', '⛰', '⛰', '🌾'],
    ['🌾', '🌾', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾'],
]

#global vars for a* search
user_defined_map = [[None for x in range(WIDTH)] for y in range(HEIGHT)]

#############
# FUNCTIONS #
#############

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

#heuristic function dictionary to allow access to all functions through dropdowns
heuristic_functions = {
    'Next Move' : heuristic_next,
    'Manhattan Distance' : heuristic_manhattan,
    'Euclidean Distance' : heuristic_euclidean,
}

#frontier function - take highest priority candidate - from project 1
def next_from_frontier(frontier: dict[int,List[Tuple[int,int]]]) -> Tuple[Tuple[int,int], dict[int,List[Tuple[int,int]]]]:
    frontier_key = min(frontier.keys())
    current_state_queue = frontier[frontier_key]
    current_state = current_state_queue[0]
    current_state_queue.pop(0)
    if len(current_state_queue) == 0:
        del frontier[frontier_key]
    return current_state, frontier

#update frontier - from project 1
def update_frontier(frontier: dict[int,List[Tuple[int,int]]], node: Tuple[int,int], cost: int) -> dict[int,List[Tuple[int,int]]]:
    if cost in frontier.keys():
        frontier[cost].append(node)
    else:
        frontier[cost] = [node]

#search function - from project 1
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

#map path - get the path and return the values to print as arrow emojis
def map_path(start: Tuple[int, int], path: List[Tuple[int, int]]) -> Dict[Tuple[int,int],str]:
    path_coordinates = [start]
    print_path = {}
    arrows = {(1,0): '⏬', (-1,0): '⏫', (0,1): '⏩', (0,-1): '⏪'}
    for move in path:
        path_coordinates.append((path_coordinates[-1][0] + move[0], path_coordinates[-1][1] + move[1]))
        print_path[path_coordinates[-2]] = arrows[move]
    print_path[path_coordinates[-1]] = '❓'
    return print_path

#pretty print path - this now returns the map to be rendered, along with the total cost, which was returned in the original function from project 1
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

# session state variables - the advantage of using these is that the rendered values update automatically,
# without having to call out to update global variables.
if 'map_lines' not in st.session_state:
    st.session_state['map_lines'] = user_defined_map

if 'path' not in st.session_state:
    st.session_state['path'] = []

if 'path_cost' not in st.session_state:
    st.session_state['path_cost'] = 0

#function to update path
#this function is called when the form is submitted
def do_path():
    st.session_state.path = a_star_search(user_defined_map, start_coords, end_coords, COSTS, MOVES, heuristic_func)
    st.session_state.map_lines, st.session_state.path_cost = pretty_print_path(user_defined_map, st.session_state.path, start_coords, end_coords, COSTS)

#function to show map at the bottom of the page
#uses html to center-align the text
#found this resource online: https://discuss.streamlit.io/t/justifying-or-centering-text-on-streamlit/11564
def render_map(map):
    for row in map:
        st.html('<div style="text-align: center">'+'  '.join(row)+'</div>')

########
# FORM #
########

#form to contain all the user-controlled parameters
#these variables don't need to be controlled by the session_state, as they're updated automatically upon form submission
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

    #grab the correct h(x) for A* Search
    heuristic_func = heuristic_functions[heuristic]
    
    #grid selection
    columns = st.columns(WIDTH)
    for x, col in enumerate(columns):
        with col:
            for y in range(HEIGHT):
                user_defined_map[y][x] = st.selectbox(
                  label = f'({x},{y})', 
                  options = TERRAIN_OPTIONS, 
                  index = TERRAIN_OPTIONS.index(full_world[y][x]), 
                  key = f'{x}_{y}',
                  on_change = None,
                  help=None, 
                  placeholder="Choose an option", 
                  disabled=False, 
                  label_visibility="visible"
                )
    
    #make the search happen
    submitted = st.form_submit_button(
        'A* Search',
        on_click = do_path
    )

# run this once - there are errors otherwise, such as needing to submit the form twice, if only showing a blank map at first.
do_path()

st.header('Rendered Map')
st.write('Submit the form to perform A* search for the given map and parameters.')
st.write(f'The found path is {st.session_state.path}.')
st.write(f'The path cost is {st.session_state.path_cost}.')
render_map(st.session_state.map_lines)
