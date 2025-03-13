import arcpy
import pandas as pd
import json

# Set the path to your ArcGIS Pro project file (.aprx)
aprx_path = r"C:\Path\To\YourProject.aprx"

# Load the ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject(aprx_path)

# Get the active map view (this only works in an open ArcGIS Pro session)
map_views = aprx.listViews()  # Get all open MapViews

if not map_views:
    print("No active MapViews found. Open a map in ArcGIS Pro and try again.")
    raise SystemExit

map_view = map_views[0]  # Use the first available MapView

# Prepare a list to store bookmark envelope data
bookmarks_list = []

# Get the associated map from the active MapView
map_obj = map_view.map

if not map_obj:
    print("No map associated with the active MapView.")
    raise SystemExit

# Loop through bookmarks and extract extents
for bookmark in map_obj.listBookmarks():
    # Zoom to the bookmark (updates the MapView's extent)
    map_view.zoomToBookmark(bookmark)

    # Get the current extent of the active MapView
    extent = map_view.camera.getExtent()  # ✅ Correctly extracts extent now

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

# Define Excel file path
excel_path = r"C:\Path\To\Output_Bookmarks.xlsx"

# Save DataFrame to Excel
df.to_excel(excel_path, index=False)

print(f"✅ Bookmarks extracted and saved as JSON in {excel_path}")