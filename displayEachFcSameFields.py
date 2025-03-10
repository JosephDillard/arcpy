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
                desc = arcpy.Describe(lyr)
                vis_fields = {f.name for f in desc.fields if f.name in lyr.visibleFields}
                all_visible_fields.update(vis_fields)
            except Exception as e:
                print(f"Error accessing fields for {lyr.name}: {e}")

        # Ensure all layers have the same visible fields
        for lyr in layers:
            try:
                current_visible = set(lyr.visibleFields)
                missing_fields = all_visible_fields - current_visible
                
                if missing_fields:
                    print(f"Updating layer {lyr.name}: Turning on {missing_fields}")
                    
                    # Enable missing fields
                    lyr.visibleFields = list(all_visible_fields)  # Assigns all visible fields
            except Exception as e:
                print(f"Error updating visibility for {lyr.name}: {e}")

    print("Layer visibility synchronized successfully.")

# Run the function
synchronize_layer_visibility()