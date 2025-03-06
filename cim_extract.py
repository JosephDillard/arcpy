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
        if layer.isFeatureLayer or layer.isRasterLayer:
            # Get the layer's CIM definition
            cim_layer = layer.getDefinition("V2")
            description = cim_layer.description if cim_layer else "No Description"
            
            # Store layer details
            layer_info.append([layer.name, description])
    except Exception as e:
        layer_info.append([layer.name, f"Error: {str(e)}"])

# Create a Pandas DataFrame
df = pd.DataFrame(layer_info, columns=["Layer Name", "Description"])

# Export to Excel
output_excel = r"C:\GIS\Layer_Descriptions.xlsx"  # Change path as needed
df.to_excel(output_excel, index=False)

print(f"Excel file saved at: {output_excel}")