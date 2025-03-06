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
        # Get layer CIM definition
        cim_layer = layer.getDefinition("V2")
        layer_id = cim_layer.uRI if cim_layer else "N/A"  # Unique Layer ID
        description = cim_layer.description if cim_layer else "No Description"

        # Initialize variables
        table_name = "N/A"
        is_versioned = "N/A"
        spatial_ref = "N/A"

        # Check if the layer is a feature layer
        if layer.isFeatureLayer:
            # Get the underlying data source
            desc = arcpy.Describe(layer)
            if hasattr(desc, "name"):
                table_name = desc.name  # Feature class name

            # Check if it's in an enterprise geodatabase and if it's versioned
            if hasattr(desc, "workspaceType") and desc.workspaceType == "RemoteDatabase":
                if hasattr(desc, "isVersioned"):
                    is_versioned = "Yes" if desc.isVersioned else "No"

            # Get spatial reference (projection)
            if hasattr(desc, "spatialReference"):
                spatial_ref = desc.spatialReference.name if desc.spatialReference else "Unknown"

        # Store layer details
        layer_info.append([layer.name, layer_id, description, table_name, is_versioned, spatial_ref])
    
    except Exception as e:
        layer_info.append([layer.name, "Error", f"Error: {str(e)}", "N/A", "N/A", "N/A"])

# Create a Pandas DataFrame
df = pd.DataFrame(layer_info, columns=["Layer Name", "Layer ID", "Description", "Table Name", "Is Versioned", "Spatial Reference"])

# Export to Excel
output_excel = r"C:\GIS\Layer_Details.xlsx"  # Change path as needed
df.to_excel(output_excel, index=False)

print(f"Excel file saved at: {output_excel}")