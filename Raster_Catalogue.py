# import relevant package  folio, geopandas etc
import glob, shapely
import pandas as pdd
import geopandas as gpd
import rasterio as rio
from rasterio import features # necessary as features often not resolved using an import of rasterio
import folium

# define a list of the GeoTIFF file paths
def get_tif_paths(tif_directory: str) -> list[str]:
    # Use glob and the .tif suffix to retrieve paths for all .tif files in the passed directory
    return glob.glob(f'{tif_directory}/*.tif')

def get_tif_footprint(tif_path: str) -> gpd.GeoSeries:
    with rio.open(tif_path) as img:

        # Set all valid data cells to the same value (1) for feature extraction
        tif_nodata = img.profile ['nodata']
        tif_array = img.read(1)
        tif_array[tif_array != tif_nodata] = 1

        #create a mask of invalid data cells to ignore in feature extraction
        tif_mask = img.dataset_mask()

        # Iterate over features (contiguous areas of the same value), of which there should be one (in typical satellite imagery)
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
                'EPSG:4326'
            )

        return footprint_gs
def build_footprint_gdf(gs_array: list[gpd.GeoSeries]) -> gpd.GeoDataFrame:
     # Build a GeoDataFrame from a concatenated GeoSeries of those in the passed list
     return gpd.GeoDataFrame(geometry=pd.concat(gs_array))
def main():
     ''

if __name__ == '__main__':
     main()
     tif_directory = r'C:\Users\Oz Smith\Downloads\dimapV2_PHR1A_acq20230510_deld6b99b48\IMG_PHR1A_PMS_001'
     tif_paths = get_tif_paths(tif_directory)
     gs_array = []

     for path in tif_paths:
         gs_array.append(get_tif_footprint(path))

     gdf = build_footprint_gdf(gs_array)

     print(gdf.centroid)
