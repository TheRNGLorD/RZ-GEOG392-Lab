# -*- coding: utf-8 -*-

import arcpy
import os

class Toolbox(object):
    def __init__(self):
        # Define the toolbox (the name of the toolbox is the name of the .pyt file).
        self.label = "Lab5_Toolbox"
        self.alias = "Lab5_Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Lab5_Tool]


class Lab5_Tool(object):
    def __init__(self):
        # Define the tool (tool name is the name of the class).
        self.label = "Lab5_Tool"
        self.description = "A tool for creating a geodatabase, buffering, and clipping features."
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Define parameter definitions
        param_GDB_folder = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdbfolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param_GDB_Name = arcpy.Parameter(
            displayName="GDB Name",
            name="gdbname",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Garage_CSV_File = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garage_csv",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param_Garage_Layer_Name = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="garage_layer_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Campus_GDB = arcpy.Parameter(
            displayName="Campus GDB",
            name="campus_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        param_Selected_Garage_Name = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="selected_garage_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Buffer_Radius = arcpy.Parameter(
            displayName="Buffer Radius (meters)",
            name="buffer_radius",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        
        params = [
            param_GDB_folder,
            param_GDB_Name,
            param_Garage_CSV_File,
            param_Garage_Layer_Name,
            param_Campus_GDB,
            param_Selected_Garage_Name,
            param_Buffer_Radius
        ]
        return params

    def isLicensed(self):
        # Set whether tool is licensed to execute.
        return True

    def updateParameters(self, parameters):
        # Modify the values and properties of parameters before internal validation.
        return

    def updateMessages(self, parameters):
        # Modify the messages created by internal validation for each tool parameter.
        return

    def execute(self, parameters, messages):
        # The source code of the tool.
        # Query user input
        GDB_Folder = parameters[0].valueAsText
        GDB_Name = parameters[1].valueAsText
        Garage_CSV_File = parameters[2].valueAsText
        Garage_Layer_Name = parameters[3].valueAsText
        Campus_GDB = parameters[4].valueAsText
        Selected_Garage_Name = parameters[5].valueAsText
        Buffer_Radius = parameters[6].value

        # Create geodatabase
        arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)
        GDB_Full_Path = os.path.join(GDB_Folder, f"{GDB_Name}.gdb")

        # Import garage CSV
        garages = arcpy.management.MakeXYEventLayer(
            Garage_CSV_File, "X", "Y", Garage_Layer_Name
        )
        arcpy.conversion.FeatureClassToGeodatabase(garages, GDB_Full_Path)

        # Search cursor to find selected garage
        structures = os.path.join(Campus_GDB, "Structures")
        where_clause = f"LotName = '{Selected_Garage_Name}'"
        with arcpy.da.SearchCursor(
            os.path.join(GDB_Full_Path, Garage_Layer_Name), ["LotName"]
        ) as cursor:
            shouldProceed = any(row[0] == Selected_Garage_Name for row in cursor)

        if shouldProceed:
            # Select garage as feature layer
            selected_garage_layer_name = "SelectedGarage"
            garage_feature = arcpy.analysis.Select(
                os.path.join(GDB_Full_Path, Garage_Layer_Name),
                os.path.join(GDB_Full_Path, selected_garage_layer_name),
                where_clause
            )

            # Buffer the selected building
            garage_buff_name = os.path.join(GDB_Full_Path, "building_buffed")
            arcpy.analysis.Buffer(garage_feature, garage_buff_name, Buffer_Radius)

            # Clip structures by buffer
            clipped_output = os.path.join(GDB_Full_Path, "clipped_structures")
            arcpy.analysis.Clip(structures, garage_buff_name, clipped_output)

            arcpy.AddMessage("Processing completed successfully.")
        else:
            arcpy.AddError(f"Could not find the garage name: {Selected_Garage_Name}")

        return
