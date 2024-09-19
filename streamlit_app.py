import streamlit as st

st.title('A* Search')
st.header('Taylor Hawks')

WIDTH = 20
HEIGHT = 20

for x in range(WIDTH):
  st.selectbox(
    label = 'terrain', 
    options = ['⛰️'], 
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
