import arcpy
import pandas as pd
import json

# Use the currently open ArcGIS Pro session
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Get the first open map (modify if needed)
maps = aprx.listMaps()
if not maps:
    print("No maps found in the current project.")
    raise SystemExit
map_obj = maps[0]  # Select the first map

# Get a layout with a map frame (needed to extract extents)
layouts = aprx.listLayouts()
if not layouts:
    print("No layouts found in the project. A layout with a MapFrame is required.")
    raise SystemExit

# Find a map frame associated with the selected map
map_frame = None
for layout in layouts:
    for mf in layout.listElements("MAPFRAME_ELEMENT"):
        if mf.map.name == map_obj.name:
            map_frame = mf
            break
    if map_frame:
        break

if not map_frame:
    print("No matching MapFrame found for the active map. Open a layout with a linked MapFrame.")
    raise SystemExit

# Prepare a list to store bookmark data
bookmarks_list = []

# Loop through bookmarks and extract extents
for bookmark in map_obj.listBookmarks():
    # Zoom to the bookmark (this updates the map frame’s camera)
    map_frame.zoomToBookmark(bookmark)

    # Get the current extent of the map frame
    extent = map_frame.camera.getExtent()

    # Create a ring geometry in ArcGIS Server REST format
    ring_geometry = {
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
    }

    # Store bookmark data
    bookmark_data = {
        "map_name": map_obj.name,
        "bookmark_name": bookmark.name,
        "geometry": ring_geometry
    }
    bookmarks_list.append(bookmark_data)

# Convert the list to a JSON string
json_data = json.dumps(bookmarks_list, indent=4)

# Save JSON string in a DataFrame
df = pd.DataFrame({"Bookmarks_JSON": [json_data]})

# Define Excel file path (modify as needed)
excel_path = r"C:\Temp\Output_Bookmarks.xlsx"

# Save DataFrame to Excel
df.to_excel(excel_path, index=False)

print(f"✅ Bookmarks extracted and saved as JSON in {excel_path}")