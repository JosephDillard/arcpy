import arcpy
import pandas as pd
import json

# Use the currently open ArcGIS Pro session
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Get all maps in the project
maps = aprx.listMaps()

if not maps:
    print("No maps found in the current project.")
    raise SystemExit

# Prepare a list to store bookmark data
bookmarks_list = []

# Get layouts and check for a map frame
layouts = aprx.listLayouts()
if not layouts:
    print("No layouts found in the project. A layout with a MapFrame is required.")
    raise SystemExit

# Find a map frame associated with each map
for map_obj in maps:
    map_frame = None

    for layout in layouts:
        for mf in layout.listElements("MAPFRAME_ELEMENT"):
            if mf.map.name == map_obj.name:  # Match map frame to the map
                map_frame = mf
                break
        if map_frame:
            break

    if not map_frame:
        print(f"⚠ No matching MapFrame found for map '{map_obj.name}'. Skipping.")
        continue  # Skip this map if no MapFrame is found

    # Loop through bookmarks and extract extents
    for bookmark in map_obj.listBookmarks():
        # Zoom to the bookmark (this updates the map frame’s camera)
        map_frame.zoomToBookmark(bookmark)

        # Get the current extent of the map frame
        extent = map_frame.camera.getExtent()

        # Create a ring geometry in ArcGIS Server REST format
        ring_geometry = json.dumps({
            "rings": [
                [
                    [extent.XMin, extent.YMin],  # Bottom-left
                    [extent.XMin, extent.YMax],  # Top-left
                    [extent.XMax, extent.YMax],  # Top-right
                    [extent.XMax, extent.YMin],  # Bottom-right
                    [extent.XMin, extent.YMin]   # Close the ring
                ]
            ],
            "spatialReference": {"wkid": 4326}  # WGS 84 (Change WKID if needed)
        })

        # Store bookmark data in separate columns
        bookmarks_list.append({
            "Map Name": map_obj.name,
            "Bookmark Name": bookmark.name,
            "Geometry (Rings)": ring_geometry
        })

# Convert the list to a DataFrame
df = pd.DataFrame(bookmarks_list)

# Define Excel file path (modify as needed)
excel_path = r"C:\Temp\Output_Bookmarks.xlsx"

# Save DataFrame to Excel
df.to_excel(excel_path, index=False)

print(f"✅ All bookmarks extracted and saved as separate columns in {excel_path}")