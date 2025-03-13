import arcpy
import pandas as pd
import json

# Set the path to your ArcGIS Pro project file (.aprx)
aprx_path = r"C:\Path\To\YourProject.aprx"

# Load the ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject(aprx_path)

# Get all maps in the project
maps = aprx.listMaps()

if not maps:
    print("No maps found in the project.")
    raise SystemExit

# Prepare a list to store bookmark envelope data
bookmarks_list = []

# Loop through maps and extract bookmarks
for map_obj in maps:
    for bookmark in map_obj.listBookmarks():
        # Get the extent of the bookmark
        extent = bookmark.extent  # ✅ Bookmark now correctly has an extent

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

        # Structure the bookmark data
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

# Define Excel file path
excel_path = r"C:\Path\To\Output_Bookmarks.xlsx"

# Save DataFrame to Excel
df.to_excel(excel_path, index=False)

print(f"✅ Bookmarks extracted and saved as JSON in {excel_path}")