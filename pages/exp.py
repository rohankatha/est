import pandas as pd
import os 
import streamlit as st
import plotly.graph_objects as go
path = os.path.dirname(__file__)

option = st.selectbox(
   "Select country",
   ("Ghana", "Congo republic", "Nigeria","Cameroon"),
   index=None,
   placeholder="Select contry",
)

option2 = st.selectbox(
   "Select Method",
   ("LSTM", "GRU", "RNN"),
   index=None,
   placeholder="Select method",
)

file_path = None
file_path2 = None
if option2 == "LSTM":
  file_path_2 =  path+'/LSTM.csv'
if option2 == "RNN":
  file_path_2 =  path+'/RNN.csv'
if option2 == "GRU":
  file_path_2 =  path+'/GRU.csv'



if option is not None and option2 is not None:
   file_path = path+'/tree_loss_projections.csv'
   df = pd.read_csv(file_path)
   if option == "Congo republic":
    option = 'Democratic Republic of the Congo'
   x = df[df.iloc[:,0].str.contains(option)]
   x = x.iloc[0, :23]
   list_x = []
   for i in range(len(x)):
    list_x.append(x[i])
   years = [str(2000 + i) for i in range(26)]

   df_2 = pd.read_csv(file_path_2)
   list_y = []
   if option == "Ghana":
    list_y = list(df_2.iloc[:,2])
  
   for i in list_y:
      list_x.append(i)
   
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

 
   