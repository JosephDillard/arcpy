import arcpy
import pandas as pd
import os

# Define the ArcGIS Pro project (CURRENT if running inside ArcGIS Pro)
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Initialize an empty list to store results
data = []

# Loop through all maps in the project
for m in aprx.listMaps():
    print(f"Checking map: {m.name}")
    
    # Loop through all layers in the map
    for lyr in m.listLayers():
        if lyr.supports("DATASOURCE"):  # Ensure the layer has a data source
            try:
                desc = arcpy.Describe(lyr)
                
                # Check if it's a feature layer
                if hasattr(desc, "featureClass"):
                    fields = arcpy.ListFields(lyr.dataSource)
                    
                    # Collect required fields
                    for field in fields:
                        if field.required:
                            data.append([m.name, lyr.name, field.name, field.type])

            except Exception as e:
                print(f"Error checking layer {lyr.name}: {e}")

# Create a DataFrame
df = pd.DataFrame(data, columns=["Map Name", "Layer Name", "Required Field", "Field Type"])

# Define the output Excel file path
output_folder = os.path.expanduser("~/Documents")  # Adjust as needed
output_file = os.path.join(output_folder, "Required_Fields.xlsx")

# Save to Excel
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Required Fields", index=False)

print(f"\nCompleted! Results saved to {output_file}")