import arcpy
from arcpy.sa import Raster
import os

BASE_DIR = r"C:/Users/ryanz/RZ-GEOG392-Lab/Lab7" 

band_RED = Raster(f"{BASE_DIR}/LT05_L2SP_026039_20110803_20200820_02_T1_SR_B3.TIF") 
band_NIR = Raster(f"{BASE_DIR}/LT05_L2SP_026039_20110803_20200820_02_T1_SR_B4.TIF") 

band_NDVI = ((band_NIR - band_RED) / (band_NIR + band_RED)) * 100 + 100

ndvi_output = os.path.join(BASE_DIR, "NDVI.tif")

# Save the NDVI raster
band_NDVI.save(ndvi_output)

print(f"NDVI raster saved at: {ndvi_output}")
