import arcpy
import pandas as pd
import os

# Get the current ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Set output Excel file path (stored in the scratch folder)
output_excel = os.path.join(arcpy.env.scratchFolder, "symbology_reference_scale.xlsx")

# Prepare a list to store symbology details
data = []

# Print header for console output
print("\n--- Symbology, Display Field, and Reference Scale Information ---\n")
print(f"{'Map Name':<20} {'Layer Name':<30} {'Symbology Field(s)':<40} {'Display Field':<30} {'Reference Scale':<15}")

# Iterate through all maps in the project
for m in aprx.listMaps():
    ref_scale = m.referenceScale  # Get the reference scale of the map
    for lyr in m.listLayers():
        if lyr.isFeatureLayer:
            sym = lyr.symbology
            display_field = lyr.displayField  # Correctly retrieve display field
            symbology_field = None

            if hasattr(sym, "renderer"):
                renderer = sym.renderer

                # Get the field used for symbology based on renderer type
                if renderer.type == "SimpleRenderer":
                    symbology_field = "N/A (Single Symbol)"
                elif renderer.type == "UniqueValueRenderer":
                    symbology_field = ", ".join(renderer.fields)  # List of fields used
                elif renderer.type == "ClassBreaksRenderer":
                    symbology_field = renderer.field  # Single field
                
                # Append layer details to the data list
                data.append([m.name, lyr.name, symbology_field, display_field, ref_scale])
                
                # Print layer details to console
                print(f"{m.name:<20} {lyr.name:<30} {str(symbology_field):<40} {display_field:<30} {ref_scale:<15}")

# Create a DataFrame and export to Excel
df = pd.DataFrame(data, columns=["Map Name", "Layer Name", "Symbology Field(s)", "Display Field", "Reference Scale"])
df.to_excel(output_excel, index=False)

# Print output file location
print(f"\nExcel file saved at: {output_excel}")