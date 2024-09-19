import streamlit as st
from typing import List, Tuple, Dict, Callable

st.title('A* Search')
st.header('Taylor Hawks')

WIDTH = 7
HEIGHT = 7

#global vars
COSTS  = { '🌾': 1, '🌲': 3, '⛰': 5, '🐊': 7}
MOVES = [(-1,0),(0,-1),(1,0),(0,1)]
TERRAIN_OPTIONS = list(COSTS.keys())

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

# search functions

if 'search_path' not in st.session_state:
    st.session_state['search_path'] = user_defined_map

def do_path():
    st.session_state.search_path = small_world


# form

with st.form("Map Parameters"):

    #start and finish
    start = st.text_input("Starting Position (comma separated)", "0,0").split(",")
    end = st.text_input("End Position (comma separated)", f"{WIDTH}, {HEIGHT}").split(",")
    
    #grid selection
    columns = st.columns(WIDTH)
    for x, col in enumerate(columns):
        with col:
            for y in range(HEIGHT):
                user_defined_map[x][y] = st.selectbox(
                  label = f'({x},{y})', 
                  options = TERRAIN_OPTIONS, 
                  index = TERRAIN_OPTIONS.index(small_world[x][y]), 
                  # format_func=special_internal_function, 
                  key=str(x)+str(y), 
                  # help=None, 
                  # on_change=None, 
                  # args=None, 
                  # kwargs=None, *, 
                  placeholder="Choose an option", 
                  disabled=False, 
                  label_visibility="visible"
                )
    
    #make the search happen
    submitted = st.form_submit_button('A* Search', on_click = do_path)
    
# st.write(st.session_state.search_path)
