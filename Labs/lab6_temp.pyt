# -*- coding: utf-8 -*-

import arcpy
import os
import time

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Lab6_Toolbox"
        self.alias = "Lab6_Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Lab6_Tool_Structures, Lab6_Tool_Trees]


class Lab6_Tool_Structures(object):
    def __init__(self):
        """Define the tool for Task 1."""
        self.label = "Lab6_Tool_Structures"
        self.description = "Tool to update renderer for the Structures layer"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param_proj_path = arcpy.Parameter(
            displayName="Project File Path",
            name="project_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param_layer_name = arcpy.Parameter(
            displayName="Layer Name",
            name="layer_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_output_path = arcpy.Parameter(
            displayName="Output Project File Path",
            name="output_project_path",
            datatype="DEFile",
            parameterType="Optional",
            direction="Output"
        )

        params = [param_proj_path, param_layer_name, param_output_path]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Setup the progressor
        readTime = 3
        start = 0
        max = 100
        step = 50  # Progress for each layer
        arcpy.SetProgressor("step", "Starting rendering process...", start, max, step)

        # Add message to the results pane
        arcpy.AddMessage("Initializing the tool...")

        # Accept user input from toolbox interface
        aprxFilePath = parameters[0].valueAsText
        layerName = parameters[1].valueAsText
        outputPath = parameters[2].valueAsText if parameters[2].valueAsText else aprxFilePath.replace(".aprx", "_updated.aprx")

        # Fetch the project
        project = arcpy.mp.ArcGISProject(aprxFilePath)
        layers = project.listMaps('Map')[0].listLayers()

        # Loop through the layers
        for layer in layers:
            if layer.isFeatureLayer:
                symbology = layer.symbology
                # Advance the progressor here
                arcpy.SetProgressorPosition(start + step)
                arcpy.SetProgressorLabel(f"Processing layer: {layer.name}")
                arcpy.AddMessage(f"Processing layer: {layer.name}")
                time.sleep(readTime)

                if hasattr(symbology, 'renderer') and layer.name == 'Structures':
                    # Re-render the 'Structures' layer into 'UniqueValueRenderer'
                    symbology.updateRenderer('UniqueValueRenderer')
                    symbology.renderer.fields = ["Type"]
                    layer.symbology = symbology
                    arcpy.AddMessage("Updated 'Structures' layer with UniqueValueRenderer.")
                else:
                    arcpy.AddMessage(f"Layer '{layer.name}' is not 'Structures' or does not have a valid renderer.")
        
        # Save the updated project into a new copy.
        project.saveACopy(outputPath)
        arcpy.SetProgressorPosition(max)
        arcpy.SetProgressorLabel("Saving the project...")
        arcpy.AddMessage(f"Project saved to: {outputPath}")
        time.sleep(readTime)

        return


class Lab6_Tool_Trees(object):
    def __init__(self):
        """Define the tool for Task 2."""
        self.label = "Lab6_Tool_Trees"
        self.description = "Tool to update renderer for the Trees layer"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param_proj_path = arcpy.Parameter(
            displayName="Project File Path",
            name="project_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param_layer_name = arcpy.Parameter(
            displayName="Layer Name",
            name="layer_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_output_path = arcpy.Parameter(
            displayName="Output Project File Path",
            name="output_project_path",
            datatype="DEFile",
            parameterType="Optional",
            direction="Output"
        )

        params = [param_proj_path, param_layer_name, param_output_path]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Setup the progressor
        readTime = 3
        start = 0
        max = 100
        step = 50  # Progress for each layer
        arcpy.SetProgressor("step", "Starting rendering process for Trees...", start, max, step)

        # Add message to the results pane
        arcpy.AddMessage("Initializing the tool...")

        # Accept user input from toolbox interface
        aprxFilePath = parameters[0].valueAsText
        layerName = parameters[1].valueAsText
        outputPath = parameters[2].valueAsText if parameters[2].valueAsText else aprxFilePath.replace(".aprx", "_trees_updated.aprx")

        # Fetch the project
        project = arcpy.mp.ArcGISProject(aprxFilePath)
        layers = project.listMaps('Map')[0].listLayers()

        # Loop through the layers
        for layer in layers:
            if layer.isFeatureLayer:
                symbology = layer.symbology
                # Advance the progressor here
                arcpy.SetProgressorPosition(start + step)
                arcpy.SetProgressorLabel(f"Processing layer: {layer.name}")
                arcpy.AddMessage(f"Processing layer: {layer.name}")
                time.sleep(readTime)

                if hasattr(symbology, 'renderer') and layer.name == 'Trees':
                    # Re-render the 'Trees' layer into 'GraduatedColorsRenderer'
                    symbology.updateRenderer('GraduatedColorsRenderer')
                    symbology.renderer.classificationField = "Shape_Area"
                    symbology.renderer.breakCount = 5
                    # Use a default color ramp if "Yellow to Green" is not found
                    color_ramps = project.listColorRamps("Yellow to Red")
                    if color_ramps:
                        symbology.renderer.colorRamp = color_ramps[0]
                    else:
                        # Fallback to a default color ramp (e.g., first available ramp)
                        symbology.renderer.colorRamp = project.listColorRamps()[0]

                    layer.symbology = symbology
                    arcpy.AddMessage("Updated 'Trees' layer with GraduatedColorsRenderer.")
                else:
                    arcpy.AddMessage(f"Layer '{layer.name}' is not 'Trees' or does not have a valid renderer.")
        
        # Save the updated project into a new copy.
        project.saveACopy(outputPath)
        arcpy.SetProgressorPosition(max)
        arcpy.SetProgressorLabel("Saving the project...")
        arcpy.AddMessage(f"Project saved to: {outputPath}")
        time.sleep(readTime)

        return
