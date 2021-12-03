# -*- coding: utf-8 -*-
import os
import arcpy
from arcpy import env
from arcpy.sa import *
from Delete_file import *
from Path_read import *
from ProjectRaster import *
from xpinyin import Pinyin
from Copy_shp import *
from Value_read import *
from osgeo import ogr


p = Pinyin()

TianShui = ['武山县', '清水县', '甘谷县', '秦安县', '秦州区', '麦积区', '张家川回族自治县']
LinXia = ['临夏市']#, '临夏县', '康乐县', '永靖县', '广河县', '和政县', '东乡县', '积石山县']
WuWei = ['古浪县', '天祝藏族自治县', '民勤县', '凉州区']

# 文件路径
out_path = u'E:\\工作三\\水旱普查\\py3\\临时_结果'
temp_path = u'E:\\工作三\\水旱普查\\py3\\临时_加载'
Shp = u'E:\\工作三\\水旱普查\\风险普查行政区划边界（省市县）20210616\\县区界'
Tiff = u"E:\\工作三\\水旱普查\\20211117\\Linxia"

m = 0
for line in LinXia:
    m = m + 1
    # 定义工作空间
    env.workspace = temp_path

    # 清空工作文件夹
    setDir(temp_path)

    # 检查扩展
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension('Spatial')

    # 投影转换
    city = p.get_pinyin(line.strip(), '')
    img_path = Tiff + '\\' + str(m) + city + '\\Plan 02'
    list_name = []
    list_name = listdir(img_path, list_name)
    for img in list_name:
        proj_data(img, temp_path)

    # 栅格转tin ：tin转三角网
    arcpy.RasterTin_3d('Depth (100).tif1.tif', "tin", "#", "#", "10")
    arcpy.TinTriangle_3d("tin", "tin_triangle.shp", "DEGREE", 1, "#", "#")

    list_name = []
    list_name = listdir(temp_path, list_name)
    for tif in list_name:
        # 以表格显示分区统计
        tif_ = tif.replace(' (', '_')
        tif_ = tif_.replace(')', '')
        outZSaT = ZonalStatisticsAsTable("tin_triangle.shp", "FID", tif,
                                         tif_.split('.tif1.tif')[0]+'.dbf', "NODATA", "MAXIMUM")

    list = ['风险_5.shp', '风险_10.shp', '风险_20.shp', '风险_50.shp', '风险_100.shp']
    for shp in list:
        copy(temp_path+"\\"+"tin_triangle.shp", out_path+"\\"+line.strip() + shp)
        arcpy.AddField_management(out_path+"\\"+line.strip() + shp, "Depth", 'FLOAT', "", "", '50')
        arcpy.AddField_management(out_path+"\\"+line.strip() + shp, "Velocity", 'FLOAT', "", "", '50')
        arcpy.AddField_management(out_path+"\\"+line.strip() + shp, "WSE", 'FLOAT', "", "", '50')

        driver = ogr.GetDriverByName('ESRI Shapefile')
        datasource = driver.Open(out_path+"\\"+line.strip() + shp, 1)
        layer = datasource.GetLayer(0)

        list_name = []
        list_name = listdir_name(temp_path, list_name)
        for file in list_name:
            file_ = file.replace(' (', '_')
            file_ = file_.replace(')', '')
            if file_.split('_')[0] == "Depth" and file_.split('_')[1].split('.')[0] == shp.split('_')[1].split('.')[0]:
                shuzu = value(temp_path+"\\"+file_.split('.')[0]+".dbf")
                for i in range(layer.GetFeatureCount()):
                    feat = layer.GetFeature(i)
                    feat.SetField('Depth', shuzu[i, 3])
                    layer.SetFeature(feat)
                    layer.ResetReading()
            if file_.split('_')[0] == "Velocity" and file_.split('_')[1].split('.')[0] == shp.split('_')[1].split('.')[0]:
                shuzu = value(temp_path+"\\"+file_.split('.')[0]+".dbf")
                for i in range(layer.GetFeatureCount()):
                    feat = layer.GetFeature(i)
                    feat.SetField('Velocity', shuzu[i,3])
                    layer.SetFeature(feat)
                    layer.ResetReading()
            if file_.split('_')[0] == "WSE" and file_.split('_')[1].split('.')[0] == shp.split('_')[1].split('.')[0]:
                shuzu = value(temp_path+"\\"+file_.split('.')[0]+".dbf")
                for i in range(layer.GetFeatureCount()):
                    feat = layer.GetFeature(i)
                    feat.SetField('WSE', shuzu[i,3])
                    layer.SetFeature(feat)
                    layer.ResetReading()









