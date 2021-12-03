import gdal
import ogr
import os
import numpy as np
import csv
import pandas as pd
import time


def boundingBoxToOffsets(bbox, geot):
    col1 = int((bbox[0] - geot[0]) / geot[1])
    col2 = int((bbox[1] - geot[0]) / geot[1]) + 1
    row1 = int((bbox[3] - geot[3]) / geot[5])
    row2 = int((bbox[2] - geot[3]) / geot[5]) + 1
    return [row1, row2, col1, col2]


def geotFromOffsets(row_offset, col_offset, geot):
    new_geot = [
        geot[0] + (col_offset * geot[1]),
        geot[1],
        0.0,
        geot[3] + (row_offset * geot[5]),
        0.0,
        geot[5]
    ]
    return new_geot


def setFeatureStats(fid, min, max, mean, median, sd, sum, count,
                    names=["min", "max", "mean", "median", "sd", "sum", "count", "id"]):
    featstats = {
        names[0]: min,
        names[1]: max,
        names[2]: mean,
        names[3]: median,
        names[4]: sd,
        names[5]: sum,
        names[6]: count,
        names[7]: fid,
    }
    return featstats


def zonal(fn_raster, fn_zones, fn_csv):
    mem_driver = ogr.GetDriverByName("Memory")
    mem_driver_gdal = gdal.GetDriverByName("MEM")
    shp_name = "temp"

    # fn_raster = "C:/pyqgis/raster/USGS_NED_13_n45w116_IMG.img"
    # fn_zones = "C:/temp/zonal_stats/zones.shp"

    r_ds = gdal.Open(fn_raster)
    p_ds = ogr.Open(fn_zones)

    lyr = p_ds.GetLayer()
    geot = r_ds.GetGeoTransform()
    nodata = r_ds.GetRasterBand(1).GetNoDataValue()

    zstats = []

    p_feat = lyr.GetNextFeature()
    niter = 0

    while p_feat:
        if p_feat.GetGeometryRef() is not None:
            if os.path.exists(shp_name):
                mem_driver.DeleteDataSource(shp_name)
            tp_ds = mem_driver.CreateDataSource(shp_name)
            tp_lyr = tp_ds.CreateLayer('polygons', None, ogr.wkbPolygon)
            tp_lyr.CreateFeature(p_feat.Clone())
            offsets = boundingBoxToOffsets(p_feat.GetGeometryRef().GetEnvelope(), geot)
            new_geot = geotFromOffsets(offsets[0], offsets[2], geot)

            tr_ds = mem_driver_gdal.Create(
                "",
                offsets[3] - offsets[2],
                offsets[1] - offsets[0],
                1,
                gdal.GDT_Byte)

            tr_ds.SetGeoTransform(new_geot)
            gdal.RasterizeLayer(tr_ds, [1], tp_lyr, burn_values=[1])
            tr_array = tr_ds.ReadAsArray()

            r_array = r_ds.GetRasterBand(1).ReadAsArray(
                offsets[2],
                offsets[0],
                offsets[3] - offsets[2],
                offsets[1] - offsets[0])

            id = p_feat.GetFID()

            if r_array is not None:
                maskarray = np.ma.MaskedArray(
                    r_array,
                    maskarray=np.logical_or(r_array == nodata, np.logical_not(tr_array)))

                if maskarray is not None:
                    zstats.append(setFeatureStats(
                        id,
                        maskarray.min(),
                        maskarray.max(),
                        maskarray.mean(),
                        np.ma.median(maskarray),
                        maskarray.std(),
                        maskarray.sum(),
                        maskarray.count()))
                else:
                    zstats.append(setFeatureStats(
                        id,
                        nodata,
                        nodata,
                        nodata,
                        nodata,
                        nodata,
                        nodata,
                        nodata))
            else:
                zstats.append(setFeatureStats(
                    id,
                    nodata,
                    nodata,
                    nodata,
                    nodata,
                    nodata,
                    nodata,
                    nodata))

            tp_ds = None
            tp_lyr = None
            tr_ds = None

            p_feat = lyr.GetNextFeature()

    col_names = zstats[0].keys()
    with open(fn_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, col_names)
        writer.writeheader()
        writer.writerows(zstats)


def shp_field_value(csv_file, shp):
    data = pd.DataFrame(pd.read_csv(csv_file))
    driver = ogr.GetDriverByName('ESRI Shapefile')
    layer_source = driver.Open(shp, 1)
    lyr = layer_source.GetLayer()

    s_name = ogr.FieldDefn('min', ogr.OFTReal)
    lyr.CreateField(s_name)
    s_name = ogr.FieldDefn('max', ogr.OFTReal)
    lyr.CreateField(s_name)
    s_name = ogr.FieldDefn('mean', ogr.OFTReal)
    lyr.CreateField(s_name)
    s_name = ogr.FieldDefn('median', ogr.OFTReal)
    lyr.CreateField(s_name)
    s_name = ogr.FieldDefn('sd', ogr.OFTReal)
    lyr.CreateField(s_name)
    s_name = ogr.FieldDefn('sum', ogr.OFTReal)
    lyr.CreateField(s_name)
    s_name = ogr.FieldDefn('count', ogr.OFTReal)
    lyr.CreateField(s_name)

    count = 0
    defn = lyr.GetLayerDefn()
    featureCount = defn.GetFieldCount()
    feature = lyr.GetNextFeature()
    while feature is not None:
        for i in range(featureCount):
            feature.SetField('min', data['min'][count])
            feature.SetField('max', data['max'][count])
            feature.SetField('mean', data['mean'][count])
            feature.SetField('median', data['median'][count])
            feature.SetField('sd', data['sd'][count])
            feature.SetField('sum', data['sum'][count])
            feature.SetField('count', data['count'][count])
            lyr.SetFeature(feature)
        count += 1
        feature = lyr.GetNextFeature()


if __name__ == "__main__":
    time1 = time.time()
    fn_raster = r'E:\工作三\水旱普查\py3\临时_加载\Depth (100).tif1.tif'
    fn_zones = r'E:\工作三\水旱普查\py3\临时_加载\tin_triangle.shp'
    fn_csv = r'E:\工作三\水旱普查\py3\临时_加载\zens.csv'
    zonal(fn_raster, fn_zones, fn_csv)
    shp_field_value(fn_csv, fn_zones)
    time2 = time.time()
    print((time2 - time1) / 3600.0)

