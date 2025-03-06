import arcpy
import pandas as pd
from arcpy import mp

# Get the current ArcGIS Pro project and active map
aprx = mp.ArcGISProject("CURRENT")
m = aprx.activeMap

# List to store layer information
layer_info = []

# Iterate through all layers in the map
for layer in m.listLayers():
    try:
        # Get CIM definition
        cim_layer = layer.getDefinition("V2")
        layer_id = cim_layer.uRI if cim_layer else "N/A"  # Unique Layer ID
        description = cim_layer.description if cim_layer else "No Description"

        # General layer properties
        layer_type = layer.dataSource if layer.supports("DATASOURCE") else "N/A"
        visibility = layer.visible
        selectable = layer.canSelect
        definition_query = layer.definitionQuery if layer.supports("DEFINITIONQUERY") else "N/A"

        # Initialize additional properties
        table_name = "N/A"
        is_versioned = "N/A"
        spatial_ref = "N/A"
        source_path = "N/A"
        workspace_type = "N/A"
        has_join = "No"
        has_relationship_class = "No"
        feature_count = "N/A"
        renderer_type = "N/A"
        transparency = "N/A"
        labeling_enabled = "N/A"

        # Feature layer-specific properties
        if layer.isFeatureLayer:
            desc = arcpy.Describe(layer)
            table_name = getattr(desc, "name", "N/A")
            source_path = getattr(desc, "catalogPath", "N/A")
            workspace_type = getattr(desc, "workspaceType", "N/A")

            # Check for versioning (Enterprise GDB)
            if workspace_type == "RemoteDatabase":
                is_versioned = "Yes" if getattr(desc, "isVersioned", False) else "No"

            # Spatial reference (Projection)
            if hasattr(desc, "spatialReference"):
                spatial_ref = desc.spatialReference.name if desc.spatialReference else "Unknown"

            # Joins & Relationships
            has_join = "Yes" if len(layer.listJoins()) > 0 else "No"
            has_relationship_class = "Yes" if hasattr(desc, "relationshipClassNames") and desc.relationshipClassNames else "No"

            # Feature Count
            try:
                feature_count = arcpy.GetCount_management(layer).getOutput(0)
            except:
                feature_count = "Error"

        # Renderer Type
        if layer.supports("SYMBOLOGY"):
            renderer = layer.symbology
            renderer_type = type(renderer).__name__

        # Transparency
        if layer.supports("TRANSPARENCY"):
            transparency = layer.transparency

        # Labeling Enabled
        if layer.supports("LABELCLASSES"):
            labeling_enabled = "Yes" if layer.listLabelClasses()[0].enabled else "No"

        # Store collected details
        layer_info.append([
            layer.name, layer_id, description, layer_type, table_name, source_path, 
            is_versioned, workspace_type, spatial_ref, visibility, selectable, 
            definition_query, has_join, has_relationship_class, feature_count, 
            renderer_type, transparency, labeling_enabled
        ])
    
    except Exception as e:
        layer_info.append([layer.name, "Error", f"Error: {str(e)}"] + ["N/A"] * 15)

# Create a Pandas DataFrame
df = pd.DataFrame(layer_info, columns=[
    "Layer Name", "Layer ID", "Description", "Layer Type", "Table Name", 
    "Source Path", "Is Versioned", "Workspace Type", "Spatial Reference", 
    "Visibility", "Selectable", "Definition Query", "Has Join", 
    "Has Relationship Class", "Feature Count", "Renderer Type", 
    "Transparency", "Labeling Enabled"
])

# Export to Excel
output_excel = r"C:\GIS\Layer_Details.xlsx"  # Change path as needed
df.to_excel(output_excel, index=False)

print(f"Excel file saved at: {output_excel}")