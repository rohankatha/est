import requests
import pandas as pd
import geopandas as gpd
import folium

# Define your latitude and longitude coordinates
latitude = 48.858844
longitude = 2.294351

# Specify the Global Forest Watch API URL
api_url = "https://production-api.globalforestwatch.org/v2/umd_tree_cover_loss"

# Set up query parameters
params = {
    "lat": latitude,
    "lng": longitude,
    "period": "2000-2020",
    "threshold": 30,
}

# Send a GET request to the API
response = requests.get(api_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Convert the data to a DataFrame for analysis
    df = pd.DataFrame(data['data'])
    
    # Print the tree cover loss information
    print("Tree Cover Loss Information:")
    print(df)
    
    # Create a folium map to visualize the location
    m = folium.Map(location=[latitude, longitude], zoom_start=8)
    folium.Marker([latitude, longitude], tooltip='Location').add_to(m)
    
    # Display the map
    m.save('tree_cover_map.html')
    print("Map saved as 'tree_cover_map.html'")
else:
    print("Failed to retrieve data. Status code:", response.status_code)
