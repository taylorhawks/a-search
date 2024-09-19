import streamlit as st

st.title('A* Search')
st.header('Taylor Hawks')

WIDTH = 10
HEIGHT = 10
TERRAIN_OPTIONS = ['⛰️']

columns = st.columns(WIDTH)

for col in columns:
  with col1:
      st.selectbox(
        label = 'terrain', 
        options = TERRAIN_OPTIONS, 
        index=x, 
        # format_func=special_internal_function, 
        # key=None, 
        # help=None, 
        # on_change=None, 
        # args=None, 
        # kwargs=None, *, 
        placeholder="Choose an option", 
        disabled=False, 
        label_visibility="visible"
      )
  
