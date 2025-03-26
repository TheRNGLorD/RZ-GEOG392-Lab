import arcpy
import os

band_red = r"C:/Users/ryanz/RZ-GEOG392-Lab/Lab7/LT05_L2SP_026039_20110803_20200820_02_T1_SR_B3.TIF"
band_green = r"C:/Users/ryanz/RZ-GEOG392-Lab/Lab7/LT05_L2SP_026039_20110803_20200820_02_T1_SR_B2.TIF"  
band_blue = r"C:/Users/ryanz/RZ-GEOG392-Lab/Lab7/LT05_L2SP_026039_20110803_20200820_02_T1_SR_B1.TIF"

input_dir = os.path.dirname(band_red)

output_rgb_composite = os.path.join(input_dir, "RGB_Composite.tif")

# Combine bands into an RGB composite raster
arcpy.management.CompositeBands(
    [band_red, band_green, band_blue],  
    output_rgb_composite  
)

print(f"RGB Composite raster saved at: {output_rgb_composite}")
