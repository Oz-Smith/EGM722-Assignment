This code serves the purpose of cataloguing and generating a map that displays the footprints of GeoTIFF files found within a specified directory. The footprints are represented by polygons, which outline the valid data of each GeoTIFF file. The resulting map is created using the Folium library and can be saved as an HTML file for further exploration and sharing. Additionally, each polygon on the map includes the corresponding file path of the GeoTIFF it represents, providing information about the source and location of the data.
A number of packages are required to be installed on the system that will be searched.  These packages are:
os
glob
shapely
folium
geopandas
padas
rasterio
tqdm

Running the code will generate an HTML file named "GeoTIFF_footprints_map.html" that contains a map. The map will display the footprints of all GeoTIFF files found in the specified directory. Each footprint will be represented by a polygon with a blue fill color and black border. Hovering over a footprint will display the file path as a tooltip.

If you encounter any issues while running the code, consider the following troubleshooting advice:
Invalid Directory: If an invalid directory  is provided, a message "Directory does not exist." may occur.  Make sure to enter a valid directory path that exists on the system.
No GeoTIFF Files Found: If no GeoTIFF files with the .tif suffix are found in the specified directory and its subdirectories, a message "No files with .tif suffix found in [directory]." will appear.  Double-check that the directory provided contains the GeoTIFF files needed to visualise.
Missing Dependencies: If import errors or missing module issues are encountered, ensure that all the required dependencies mentioned in the setup section have been installed. Use the pip install command to install any missing libraries.
Unsupported GeoTIFF Format: If an error related to unsupported GeoTIFF formats is encountered it may be due to compatibility issues with the rasterio library. Try converting the GeoTIFF files to a compatible format before running the script.
Memory Errors: Processing large GeoTIFF files or a large number of files may lead to memory errors. If you encounter memory-related issues, consider running the script on a machine with more memory or limit the number or size of the GeoTIFF files you process at once.
