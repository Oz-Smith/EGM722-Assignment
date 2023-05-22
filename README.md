This code serves the purpose of cataloguing and generating a map that displays the footprints of GeoTIFF files found within a specified directory. The footprints are represented by polygons, which outline the valid data of each GeoTIFF file. The resulting map is created using the Folium library and can be saved as an HTML file for further exploration and sharing. Additionally, each polygon on the map includes the corresponding file path of the GeoTIFF it represents, providing information about the source and location of the data.
A number of packages are required to be installed on the system that will be searched.  These packages are:
glob
shapely
folium
geopandas
padas
rasterio
tqdm

Running the code will generate an HTML file named "GeoTIFF_footprints_map.html" that contains a map. The map will display the footprints of all GeoTIFF files found in the specified directory. Each footprint will be represented by a polygon with a blue fill color and black border. Hovering over a footprint will display the file path as a tooltip.

If you encounter any issues while running the code, consider the following troubleshooting advice:
Dependency Errors: Ensure that all the required packages (folium, geopandas, pandas, rasterio, tqdm) are installed. You can use the pip install command mentioned in the installation section to install missing packages.
Invalid Directory Path: Double-check the directory path specified in the main function's tif_directory variable. Make sure it points to the correct directory where your GeoTIFF files are located. Adjust the path if necessary.
Missing GeoTIFF Files: If no GeoTIFF files are found in the specified directory, the map will not display any footprints. Verify that there are GeoTIFF files in the directory and that they have the ".tif" file extension.
Invalid GeoTIFF Files: If the code encounters any issues while reading the GeoTIFF files (e.g., corrupt files), it may raise an exception or produce unexpected results. Check the integrity of your GeoTIFF files or try running the code with a different set of GeoTIFF files.
