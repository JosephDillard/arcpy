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
                    # Get all field names using .fieldName
                    fields = [field.fieldName for field in arcpy.ListFields(lyr)]
                    
                    # Set all fields to be visible
                    cim_lyr.featureTable.fieldDescriptions = [
                        arcpy.cim.FieldDescription(name=field, visible=True) for field in fields
                    ]
                    
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