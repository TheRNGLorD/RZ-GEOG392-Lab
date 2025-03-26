import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

"""
You can change the `workspace` path as your wish.
"""
arcpy.env.workspace = BASE_DIR

"""
Here are some hints of what values the following variables should accept.
When running, the following code section will accept user input from terminal
Use `input()` method.

GDB_Folder = "***/Labs/Lab5"
GDB_Name = "Lab5.gdb"
Garage_CSV_File = "***/Labs/Lab5/garages.csv"
Garage_Layer_Name = "garages"
Campus_GDB = "***/Labs/Lab5/Campus.gdb"
Selected_Garage_Name = "Northside Parking Garage"
Buffer_Radius = "150 meter"
"""
### >>>>>> Add your code here
print("Please input the following parameters:\n")
GDB_Folder = input("GDB Folder: ")
GDB_Name = input("GDB Name: ")
Garage_CSV_File = input("Garage CSV File Path: ")
Garage_Layer_Name = input("Garage Layer Name: ")
Campus_GDB = input("Campus GDB Path: ")
Selected_Garage_Name = input("Selected Garage Name: ")
Buffer_Radius = input("Buffer Radius (example: 150): ")
### <<<<<< End of your code here

"""
In this section, you can re-use your codes from Lab4.

"""
### >>>>>> Add your code here
# Create geodatabase
arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)
GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)

# Import garage CSV to geodatabase
garages = arcpy.management.MakeXYEventLayer(
    Garage_CSV_File, "X", "Y", Garage_Layer_Name   
)
arcpy.conversion.FeatureClassToGeodatabase(
    [Garage_Layer_Name],  
    GDB_Full_Path         
)
### <<<<<< End of your code here

"""
Create a searchCursor.
Select the garage with `where` or `SQL` clause using `arcpy.analysis.Select` method.
Apply `Buffer` and `Clip` analysis on the selected feature.
Use `arcpy.analysis.Buffer()` and `arcpy.analysis.Clip()`.
"""
### >>>>>> Add your code here
#search surcor
structures = Campus_GDB + "/Structures"
where_clause = "LotName = '%s'" % Selected_Garage_Name
cursor = arcpy.da.SearchCursor(
    os.path.join(GDB_Full_Path, Garage_Layer_Name),  
    ["LotName"]                                      
)

shouldProceed = False

for row in cursor:
    if Selected_Garage_Name in row:
        shouldProceed = True
        break

if shouldProceed == True:
    #select garage as feature layer
    selected_garage_layer_name = "SelectedGarage"
    garage_feature = arcpy.analysis.Select(
        in_features = os.path.join(GDB_Full_Path, Garage_Layer_Name),
        out_feature_class = os.path.join(GDB_Full_Path, selected_garage_layer_name),
        where_clause = where_clause
    )

    # Buffer the selected building
    garage_buff_name = os.path.join(GDB_Full_Path, "building_buffed")
    arcpy.analysis.Buffer(
        in_features = garage_feature,
        out_feature_class = garage_buff_name,
        buffer_distance_or_field = Buffer_Radius
    )

    #clip
    arcpy.analysis.Clip(
        in_features = garage_buff_name,
        clip_features = structures,
        out_feature_class = os.path.join(GDB_Full_Path, "Clipped_Garage")
    )
    print("success")
else:
    print("error")
### <<<<<< End of your code here