import streamlit as st

st.title('A* Search')
st.header('Taylor Hawks')

WIDTH = 8
HEIGHT = 8
TERRAIN_OPTIONS = ['⛰️']

columns = st.columns(WIDTH)

#grid selection
for x, col in enumerate(columns):
    with col:
        for y in range(HEIGHT):
            st.selectbox(
              label = f'({x},{y})', 
              options = TERRAIN_OPTIONS, 
              index=0, 
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
  