# arcpy.CopyRaster_management(out_path, img_proj_out_tif, "DEFAULTS", "", "", "", "", "")

# del_file(u'C:\\Users\\Administrator\\Desktop\\三区划分图\\结果')

# LinXia = ['东乡族自治县', '广河县', '和政县', '积石山保安族东乡族撒拉族自治县', '康乐县', '永靖县', '临夏县', '临夏市']
#

# arcpy.ProjectRaster_management("c:/data/image.tif", "c:/output/reproject.tif",\
#                                "World_Mercator.prj", "BILINEAR", "5",\
#                                "NAD_1983_To_WGS_1984_5", "#", "#")


# for line in LinXia:
#     line.strip()
#     BOUA_path = u'C:\\Users\\Administrator\\Desktop\\三区划分图\\县区界' + '\\' + line.strip() + '.shp'
#     River_path = u'C:\\Users\\Administrator\\Desktop\\流域裁剪\\天水裁剪-11.26\\Watershed_1127.shp'
#     out_path = u'C:\\Users\\Administrator\\Desktop\\三区划分图\\结果' + '\\' + line.strip()
#     tem_path = u'C:\\Users\\Administrator\\Desktop\\三区划分图\\临时'
#
#     Dissolve = tem_path + r'\Dissolve.shp'
#     Clip = tem_path + r'\Clip.shp'
#     Erase = tem_path + r'\Erase.shp'
#     Merge = tem_path + r'\Merge.shp'
#
#     del_file(tem_path)
#     # # run the tool
#     GCS = arcpy.SpatialReference(r'C:\Users\Administrator\Desktop\三区划分图\GCS.prj')
#     arcpy.Project_management(River_path, tem_path + '\\' + 'river', GCS)  # tem_path+'\\'+line.strip()+'.shp'
#     # # 融合
#     # arcpy.Dissolve_management(BOUA_path, Dissolve)
#     # 裁剪
#     arcpy.Clip_analysis(River_path, BOUA_path, Clip)
#     # 擦除
#     arcpy.Erase_analysis(BOUA_path, Clip, Erase, '#')
#     # 合并
#     arcpy.Merge_management([Clip, Erase], Merge)
#
#     # 转换坐标系
#     # create a spatial reference object for the output coordinate system
#     PCS = arcpy.SpatialReference(r'C:\Users\Administrator\Desktop\三区划分图\PCS.prj')
#     # run the tool
#     arcpy.Project_management(Merge, out_path, PCS)
#
#     # 修改前后字段名对照属性字典
#     modifyDic = {"XH": ["XH", 'Short', "100", "10"],  # 错误字段名：[正确字段名，长度]
#                  "SQLX": ["SQLX", 'TEXT', "100", "10"],
#                  "MJ": ["MJ", 'Float', "100", "50"],
#                  "BZ": ["BZ", 'TEXT', "100", "100"]}
#
#     for Attributes in modifyDic:
#         # Process: 添加字段
#         arcpy.AddField_management(out_path + '.shp', modifyDic[Attributes][0], modifyDic[Attributes][1], "", "",
#                                   modifyDic[Attributes][3])
#     arcpy.CalculateField_management(out_path + '.shp', "MJ", "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
#     arcpy.DeleteField_management(out_path + '.shp', ["OBJECTID", "Shape_Leng", "Shape_Area", 'area_code', 'area_name'])
