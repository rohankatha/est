import numpy as np
import pandas as pd
import plotly.express as px    
import json
import os 
import streamlit as st
path = os.path.dirname(__file__)

option = st.selectbox(
   "Select country",
   ("Ghana", "Congo republic", "Nigeria","Cameroon"),
   index=None,
   placeholder="Select contry",
)


with open(path+'/gadm41_GHA_1.json', 'r') as myfile:
		data=myfile.read()
   
df2 = None
data = None
if option == "Ghana":
     df2 = pd.read_csv(path+'/Ghana_subnational.csv')
     with open(path+'/gadm41_GHA_1.json', 'r') as myfile:
          data=myfile.read()
if option == "Nigeria":
     df2 = pd.read_csv(path+'/Nigeria_subnational.csv')
     with open(path+'/gadm41_NGA_1.json', 'r') as myfile:
          data=myfile.read()
if option == "Cameroon":
     df2 = pd.read_csv(path+'/Cameroon_subnational.csv')
     with open(path+'/gadm41_CMR_1.json', 'r') as myfile:
          data=myfile.read()
if option == "Congo republic":
     df2 = pd.read_csv(path+'/Democratic Republic of the Congo_subnational.csv')
     with open(path+'/gadm41_COD_1.json', 'r') as myfile:
          data=myfile.read()



               
##### Create the Choropleth map with Plotly
if option is not None:
     gj = json.loads(data)
     names = []
     for k in gj['features']:
      names += [k['properties']['NAME_1']] #use this key to access region names
     unique_names = names
     ans = []
     for i in unique_names:
          result = df2[df2.iloc[:,0].str.contains(i, case=False, regex=True)]
          k = list(result.iloc[:,22])
          if len(k)>=1:
               ans.append(k[0])
          else:
               ans.append(0)
     df = pd.DataFrame(list(zip(unique_names, ans)), 
               columns =['Name', 'Value']) 
               
     fig = px.choropleth_mapbox(df, geojson=gj, color="Value",
                           locations="Name", 
                           featureidkey="properties.NAME_1",
                           hover_data= ['Value'],                       
                           mapbox_style="carto-positron", 
                           zoom=2.6,
                           opacity = 0.7,)
                           
     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
     st.plotly_chart(fig, use_container_width=True)