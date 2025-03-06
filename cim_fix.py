import arcpy
import pandas as pd
import os
from arcpy import mp

# Get the current ArcGIS Pro project and active map
aprx = mp.ArcGISProject("CURRENT")
m = aprx.activeMap

# Define output CSV file
output_csv = r"C:\GIS\Layer_Details.csv"  # Change path as needed

# Open CSV file for writing
with open(output_csv, "w", encoding="utf-8") as file:
    # Write the header row
    file.write("Layer Name,Layer ID,Description,Layer Type,Table Name,Source Path,"
               "Is Versioned,Workspace Type,Spatial Reference,Visibility,Selectable,"
               "Definition Query,Has Join,Has Relationship Class,Feature Count,"
               "Renderer Type,Transparency,Labeling Enabled\n")

    # Iterate through all layers in the map
    for layer in m.listLayers():
        try:
            # Initialize fields with default values
            layer_id = "N/A"
            description = "No Description"
            layer_type = "N/A"
            table_name = "N/A"
            source_path = "N/A"
            is_versioned = "N/A"
            workspace_type = "N/A"
            spatial_ref = "N/A"
            visibility = str(layer.visible)
            selectable = str(layer.canSelect)
            definition_query = "N/A"
            has_join = "No"
            has_relationship_class = "No"
            feature_count = "Skipped"
            renderer_type = "N/A"
            transparency = "N/A"
            labeling_enabled = "N/A"

            # Get CIM definition safely
            if layer.supports("DEFINITIONQUERY") or layer.supports("DATASOURCE"):
                try:
                    cim_layer = layer.getDefinition("V2")
                    if cim_layer:
                        layer_id = cim_layer.uRI
                        description = cim_layer.description if cim_layer.description else "No Description"
                except:
                    pass  # Some layers don’t support CIM

            # Get layer type and data source
            if layer.supports("DATASOURCE"):
                layer_type = layer.dataSource

            # If it's a feature layer, extract more details
            if layer.isFeatureLayer:
                desc = arcpy.Describe(layer)

                # Table Name
                table_name = getattr(desc, "name", "N/A")

                # Source Path
                if hasattr(layer, "connectionProperties"):
                    source_path = layer.connectionProperties['connection_info'].get('database', "N/A")
                else:
                    source_path = getattr(desc, "catalogPath", "N/A")

                # Workspace Type
                workspace_type = getattr(desc, "workspaceType", "N/A")

                # Check for versioning in Enterprise GDB
                if workspace_type == "RemoteDatabase":
                    is_versioned = "Yes" if getattr(desc, "isVersioned", False) else "No"

                # Spatial Reference
                if hasattr(desc, "spatialReference") and desc.spatialReference:
                    spatial_ref = desc.spatialReference.name

                # Check for Joins & Relationships
                has_join = "Yes" if len(layer.listJoins()) > 0 else "No"
                has_relationship_class = "Yes" if hasattr(desc, "relationshipClassNames") and desc.relationshipClassNames else "No"

                # Feature Count (Skip large layers)
                try:
                    if int(arcpy.GetCount_management(layer).getOutput(0)) < 100000:
                        feature_count = arcpy.GetCount_management(layer).getOutput(0)
                except:
                    feature_count = "Error"

            # Get Renderer Type
            if layer.supports("SYMBOLOGY"):
                try:
                    renderer = layer.symbology
                    renderer_type = type(renderer).__name__
                except:
                    renderer_type = "N/A"

            # Transparency
            if layer.supports("TRANSPARENCY"):
                transparency = str(layer.transparency)

            # Labeling Enabled
            if layer.supports("LABELCLASSES") and layer.listLabelClasses():
                labeling_enabled = "Yes" if layer.listLabelClasses()[0].enabled else "No"

            # Write data to CSV file
            file.write(f"{layer.name},{layer_id},{description},{layer_type},{table_name},{source_path},"
                       f"{is_versioned},{workspace_type},{spatial_ref},{visibility},{selectable},"
                       f"{definition_query},{has_join},{has_relationship_class},{feature_count},"
                       f"{renderer_type},{transparency},{labeling_enabled}\n")

        except Exception as e:
            file.write(f"{layer.name},Error,Error: {str(e)},N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A\n")

print(f"CSV file saved at: {output_csv}")