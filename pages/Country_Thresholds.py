
from matplotlib import pyplot as plt
import plotly.express as px

import pandas as pd
import streamlit as st
import os


path = os.path.dirname(__file__)
file_path = path+'/NGA.xlsx'

option = st.selectbox(
   "Select country",
   ("Ghana", "Cameroon", "Congo republic","Nigeria"),
   index=None,
   placeholder="Select contry",
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


sheet_name = 'Country tree cover loss'
subnational_sheet_name = 'Subnational 1 tree cover loss'
pie_chart_data = extract_bar_data(file_path, subnational_sheet_name)

if option == "Ghana":
    txt = st.write(
    "- *The government of Ghana lifted a ban on the export of unprocessed timber logs in 2002.* This led to a surge in logging, as timber companies rushed to clear forests and export the logs before the ban was reinstated. - *The government also reduced funding for forestry programs in 2002.* This made it more difficult for the Forestry Commission to enforce forest laws and protect forests from deforestation.- *In addition, the government granted concessions to mining companies in forested areas.* This led to the clearing of forests for mining operations.",
    )
if option == "Cameroon":
    txt = st.write("The increase in tree cover loss in 2002 when compared to 2001 and in the years 2010 and 2015 is likely due to a combination of factors, including:Increased demand for agricultural products: Cameroon is a major exporter of agricultural products, such as cocoa, palm oil, and rubber. As global demand for these products has increased, so has the need to clear forests for agricultural land.Illegal logging: Cameroon is also a major exporter of timber. However, a significant portion of this logging is illegal. Illegal logging operations often clear large areas of forest without any regard for sustainable forest management practices.Weak governance: Cameroon's forest laws are relatively strong, but they are not always effectively enforced. This creates an environment where illegal logging and other forms of forest degradation can thrive.The main reason for the decrease in tree cover loss after 2017 is likely a combination of factors, including:Increased government efforts to combat deforestation: The Cameroonian government has taken a number of steps in recent years to reduce deforestation, including increasing enforcement of forest laws and investing in sustainable forest management practices.Increased public awareness of the importance of forests: Cameroonian civil society organizations have also played an important role in raising public awareness of the importance of forests and the need to protect them.Decline in global demand for some agricultural products: Global demand for some agricultural products, such as cocoa and palm oil, has declined in recent years. This has reduced the pressure to clear forests for agricultural land.")
if option == "Congo republic":
    txt = st.write("The Republic of Congo presents a complex scenario where conservation efforts intersect with challenges such as corruption, selective logging practices, and the potential impact of climate change. While strides have been made in sustainable forest management, the delicate balance between economic development and environmental preservation remains a significant concern. Addressing corruption, improving transparency, and considering the long-term consequences of logging and agriculture are essential for the Republic of Congo to sustainably manage its rich rainforest resources.")
if option == "Nigeria":
    txt = st.write("Nigeria had seen a sudden increase of tree cover loss, in 2016-17 because of infrastructure projects being established and unrest due to attacks by private militant groups. A railway line has been established from Lagos to Kanos, which required clearing of forests. The Niger delta avengers had attacked the oil pipelines (Niger Delta), which caused a forest damaging oil spill.")
if option != None and option2 != None:
 selected_data = pie_chart_data.get(option2)
 df = pd.DataFrame(selected_data)
 fig = px.bar(df, x='year', y='tc_loss_ha', title=f'Tree Cover Loss Over Years (Key {option2})',color='tc_loss_ha')
 st.plotly_chart(fig, use_container_width=True)
