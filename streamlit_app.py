import streamlit as st

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

# https://discuss.streamlit.io/t/delete-remove-from-app-screen-streamlit-form-st-form-after-feeling/25041/3
placeholder = st.empty()

with placeholder.form("Map Parameters"):

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
    submitted = st.form_submit_button('A* Search')

    if submitted:
        placeholder.empty()
        st.write("Searched.")
  
