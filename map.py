# app.py

import streamlit as st
from streamlit_folium import st_folium
import folium
import os
from geopy.geocoders import Nominatim
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
geolocator = Nominatim(user_agent="geoapiExercises")
path = os.path.dirname(__file__)
def pie_chart(threshold,year,data_dict):
    data_extracted = data_dict[year]
    data_extracted = data_extracted[threshold]
    return data_extracted

def extract_country_data(file_path, sheet_name):
    data_dict = {}  # Dictionary to store the extracted data

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Assuming that the columns for tc_loss_ha_year follow the format "tc_loss_ha_<year>"
    year_columns = [col for col in df.columns if col.startswith('tc_loss_ha_')]

    if not year_columns:
        raise ValueError('No columns in the specified format found.')

    # Extract start year and end year
    start_year = int(year_columns[0].split('_')[3])
    end_year = int(year_columns[-1].split('_')[3])

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        subnational = row['subnational1']  # Assuming 'subnational' is the column name for the subnational value

        for year in range(start_year, end_year + 1):
            threshold = row['threshold']
            tc_loss_year = row[f'tc_loss_ha_{year}']

            # Initialize a new dictionary for the year if not present
            if year not in data_dict:
                data_dict[year] = {}

            # Store the subnational tc_loss for the corresponding threshold
            if threshold not in data_dict[year]:
                data_dict[year][threshold] = {}

            data_dict[year][threshold][subnational] = tc_loss_year

    return data_dict


def extract_bar_data(file_path, sheet_name):
    data_dict = {}  # List to store the extracted data

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Assuming that the columns for tc_loss_ha_year follow the format "tc_loss_ha_<year>"
    year_columns = [col for col in df.columns if col.startswith('tc_loss_ha_')]

    if not year_columns:
        raise ValueError('No columns in the specified format found.')

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        threshold = row["threshold"]  # Assuming 'threshold' is the column name for the threshold

        # Create a list of year and tc_loss value pairs
        loss_years = [{"year": int(year.split('_')[3]), "tc_loss_ha": row[year]} for year in year_columns]
        
        data_dict[threshold]=  loss_years

    return data_dict



# Initialize Flask


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

def extract_country_data(file_path, sheet_name):
    data_dict = {}  # Dictionary to store the extracted data

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Assuming that the columns for tc_loss_ha_year follow the format "tc_loss_ha_<year>"
    year_columns = [col for col in df.columns if col.startswith('tc_loss_ha_')]

    if not year_columns:
        raise ValueError('No columns in the specified format found.')

    # Extract start year and end year
    start_year = int(year_columns[0].split('_')[3])
    end_year = int(year_columns[-1].split('_')[3])

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        subnational = row['subnational1']  # Assuming 'subnational' is the column name for the subnational value

        for year in range(start_year, end_year + 1):
            threshold = row['threshold']
            tc_loss_year = row[f'tc_loss_ha_{year}']

            # Initialize a new dictionary for the year if not present
            if year not in data_dict:
                data_dict[year] = {}

            # Store the subnational tc_loss for the corresponding threshold
            if threshold not in data_dict[year]:
                data_dict[year][threshold] = {}

            data_dict[year][threshold][subnational] = tc_loss_year

    return data_dict
def home():
   return "welcome to flask form streamlit"

def main():
    st.title("WORLD WIDE FOREST COVER")
    st.sidebar.success("Traversal") 
    
    # Streamlit components
    st.write("Click on any location near afrique to find tree cover loss")

    # Folium Map
    m = folium.Map(location=[0,0], zoom_start=5)
    m.add_child(folium.LatLngPopup())
    map = st_folium(m, height=350, width=700)
    data = None
    if map.get("last_clicked"):
      data = map["last_clicked"]["lat"], map["last_clicked"]["lng"]
    if data is not None:
      data = list(data)
      data[0] = str(data[0])
      data[1] = str(data[1])
      location = geolocator.geocode(data[0]+","+data[1])# Writes to the app
      st.write(location)
      tree_cover(location) # Writes to terminal
    return m.get_root().render()
def tree_cover(location):
   x = str(location)
   subnational_sheet_name = 'Subnational 1 tree cover loss'
   x = x.split(',')
   file_path = None
   
   if(len(x)>1):
      option = "Ghana"
      option = str(x[-1])
      option2 = str(x[-2])
      print(option2)
      option = option.strip()  
      option2 = option2.strip()
      
      if option == "Ghana":
          file_path = path+'/pages/GHA.xlsx'
      if option == "Nigeria":
          file_path = path+'/pages/NGA.xlsx'
      if option == "République démocratique du Congo":
          file_path = path+'/pages/COD.xlsx'
      if option == 'Cameroun':
     
          file_path = path+'/pages/CMR.xlsx'
   if file_path != None:
      pie_chart_data = extract_country_data(file_path, subnational_sheet_name)
      y = pie_chart(0,2022,pie_chart_data)
      provinces = list(y.keys())
      population = list(y.values())
      custom_colors = ['blue', 'green', 'red', 'yellow', 'purple', 'orange']
      fig = px.pie(names=provinces, values=population, title='Tree loss cover')
      fig.update_traces(marker=dict(colors=custom_colors))
      st.plotly_chart(fig, use_container_width=True)
      if option2 != None:
        if option == "Ghana":
          file_path = path+'/pages/Ghana_subnational.csv'
        if option == "Nigeria":
          file_path = path+'/pages/Nigeria_subnational.csv'
        if option == "République démocratique du Congo":
            file_path = path+'/pages/Democratic Republic of the Congo_subnational.csv'
        if option == "Cameroun":
            file_path = path+'/pages/Cameroon_subnational.csv'
        print(file_path,option2)
        df = pd.read_csv(file_path)
        x = df[df.iloc[:,0].str.contains(option2)]
        x = x.iloc[0, :26]
        list_x = []
        for i in range(len(x)):
            list_x.append(x[i])
        years = [str(2000 + i) for i in range(len(list_x))]
        data = {'Year': years, 'Value': list_x}
        df = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Year'], y=df['Value']))
        fig.update_layout(
        title='Bar Chart of Values Over Years of '+ option2,
        xaxis=dict(title='Year'),
        yaxis=dict(title='Value'),)
        st.plotly_chart(fig, use_container_width=True)
   

if __name__ == '__main__':
    main()
