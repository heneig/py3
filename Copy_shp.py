def copy(inshp, outputfile):
    from osgeo import ogr
    import os

    ds = ogr.Open(inshp)
    driver = ogr.GetDriverByName("ESRI Shapefile")

    if os.access(outputfile, os.F_OK):
        driver.DeleteDataSource(outputfile)
    pt_cp = driver.CopyDataSource(ds, outputfile)
    pt_cp.Release()


# if __name__ == "__main__":
#     inshp = u'E:\\工作三\\水旱普查\\py3\\临时_加载\\tin_triangle.shp'
#     outputfile = u'E:\\工作三\\水旱普查\\py3\\临时_结果\\tin_triangle.shp'
#     copy(inshp, outputfile)
