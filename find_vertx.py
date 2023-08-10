import arcpy

# Set up workspace and input polygon feature class
arcpy.env.workspace = r"path_to_your_geodatabase.gdb"
input_feature_class = "your_polygon_feature_class"

# Define minimum distance threshold for identifying close vertices (in the map's linear unit)
min_distance_threshold = 0.1  # Adjust this value as needed

# Create a dictionary to store close vertices and their corresponding features
close_vertices = {}

# Iterate through the polygons and find close vertices
with arcpy.da.SearchCursor(input_feature_class, ["OID@", "SHAPE@"]) as cursor:
    for row in cursor:
        oid, polygon = row
        for part in polygon:
            for point in part:
                for other_part in polygon:
                    for other_point in other_part:
                        if point != other_point:
                            distance = point.distanceTo(other_point)
                            if distance < min_distance_threshold:
                                if oid not in close_vertices:
                                    close_vertices[oid] = []
                                close_vertices[oid].append(point)

# Print the results
for oid, vertices in close_vertices.items():
    print(f"Polygon OID {oid} has close vertices at:")
    for vertex in vertices:
        print(f"    {vertex.X}, {vertex.Y}")
