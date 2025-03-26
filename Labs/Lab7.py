import arcpy
import os

input_dem = r"C:/Users/ryanz/RZ-GEOG392-Lab/Lab7/n30_w097_1arc_v3.tif"  
output_dir = r"C:/Users/ryanz/RZ-GEOG392-Lab/Lab7"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

hillshade_output = os.path.join(output_dir, "output_HillShade.tif")
slope_output = os.path.join(output_dir, "output_Slope.tif")

# Generate HillShade raster
arcpy.ddd.HillShade(
    input_dem,         # Input raster
    hillshade_output,  # Output raster
    315,               # Azimuth
    45,                # Altitude
    "NO_SHADOWS",      # Shadows
    1                  # Z factor
)

# Generate Slope raster
arcpy.ddd.Slope(
    input_dem,         # Input raster
    slope_output,      # Output raster
    "DEGREE",          # Measurement
    1                  # Z factor
)

print(f"HillShade raster saved at: {hillshade_output}")
print(f"Slope raster saved at: {slope_output}")
