import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

### >>>>>> Add your code here
INPUT_DB_PATH = os.path.join(BASE_DIR, "Lab4_Data", "Campus.gdb")  
CSV_PATH = os.path.join(BASE_DIR, "Lab4_Data", "garages.csv")     
OUTPUT_DB_PATH = os.path.join(BASE_DIR, "Lab4_Data", "Output.gdb")  
### <<<<<< End of your code here

arcpy.env.workspace = INPUT_DB_PATH

# Kept Layers
layers_to_keep = ["GaragePoints", "LandUse", "Structures", "Trees"]

# List all feature classes 
feature_classes = arcpy.ListFeatureClasses()

# Delete any feature classes 
for fc in feature_classes:
    if fc not in layers_to_keep:
        arcpy.management.Delete(fc)

# GDB
if not os.path.exists(OUTPUT_DB_PATH):
    arcpy.management.CreateFileGDB(os.path.dirname(OUTPUT_DB_PATH), os.path.basename(OUTPUT_DB_PATH).replace('.gdb', ''))

# Load the CSV file 
arcpy.management.XYTableToPoint(
    CSV_PATH, 
    os.path.join(OUTPUT_DB_PATH, "GaragePoints"), "X", "Y" 
)

# Print spatial references before re-projection
print("Before Re-Projection...")
print(f"GaragePoints layer spatial reference: {arcpy.Describe(os.path.join(INPUT_DB_PATH, 'GaragePoints')).spatialReference.name}.")
print(f"Structures layer spatial reference: {arcpy.Describe(os.path.join(INPUT_DB_PATH, 'Structures')).spatialReference.name}.")

# Re-project GaragePoints and Structures layers to WGS 84 (EPSG 4326)
target_ref = arcpy.SpatialReference(4326)
arcpy.management.Project(
    os.path.join(INPUT_DB_PATH, "GaragePoints"),
    os.path.join(OUTPUT_DB_PATH, "GaragePoints_Projected"),
    target_ref
)
arcpy.management.Project(
    os.path.join(INPUT_DB_PATH, "Structures"),
    os.path.join(OUTPUT_DB_PATH, "Structures_Projected"),
    target_ref
)

# Print spatial references after re-projection
print("After Re-Projection...")
print(f"GaragePoints layer spatial reference: {arcpy.Describe(os.path.join(OUTPUT_DB_PATH, 'GaragePoints_Projected')).spatialReference.name}.")
print(f"re-projected Structures layer spatial reference: {arcpy.Describe(os.path.join(OUTPUT_DB_PATH, 'Structures_Projected')).spatialReference.name}.")

### >>>>>> Add your code here
# Buffer analysis
radiumStr = "150 Meters"
arcpy.analysis.Buffer(
    os.path.join(OUTPUT_DB_PATH, "GaragePoints_Projected"),  
    os.path.join(OUTPUT_DB_PATH, "GaragePoints_Buffered"),  
    radiumStr
)

# Intersect analysis 
arcpy.analysis.Intersect(
    [os.path.join(OUTPUT_DB_PATH, "GaragePoints_Buffered"), os.path.join(OUTPUT_DB_PATH, "Structures_Projected")],  
    os.path.join(OUTPUT_DB_PATH, "Intersected_Features")  
)
### <<<<<< End of your code here

