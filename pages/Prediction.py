import pandas as pd
import plotly.graph_objects as go
import os 
import streamlit as st

path = os.path.dirname(__file__)

option = st.selectbox(
   "Select country",
   ("Ghana", "Congo republic", "Nigeria","Cameroon"),
   index=None,
   placeholder="Select contry",
)

file_path = None
if option == "Ghana":
    file_path = path+'/Ghana_subnational.csv'
if option == "Nigeria":
    file_path = path+'/Nigeria_subnational.csv'
if option == "Congo republic":
    file_path = path+'/Democratic Republic of the Congo_subnational.csv'
if option == "Cameroon":
    file_path = path+'/Cameroon_subnational.csv'

value = st.text_input('Select sub region', '')

if value == '' and  file_path is not None:
   
   file_path = path+'/tree_loss_projections.csv'
   df = pd.read_csv(file_path)
   if option == "Congo republic":
    option = 'Democratic Republic of the Congo'
   x = df[df.iloc[:,0].str.contains(option)]
   x = x.iloc[0, :26]
   list_x = []
   for i in range(len(x)):
    list_x.append(x[i])
   years = [str(2000 + i) for i in range(len(list_x))]
   data = {'Year': years, 'Value': list_x}
   df = pd.DataFrame(data)
   fig = go.Figure()
   fig.add_trace(go.Bar(x=df['Year'][:-3], y=df['Value'][:-3], name='Other Years', marker=dict(color='blue')))
   fig.add_trace(go.Bar(x=df['Year'][-3:], y=df['Value'][-3:], name='PREDICTED_YEARS', marker=dict(color='red')))
   fig.update_layout(
    title='Bar Chart of Values Over Years',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Value'),)
   st.plotly_chart(fig, use_container_width=True)
   
if file_path is not None and value != "":
 df = pd.read_csv(file_path)
 x = df[df.iloc[:,0].str.contains(value)]
 x = x.iloc[0, :26]
 list_x = []
 for i in range(len(x)):
    list_x.append(x[i])
 years = [str(2000 + i) for i in range(len(list_x))]
 data = {'Year': years, 'Value': list_x}
 df = pd.DataFrame(data)
 fig = go.Figure()
 fig.add_trace(go.Bar(x=df['Year'][:-3], y=df['Value'][:-3], name='Other Years', marker=dict(color='blue')))
 fig.add_trace(go.Bar(x=df['Year'][-3:], y=df['Value'][-3:], name='PREDICTED_YEARS', marker=dict(color='red')))
 fig.update_layout(
    title='Bar Chart of Values Over Years',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Value'),)
 st.plotly_chart(fig, use_container_width=True)

 

