import arcpy
import pandas as pd

# Open the current ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Prepare an empty list to store relationship data
relationship_data = []

# Iterate through maps in the project
for map_obj in aprx.listMaps():
    for layer in map_obj.listLayers():
        if layer.isFeatureLayer:
            try:
                # Get relationships for the feature layer
                desc = arcpy.Describe(layer)
                if hasattr(desc, "relationshipClasses"):
                    for rel_class in desc.relationshipClasses:
                        relationship_data.append({
                            "Map": map_obj.name,
                            "Layer": layer.name,
                            "Relationship Class": rel_class.name,
                            "Origin Table": rel_class.originClassNames,
                            "Destination Table": rel_class.destinationClassNames,
                            "Forward Path Label": rel_class.forwardPathLabel,
                            "Backward Path Label": rel_class.backwardPathLabel,
                            "Cardinality": rel_class.cardinality
                        })
            except Exception as e:
                print(f"Error processing layer {layer.name}: {e}")

# Convert list to pandas DataFrame
df = pd.DataFrame(relationship_data)

# Define Excel output path in the user's Documents folder
excel_path = r"C:\Users\{}\Documents\LayerRelationships.xlsx".format(arcpy.GetSystemEnvironment("USERNAME"))

# Save to Excel
if not df.empty:
    df.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"Relationship data saved to {excel_path}")
else:
    print("No relationships found in the current project.")