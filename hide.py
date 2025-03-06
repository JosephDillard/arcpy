import arcpy

# Define the ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("CURRENT")  # Use "CURRENT" for the active project
field_to_unhide = "YourFieldName"  # Change this to the field you want to unhide

# Iterate through all maps in the project
for m in aprx.listMaps():
    for lyr in m.listLayers():
        if lyr.isFeatureLayer:  # Ensure it's a feature layer
            try:
                # Get the layer's CIM definition
                cim_def = lyr.getDefinition("V2")
                
                # Iterate through fields in the CIM and make the target field visible
                field_found = False
                for field in cim_def.featureTable.fieldDescriptions:
                    if field.name == field_to_unhide:
                        field.visible = True  # Set visibility to True
                        field_found = True
                
                # Apply changes if the field was found
                if field_found:
                    lyr.setDefinition(cim_def)  # Update the layer with the modified CIM
                    print(f"Field '{field_to_unhide}' is now visible in layer '{lyr.name}' in map '{m.name}'.")
                    
            except Exception as e:
                print(f"Error processing layer '{lyr.name}': {e}")