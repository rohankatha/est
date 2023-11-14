
from matplotlib import pyplot as plt
import plotly.express as px
import pandas as pd
import streamlit as st
import os


option = st.selectbox(
   "Select country",
   ("Ghana", "Cameroon", "Congo republic","Nigeria"),
   index=None,
   placeholder="Select contry",
)
option1 = st.selectbox(
   "Select time",
   (2001, 2002, 2003,2004,2005,2006,2007,2008,2009,2010),
   index=None,
   placeholder="Select time.",
)
option2 = st.selectbox(
   "Select threshold",
   (0,25, 50, 75),
   index=None,
   placeholder="Select threshold",
)

path = os.path.dirname(__file__)
if option == "Ghana":
    file_path = path+'/GHA.xlsx'
if option == "Nigeria":
    file_path = path+'/NGA.xlsx'
if option == "Congo republic":
    file_path = path+'/COD.xlsx'
if option == "Cameroon":
    file_path = path+'/CMR.xlsx'



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


if option != None and option1 != None and option2 != None:
    sheet_name = 'Country tree cover loss'
    subnational_sheet_name = 'Subnational 1 tree cover loss'
    pie_chart_data = extract_country_data(file_path, subnational_sheet_name)
    y = pie_chart(option2,option1,pie_chart_data)
    provinces = list(y.keys())
    population = list(y.values())
    custom_colors = ['blue', 'green', 'red', 'yellow', 'purple', 'orange']

    fig = px.pie(names=provinces, values=population, title='Tree loss cover')
    fig.update_traces(marker=dict(colors=custom_colors))
    st.plotly_chart(fig, use_container_width=True)
   
