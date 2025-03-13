import arcpy
import pandas as pd
import json

# Use the currently open ArcGIS Pro session
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Get all maps in the open project
maps = aprx.listMaps()

if not maps:
    print("No maps found in the current project.")
    raise SystemExit

# Prepare a list to store bookmark data
bookmarks_list = []

# Loop through maps and extract bookmark extents
for map_obj in maps:
    for bookmark in map_obj.listBookmarks():
        extent = bookmark.extent  # ✅ This correctly gets the bookmark's extent

        if not extent:
            print(f"⚠ Warning: No extent found for bookmark '{bookmark.name}' in map '{map_obj.name}'. Skipping.")
            continue  # Skip this bookmark if no extent is found

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

# Define Excel file path (modify if needed)
excel_path = r"C:\Temp\Output_Bookmarks.xlsx"

# Save DataFrame to Excel
df.to_excel(excel_path, index=False)

print(f"✅ Bookmarks extracted and saved as JSON in {excel_path}")