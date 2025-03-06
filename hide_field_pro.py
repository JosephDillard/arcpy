import arcpy

# Define the ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("CURRENT")  # Use "CURRENT" for the open project
field_to_unhide = "YourFieldName"  # Change to the field you want to unhide

# Iterate through all maps in the project
for m in aprx.listMaps():
    for lyr in m.listLayers():
        # Ensure the layer supports field info modification
        if lyr.supports("FIELDINFO"):
            field_info = lyr.fieldInfo
            field_found = False  # Flag to track if the field is found in the layer
            
            # Loop through all fields in the layer
            for i in range(field_info.count):
                field_name = field_info.getFieldName(i)
                if field_name == field_to_unhide:
                    field_info.setVisible(i, "VISIBLE")  # Make the field visible
                    field_found = True
            
            # Apply changes if the field was found
            if field_found:
                lyr.updateConnectionProperties(lyr.connectionProperties, lyr.connectionProperties, field_info)
                print(f"Field '{field_to_unhide}' has been unhidden in layer '{lyr.name}' in map '{m.name}'.")