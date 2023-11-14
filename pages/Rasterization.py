import streamlit as st
import folium 
import streamlit.components.v1 as components
import os 

option = st.selectbox(
   "Select year",
   ("2013","2015",'2021','2022'),
   index=None,
   placeholder="Select contry",
)
path = os.path.dirname(__file__)
file_path = path+'/'+str(option)+'.html'
if option != None:
  HtmlFile = open(file_path, 'r', encoding='utf-8')
  source_code = HtmlFile.read() 
  components.html(source_code,height = 600)



