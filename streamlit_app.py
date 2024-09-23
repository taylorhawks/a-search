import streamlit as st
from typing import List, Tuple, Dict, Callable

st.title('A* Search')
st.header('Taylor Hawks')

WIDTH = 7
HEIGHT = 7

#global vars
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

user_defined_map = [[None for x in range(WIDTH)] for y in range(HEIGHT)]

def render_map():
    for row in user_defined_map:
        st.write(''.join(row))

def do_path():
    pass

with st.form("Map Parameters"):

    #start and finish
    start = st.text_input("Starting Position (comma separated)", "0,0").split(",")

    start_x = int(start[1].strip())
    start_y = int(start[0].strip())
    
    end = st.text_input("End Position (comma separated)", f"{WIDTH}, {HEIGHT}").split(",")

    end_x = int(end[1].strip())
    end_y = int(end[0].strip())
    
    # heuristic = st.selectbox(
    #     label = 'heuristic',
    #     option = HEURISTIC_OPTIONS,
    #     index = 1,
    #     key = 'heuristic',
    #     placeholder="Choose an option", 
    #     disabled=False, 
    #     label_visibility="visible"
    # )
    
    #grid selection
    columns = st.columns(WIDTH)
    for x, col in enumerate(columns):
        with col:
            for y in range(HEIGHT):
                user_defined_map[y][x] = st.selectbox(
                  label = f'({x},{y})', 
                  options = TERRAIN_OPTIONS, 
                  index = TERRAIN_OPTIONS.index(small_world[y][x]), 
                  # format_func=special_internal_function, 
                  key = f'{x}_{y}',
                  # help=None, 
                  on_change=render_map(), 
                  # args=None, 
                  # kwargs=None, *, 
                  placeholder="Choose an option", 
                  disabled=False, 
                  label_visibility="visible"
                )
    
    #make the search happen
    submitted = st.form_submit_button('A* Search', on_click = do_path)

render_map()
