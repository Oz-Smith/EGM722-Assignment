# import relevant package  folio, geopandas etc
import glob
import shapely
import folium
import geopandas as gpd
import pandas as pd
import rasterio as rio
import os
import tqdm
from rasterio import features  # Necessary as features often not resolved using an import of rasterio

# Define a list of the GeoTIFF file paths
def get_tif_paths(tif_directory: str) -> list[str]:
    # Use glob insted of os walk to search for all .tif suffix to retrieve paths for all .tif files in the passed directory
    return glob.glob(f'{tif_directory}/**/*.tif', recursive=True)

def get_tif_footprint(tif_path: str) -> gpd.GeoSeries:
    with rio.open(tif_path) as img:

        # Set all valid data cells to the same value (1) for feature extraction
        tif_nodata = img.profile ['nodata']
        tif_array = img.read(1)
        tif_array[tif_array != tif_nodata] = 1

        # Create a mask of invalid data cells to ignore in feature extraction
        tif_mask = img.dataset_mask()

        # Iterate over features (contiguous areas of the same value), of which there should be one
        for geom, val in features.shapes(
                tif_array, mask=tif_mask, transform=img.transform
        ):

            # Create Shapely Polygon of the feature
            geom = shapely.Polygon(geom['coordinates'][0])

            # Create GeoSeries of the feature and reproject to WGS 84
            footprint_gs = gpd.GeoSeries(
                data=geom,
                crs=img.crs
            ).to_crs(
                'EPSG:3857'
            )
        return footprint_gs

    # Debug add tiff paths to the map
def build_footprint_gdf(gs_array: list[gpd.GeoSeries], tif_paths: list[str]) -> gpd.GeoDataFrame:
    # Build a GeoDataFrame from a concatenated GeoSeries of those in the passed list
    gdf = gpd.GeoDataFrame(geometry=pd.concat(gs_array))

    # Add colum for file paths
    gdf['file_path'] = tif_paths
    return gdf
def get_gdf_centroid(gdf: gpd.GeoDataFrame) ->list[int]:

    gdf_centroid = gdf.dissolve() .centroid.to_crs('EPSG:4326')
    return [gdf_centroid.iloc[0].y, gdf.centroid.iloc[0].x]
def build_folium_map(map_centre: list[int], gdf: gpd.GeoDataFrame):
    # Create a folium map centred on the centroid of the GeoDataFrame
    folium_map = folium.Map(location=map_centre, zoom_start=13)

    # Add GeoDataFrame to the map as a layer with blue fill colour and black border
    folium.GeoJson(
        gdf,
        name='Footprints',
        style_function=lambda x: {
            'fillColor': 'blue',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.3
        },
        tooltip=folium.features.GeoJsonTooltip(fields=['file_path'])  # Add file path to the layer
    ).add_to(folium_map)

    # Add layer control to the map
    folium.LayerControl().add_to(folium_map)
    return folium_map

# Define where to look for tiff files
def main():
    tif_directory = r"C:\Users\Oz Smith\Downloads"
    tif_paths = get_tif_paths(tif_directory)
    gs_array = []

    # Build a progress bar as noting seems to happen until the program finishes
    for path in tqdm.tqdm(tif_paths, desc='Retrieving GeoTIFF valid data footprints: '):
        gs_array.append(get_tif_footprint(path))

    # Create map output
    gdf = build_footprint_gdf(gs_array, tif_paths)
    map_centre = get_gdf_centroid(gdf)
    folium_map = build_folium_map(map_centre, gdf)
    folium_map.save(r"GeoTIFF_footprints_map.html")

if __name__ == '__main__':
    main()
