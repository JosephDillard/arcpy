import arcpy
import arcpy.mp

def synchronize_layer_visibility():
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    layer_dict = {}

    # Collect all feature layers by their data source
    for m in aprx.listMaps():
        for lyr in m.listLayers():
            if lyr.isFeatureLayer and lyr.supports("CONNECTIONPROPERTIES"):
                try:
                    conn_props = lyr.connectionProperties
                    source = conn_props["connection_info"]["database"] + "\\" + conn_props["dataset"]

                    if source not in layer_dict:
                        layer_dict[source] = []
                    layer_dict[source].append(lyr)
                except KeyError:
                    print(f"Skipping {lyr.name}: Cannot determine data source")

    # Process each set of layers sharing the same data source
    for source, layers in layer_dict.items():
        print(f"\n🔍 Checking layers from source: {source}")

        all_visible_fields = set()

        # Gather all visible fields from every layer
        for lyr in layers:
            try:
                cim_layer = lyr.getDefinition("V2")
                if cim_layer and hasattr(cim_layer, "fieldDescriptions"):
                    visible_fields = {f.fieldName for f in cim_layer.fieldDescriptions if f.visible}
                    all_visible_fields.update(visible_fields)
            except Exception as e:
                print(f"⚠️ Error accessing fields for {lyr.name}: {e}")

        # Ensure all layers have the same visible fields
        for lyr in layers:
            try:
                cim_layer = lyr.getDefinition("V2")
                if cim_layer and hasattr(cim_layer, "fieldDescriptions"):
                    updated = False

                    # Modify visibility in CIM definition
                    for field in cim_layer.fieldDescriptions:
                        if field.fieldName in all_visible_fields and not field.visible:
                            print(f"✅ Enabling field '{field.fieldName}' in {lyr.name}")
                            field.visible = True
                            updated = True
                    
                    if updated:
                        # Apply CIM changes
                        lyr.setDefinition(cim_layer)
                        print(f"🎯 Updated layer '{lyr.name}': Fields made visible.")

                        # **Force UI Refresh**
                        old_name = lyr.name
                        lyr.name = old_name + "_temp"
                        lyr.name = old_name
            except Exception as e:
                print(f"⚠️ Error updating visibility for {lyr.name}: {e}")

    print("\n✅ Layer visibility synchronization complete.")

# Run inside ArcGIS Pro
synchronize_layer_visibility()