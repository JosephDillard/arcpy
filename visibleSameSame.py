import arcpy
import arcpy.mp

def synchronize_layer_visibility():
    # Get the currently open ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    
    # Dictionary to store layers by their feature class data source
    layer_dict = {}

    # Loop through all maps in the project
    for m in aprx.listMaps():
        for lyr in m.listLayers():
            if lyr.isFeatureLayer and lyr.supports("CONNECTIONPROPERTIES"):  # Only process feature layers
                try:
                    # Get the data source (feature class path)
                    conn_props = lyr.connectionProperties
                    source = conn_props["connection_info"]["database"] + "\\" + conn_props["dataset"]
                    
                    # Group layers that share the same data source
                    if source not in layer_dict:
                        layer_dict[source] = []
                    layer_dict[source].append(lyr)
                except KeyError:
                    print(f"Skipping layer {lyr.name}: Unable to get data source")

    # Process each group of layers that reference the same feature class
    for source, layers in layer_dict.items():
        print(f"Processing layers from source: {source}")

        # Collect all fields that should be visible across these layers
        all_visible_fields = set()

        for lyr in layers:
            try:
                # Get CIM definition for the layer
                cim_layer = lyr.getDefinition("V2")
                if cim_layer and hasattr(cim_layer, "fieldDescriptions"):
                    visible_fields = {f.fieldName for f in cim_layer.fieldDescriptions if f.visible}
                    all_visible_fields.update(visible_fields)
            except Exception as e:
                print(f"Error accessing fields for {lyr.name}: {e}")

        # Ensure all layers have the same visible fields
        for lyr in layers:
            try:
                cim_layer = lyr.getDefinition("V2")
                if cim_layer and hasattr(cim_layer, "fieldDescriptions"):
                    updated = False  # Track if we modify anything
                    
                    for field in cim_layer.fieldDescriptions:
                        if field.fieldName in all_visible_fields and not field.visible:
                            field.visible = True  # Enable missing field visibility
                            updated = True
                    
                    if updated:
                        # Apply the updated CIM definition to the layer
                        lyr.setDefinition(cim_layer)
                        print(f"Updated layer '{lyr.name}': Missing fields made visible.")

                        # Force ArcGIS Pro to refresh by toggling visibility
                        lyr.visible = False
                        lyr.visible = True
            except Exception as e:
                print(f"Error updating visibility for {lyr.name}: {e}")

    print("Layer visibility synchronization complete.")

# Run the function inside ArcGIS Pro
synchronize_layer_visibility()