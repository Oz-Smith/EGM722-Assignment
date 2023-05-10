# import relevant files such as folio, geopandas etc
import os
import geopandas as gpd
import folium
from rasterio.plot import show
from rasterio.mask import mask

# Create a list to store the GeoTIFF file paths
geotiff_paths = []

# Define the directory to scan - this will need to be changed by each user
directory = 'C:/Users/Oz Smith/Downloads'

# Iterate through all files in the directory
for file_name in os.listdir(directory):
    file_path = os.path.join(directory, file_name)

# Check if the file is a GeoTIFF

# Get the full file path

# Create an empty GeoDataFrame to store the metadata

# Create a list to store the GeoTIFF file paths

# Open the raster file

# Create a polygon from the bounding box

# Add the metadata to the GeoDataFrame

# Create a map centred on the first GeoTIFF file

# Add each GeoTIFF file to the map

# Create a GeoJSON representation of the footprint

# Add the footprint to the map as a GeoJSON overlay

# Add a marker at the centroid of the footprint
