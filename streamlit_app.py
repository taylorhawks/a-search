import streamlit as st
from collections import OrderedDict

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

#grid selection
columns = st.columns(WIDTH)
for x, col in enumerate(columns):
    with col:
        for y in range(HEIGHT):
            st.selectbox(
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
st.button('A* Search')
  
