import arcpy
import pandas as pd
import os

# Get the current ArcGIS Pro project and active map
aprx = arcpy.mp.ArcGISProject("CURRENT")
map_obj = aprx.activeMap

# List to store field data
data_list = []

# Iterate through layers
for layer in map_obj.listLayers():
    if layer.isFeatureLayer:
        cim_layer = layer.getDefinition("V2")  # Get CIM definition

        # Retrieve fields using CIM
        if hasattr(cim_layer, "featureTable"):
            fields = cim_layer.featureTable.fieldDescriptions  # CIM field properties
            
            for field in fields:
                field_name = field.name
                field_alias = field.alias if hasattr(field, "alias") else "N/A"
                field_type = field.fieldType if hasattr(field, "fieldType") else "Unknown"
                field_index = fields.index(field)  # Get field index

                # Store data in list
                data_list.append([layer.name, field_name, field_alias, field_type, field_index])

# Convert to DataFrame
df = pd.DataFrame(data_list, columns=["Layer Name", "Field Name", "Field Alias", "Field Type", "Index"])

# Define output path to Scratch folder on E drive
output_dir = "E:\\Scratch"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
output_file = os.path.join(output_dir, "Layer_Fields_CIM.xlsx")

# Export to Excel
df.to_excel(output_file, index=False)

print(f"Exported field details using CIM to {output_file}")