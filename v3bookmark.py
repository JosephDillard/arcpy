import arcpy
import pandas as pd
import json

# Set the path to your ArcGIS Pro project file (.aprx)
aprx_path = r"C:\Path\To\YourProject.aprx"

# Load the ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject(aprx_path)

# Get the first layout in the project
layout = aprx.listLayouts()[0]  # Modify index if needed

# Get the first map frame in the layout
map_frame = layout.listElements("MAPFRAME_ELEMENT")[0]  # Modify index if needed

# Get the associated map
map_obj = map_frame.map

# Prepare a list to store bookmark data
bookmarks_list = []

# Loop through bookmarks
for bookmark in map_obj.listBookmarks():
    # Apply the bookmark to the map frame (only works if ArcGIS Pro UI is open)
    map_frame.zoomToBookmark(bookmark)

    # Get the extent of the current map view
    extent = map_frame.camera.getExtent()

    # Construct ArcGIS Server REST API ring format
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
        "spatialReference": {"wkid": 4326}  # Adjust WKID as needed
    }

    # Store data
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

print(f"Bookmarks extracted and saved as JSON in {excel_path}")