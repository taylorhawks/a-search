import streamlit as st

st.title('A* Search')
st.header('Taylor Hawks')

st.selectbox(
  label = 'terrain', 
  options = ['⛰️'], 
  index=0, 
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
