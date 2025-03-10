import arcpy

# Open the current ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Loop through all maps in the project
for m in aprx.listMaps():
    for lyr in m.listLayers():
        if lyr.isFeatureLayer:
            try:
                # Get the layer's CIM definition
                cim_lyr = lyr.getDefinition('V3')

                # Ensure the layer has a feature table
                if hasattr(cim_lyr, 'featureTable') and cim_lyr.featureTable is not None:
                    # Set all fields to visible
                    for field_desc in cim_lyr.featureTable.fieldDescriptions:
                        field_desc.visible = True  # Make the field visible

                    # Apply the updated CIM definition
                    lyr.setDefinition(cim_lyr)

                    print(f"Enabled all fields for layer: {lyr.name}")
                else:
                    print(f"Layer {lyr.name} does not have a feature table.")
            except Exception as e:
                print(f"Could not update fields for layer {lyr.name}: {e}")

# Save changes
aprx.save()
print("All fields are now visible.")