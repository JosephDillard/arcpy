import arcpy
import arcpy.mp

def synchronize_layer_visibility():
    # Get the currently open ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    
    # Dictionary to store layers by data source
    layer_dict = {}

    # Loop through all maps in the project
    for m in aprx.listMaps():
        for lyr in m.listLayers():
            if lyr.isFeatureLayer:  # Only consider feature layers
                try:
                    # Get the data source
                    conn_props = lyr.connectionProperties
                    source = conn_props["connection_info"]["database"] + "\\" + conn_props["dataset"]
                    
                    # Group layers by their data source
                    if source not in layer_dict:
                        layer_dict[source] = []
                    layer_dict[source].append(lyr)
                except KeyError:
                    print(f"Skipping layer {lyr.name}: Unable to get data source")

    # Process each group of layers that share the same data source
    for source, layers in layer_dict.items():
        print(f"Processing layers from source: {source}")

        # Get the set of all fields that should be visible
        all_visible_fields = set()

        for lyr in layers:
            try:
                # Access layer CIM definition
                cim_layer = lyr.getDefinition("V2")
                if cim_layer is not None and hasattr(cim_layer, "fieldDescriptions"):
                    vis_fields = {f.fieldName for f in cim_layer.fieldDescriptions if f.visible}
                    all_visible_fields.update(vis_fields)
            except Exception as e:
                print(f"Error accessing fields for {lyr.name}: {e}")

        # Ensure all layers have the same visible fields
        for lyr in layers:
            try:
                cim_layer = lyr.getDefinition("V2")
                if cim_layer is not None and hasattr(cim_layer, "fieldDescriptions"):
                    for field in cim_layer.fieldDescriptions:
                        if field.fieldName in all_visible_fields:
                            field.visible = True  # Ensure visibility
                    
                    # Apply changes back to the layer
                    lyr.setDefinition(cim_layer)
                    print(f"Updated layer {lyr.name}: All relevant fields are now visible.")
            except Exception as e:
                print(f"Error updating visibility for {lyr.name}: {e}")

    print("Layer visibility synchronized successfully.")

# Run the function
synchronize_layer_visibility()