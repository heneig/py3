# -*- coding: utf-8 -*-
import os
from Delete_file import *

import arcpy

del_file(u'C:\\Users\\Administrator\\Desktop\\三区划分图\\结果')

TianShui = ['天水市']  # ['武山县', '清水县', '甘谷县', '秦安县', '秦州区', '麦积区', '张家川回族自治县']
LinXia = ['临夏回族自治州']  # ['东乡族自治县', '广河县', '和政县', '积石山保安族东乡族撒拉族自治县', '康乐县', '永靖县', '临夏县', '临夏市']
WuWei = ['武威市']  # ['古浪县', '天祝藏族自治县', '民勤县', '凉州区']
for line in WuWei:
    line.strip()
    BOUA_path = u'C:\\Users\\Administrator\\Desktop\\三区划分图\\市界' + '\\' + line.strip() + '.shp'
    River_path = u'C:\\Users\\Administrator\\Desktop\\三区划分图\\流域裁剪\\武威裁剪-11.26\\Watershed.shp'
    out_path = u'C:\\Users\\Administrator\\Desktop\\三区划分图\\结果' + '\\' + line.strip()
    tem_path = u'C:\\Users\\Administrator\\Desktop\\三区划分图\\临时'

    Dissolve = tem_path + r'\Dissolve.shp'
    Clip = tem_path + r'\Clip.shp'
    Erase = tem_path + r'\Erase.shp'
    Merge = tem_path + r'\Merge.shp'

    del_file(tem_path)
    # # run the tool
    # GCS = arcpy.SpatialReference(r'C:\Users\Administrator\Desktop\三区划分图\GCS.prj')
    # arcpy.Project_management(River_path, tem_path + '\\' + 'river', GCS)  # tem_path+'\\'+line.strip()+'.shp'
    # # 融合
    # arcpy.Dissolve_management(BOUA_path, Dissolve)
    # 裁剪
    arcpy.Clip_analysis(River_path, BOUA_path, Clip)
    # 擦除
    arcpy.Erase_analysis(BOUA_path, Clip, Erase, '#')
    # 合并
    arcpy.Merge_management([Clip, Erase], Merge)

    # 转换坐标系
    # create a spatial reference object for the output coordinate system
    PCS = arcpy.SpatialReference(r'C:\Users\Administrator\Desktop\三区划分图\PCS.prj')
    # run the tool
    arcpy.Project_management(Merge, out_path, PCS)

    # 修改前后字段名对照属性字典
    modifyDic = {"XH": ["XH", 'Short', "100", "10"],  # 错误字段名：[正确字段名，长度]
                 "SQLX": ["SQLX", 'TEXT', "100", "10"],
                 "MJ": ["MJ", 'Float', "100", "50"],
                 "BZ": ["BZ", 'TEXT', "100", "100"]}

    for Attributes in modifyDic:
        # Process: 添加字段
        arcpy.AddField_management(out_path + '.shp', modifyDic[Attributes][0], modifyDic[Attributes][1], "", "",
                                  modifyDic[Attributes][3])
    arcpy.CalculateField_management(out_path + '.shp', "MJ", "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
    arcpy.DeleteField_management(out_path + '.shp', ["OBJECTID", "Shape_Leng", "Shape_Area", 'area_code'])
