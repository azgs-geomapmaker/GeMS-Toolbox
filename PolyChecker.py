import arcpy, os, sys

gdb = "C:/output/PolyCheck.gdb"

if arcpy.Exists(gdb):
    arcpy.Delete_management(gdb)
    arcpy.AddMessage(arcpy.GetMessages())

if not os.path.exists(os.path.dirname(gdb)):
    os.mkdir(os.path.dirname(gdb))

arcpy.CreateFileGDB_management(os.path.dirname(gdb), os.path.basename(gdb))
arcpy.AddMessage(arcpy.GetMessages())

arcpy.env.workspace = gdb

arcpy.AddMessage(gdb)

# Script arguments
MapUnitPolys = arcpy.GetParameterAsText(0)
if MapUnitPolys == '#' or not MapUnitPolys:
    MapUnitPolys = "MapUnitPolys"  # provide a default value if unspecified

MapUnitPolys_CopyFeatures = arcpy.GetParameterAsText(1)

# Set Geoprocessing environments
MapUnitPolys = MapUnitPolys

Polygon_Neighbors = r"C:/output/PolyCheck.gdb/polytest"

PolygonNeighbor_TableSelect = r"C:/output/PolyCheck.gdb/PolygonNeighbor_TableSelect"

inFeatures_lyr = r"C:/output/PolyCheck.gdb/inFeatures_lyr"


# Process: Polygon Neighbors
arcpy.PolygonNeighbors_analysis(MapUnitPolys, Polygon_Neighbors, "OBJECTID;MapUnit", "NO_AREA_OVERLAP", "BOTH_SIDES",
                                "", "METERS", "SQUARE_METERS")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(Polygon_Neighbors, "NEW_SELECTION", "src_MapUnit = nbr_MapUnit")

# Process: Table Select
arcpy.TableSelect_analysis(Polygon_Neighbors, PolygonNeighbor_TableSelect, "src_MapUnit = nbr_MapUnit")

arcpy.GetCount_management(PolygonNeighbor_TableSelect)

arcpy.AddMessage(arcpy.GetMessages())

if int(arcpy.GetCount_management(PolygonNeighbor_TableSelect)[0]) > 0:
    arcpy.MakeFeatureLayer_management(MapUnitPolys, inFeatures_lyr)
else:
    print ("done")


# Process: Add Join
arcpy.AddJoin_management(inFeatures_lyr, "OBJECTID", PolygonNeighbor_TableSelect, "src_OBJECTID", "KEEP_COMMON")

# Process: Copy Features
arcpy.CopyFeatures_management(inFeatures_lyr, MapUnitPolys_CopyFeatures, "", "0", "0", "0")

# Process: Remove Join
arcpy.RemoveJoin_management(inFeatures_lyr, "")

# Execute Delete
arcpy.Delete_management(PolygonNeighbor_TableSelect)
arcpy.Delete_management(Polygon_Neighbors)

#
arcpy.AddMessage('All done! Check Polygons')
#arcpy.AddMessage(arcpy.GetMessages())
