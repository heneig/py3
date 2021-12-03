# -*- coding: utf-8 -*-
import os
import arcpy


def proj_data(img, temp_path):
    arcpy.CheckOutExtension('Spatial')

    temp_gdb = os.path.join(temp_path, 'temp.gdb')
    if os.path.exists(temp_gdb):
        pass
    else:
        arcpy.CreateFileGDB_management(temp_path, "temp.gdb")
    img_ = img.replace(' (', '_')
    img_ = img_.replace(')', '')
    img_proj_out = os.path.join(temp_gdb, img_.split('Plan 02\\')[1].split('.tif')[0])
    img_proj_out_tif = os.path.join(temp_path, img.split('Plan 02\\')[1])

    img_arcpy_proj = arcpy.SpatialReference("WGS 1984")
    dem_arcpy_proj = arcpy.SpatialReference("China Geodetic Coordinate System 2000")
    gtf = u'E:\\工作三\\水旱普查\\py3\\WGS_84_to_CGCS_2000.gtf'
    # arcpy.ProjectRaster_management(in_raster=img, out_raster=img_proj_out, out_coor_system=dem_arcpy_proj,
    #                                resampling_type="NEAREST", cell_size="#", geographic_transform='#',
    #                                Registration_Point="#", in_coor_system=img_arcpy_proj)
    arcpy.ProjectRaster_management(img, img_proj_out, dem_arcpy_proj, "NEAREST", "#", "#", "#", img_arcpy_proj)
    arcpy.CopyRaster_management(img_proj_out, img_proj_out_tif, "DEFAULTS", "", "", "", "", "")
    return img_proj_out_tif


if __name__ == "__main__":
    img = u"E:\\工作三\\水旱普查\\20211117\\Linxia\\1Linxiashi\\Plan 02\\Depth (10).tif1.tif"
    dem = u"E:\\工作三\\水旱普查\\20211117\\mubiaotouying.tif"
    temp_path = u'E:\\工作三\\水旱普查\\py3\\临时_加载'
    proj_data(img, temp_path)

"""代码来源"""
"""https://blog.csdn.net/qq_20373723/article/details/111311307"""
# # -*- coding: utf-8 -*-
# import os, sys
# import time
# import math
# import cv2
# import gdal
# import arcpy
# from arcpy import *
# from arcpy import env
# import numpy as np
#
#
# def read_img(filename):
#     dataset = gdal.Open(filename)
#     im_width = dataset.RasterXSize
#     im_height = dataset.RasterYSize
#     im_geotrans = dataset.GetGeoTransform()
#     im_proj = dataset.GetProjection()
#     im_data = dataset.ReadAsArray(0, 0, im_width, im_height)
#     del dataset
#     return im_proj, im_geotrans, im_width, im_height, im_data
#
#
# def proj_data(img, dem, temp_path, temp_gdb):
#     im_proj, im_geotrans, im_width, im_height, img_data = read_img(img)
#     dem_proj, dem_geotrans, dem_width, dem_height, dem_data = read_img(dem)
#     img_proj_out = os.path.join(temp_gdb, 'img_p')
#     img_proj_out_tif = os.path.join(temp_path, 'img_p.tif')
#     cell_size_str = str(abs(im_geotrans[1])) + ' ' + str(abs(im_geotrans[5]))
#
#     img_arcpy_proj = arcpy.Describe(img).spatialReference
#     dem_arcpy_proj = arcpy.Describe(dem).spatialReference
#
#     arcpy.ProjectRaster_management(in_raster=img, out_raster=img_proj_out, out_coor_system=dem_arcpy_proj,
#                                    resampling_type="NEAREST", cell_size="#", geographic_transform="#",
#                                    Registration_Point="#", in_coor_system=img_arcpy_proj)
#     arcpy.CopyRaster_management(img_proj_out, img_proj_out_tif, "DEFAULTS", "", "", "", "", "")
#     return img_proj_out_tif
#
#
# if __name__ == "__main__":
#     img = "xxx/t_1.tif"
#     dem = "xxx/t_dem.tif"
#     shp = ""
#     temp_path = "xxx/temp_t/"
#
#     arcpy.CheckOutExtension('Spatial')
#     arcpy.env.overwriteOutput = True
#     env.workspace = "xxx/"
#
#     gdb_file = "xxx/"
#     temp_gdb = os.path.join(gdb_file, 'temp.gdb')
#     if os.path.exists(temp_gdb):
#         pass
#     else:
#         arcpy.CreateFileGDB_management(gdb_file, "temp.gdb")
#
#     proj_data(img, dem, temp_path, temp_gdb)
