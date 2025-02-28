import arcpy
import pandas as pd

# Path to the Excel file
excel_path = r"C:\path\to\your\excel_file.xlsx"

# Read the Excel file, loading all sheets into a dictionary of DataFrames
xls = pd.read_excel(excel_path, sheet_name=None)

# Set the ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.activeMap  # Get the active map

# Iterate through sheets (each sheet corresponds to a layer)
for sheet_name, df in xls.items():
    layer_name = sheet_name  # Assume sheet name matches layer name
    layer = None
    
    # Find the corresponding layer in the project
    for lyr in m.listLayers():
        if lyr.name == layer_name:
            layer = lyr
            break
    
    if layer is None:
        print(f"Layer '{layer_name}' not found in the project. Skipping...")
        continue

    # Ensure the layer supports field visibility changes
    if not layer.isFeatureLayer:
        print(f"Layer '{layer_name}' is not a feature layer. Skipping...")
        continue

    # Read field visibility settings from the Excel sheet
    field_visibility = {row["Field Name"]: row["Hide Field"] for _, row in df.iterrows()}

    # Modify field visibility
    fc_def = layer.listFields()  # Get layer fields
    layer_cim = layer.getDefinition("V2")  # Get layer's CIM definition

    for field in fc_def:
        if field.name in field_visibility:
            hide = field_visibility[field.name].strip().lower() == "yes"
            
            for field_cim in layer_cim.featureTable.fieldDescriptions:
                if field_cim.name == field.name:
                    field_cim.visible = not hide  # Hide field if "Yes"
                    print(f"{'Hiding' if hide else 'Showing'} field: {field.name} in {layer_name}")
    
    # Apply changes
    layer.setDefinition(layer_cim)

# Save project
aprx.save()
print("Field visibility updates completed.")
