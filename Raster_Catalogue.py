# Import relevant package  folio, geopandas etc
import os
import glob
import shapely
import folium
import geopandas as gpd
import pandas as pd
import rasterio as rio
import tqdm
# Import features directly - necessary as module often not resolved through import of rasterio
from rasterio import features

# Define a list of the GeoTIFF file paths and provide valid directory


def get_tif_paths() -> list[str]:
    # Enter infinite while loop until user provides valid directory containing >= 1 file with the .tif suffix
    while True:
        print('Enter valid directory in which to search for GeoTIFFs:')
        tif_directory = input()

        # Verify the input directory exists
        if not os.path.exists(tif_directory):
            print('Directory does not exist.')
            continue

# Use glob instead of os walk to recursively search directory (and subdirectories) for files with the .tif suffix
        tif_paths = glob.glob(f'{tif_directory}/**/*.tif', recursive=True)

        # Verify that 1 or more files with the .tif suffix have been found
        if len(tif_paths) == 0:
            print(f'No files with .tif suffix found in {tif_directory}')
            continue

        return tif_paths


def get_tif_footprint(tif_path: str) -> gpd.GeoSeries:
    with rio.open(tif_path) as img:
        # Set all valid data cells to the same value (1) for feature extraction
        tif_nodata = img.profile['nodata']
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
    # Build a GeoDataFrame from a concatenated GeoSeries of those in the list
    gdf = gpd.GeoDataFrame(geometry=pd.concat(gs_array))

    # Add column for file paths to GeoDataFrame
    gdf['file_path'] = tif_paths
    return gdf


def get_gdf_centroid(gdf: gpd.GeoDataFrame) -> list[int]:
    # Reproject the GeoDataFrame to EPSG:3857 to prevent GeoPandas centroid warning
    gdf = gdf.to_crs('EPSG:3857')

    # Obtain GeoDataFrame centroid and reproject to WGS 84 for folium
    gdf_centroid = gdf.dissolve().centroid.to_crs('EPSG:4326')
    return [gdf_centroid.iloc[0].y, gdf_centroid.iloc[0].x]


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


# Wrap processing functions in main() function for concise calling of entire workflow in other scripts
def main():
    tif_paths = get_tif_paths()
    gs_array = []

    # Use tqdm to show progress bar
    for path in tqdm.tqdm(tif_paths, desc='Retrieving GeoTIFF valid data footprints: '):
        gs_array.append(get_tif_footprint(path))

    # Create map output
    gdf = build_footprint_gdf(gs_array, tif_paths)
    map_centre = get_gdf_centroid(gdf)
    folium_map = build_folium_map(map_centre, gdf)

    # Save folium html map to script's working directory
    folium_map.save(r"GeoTIFF_footprints_map.html")


# Ensure main() is only run when current file is executed directly
if __name__ == '__main__':
    main()
