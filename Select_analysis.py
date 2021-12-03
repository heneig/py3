# - * - coding: utf-8 -
"""将一个shp文件按照某一要素属性分解为单一要素shp文件"""
"""从输入要素类或输入要素图层中提取要素（通常使用选择或结构化查询语言 (SQL) 表达式），并将其存储于输出要素类中。"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import arcpy

path = r"C:\Users\Administrator\Desktop\三区划分图\结果"
# 工作空间
arcpy.env.workspace = path
# 输入要素
inFc = "武威市.shp"
# 建立游标读取"shp"里的"area_name"字段信息
cursor = arcpy.SearchCursor("武威市.shp", fields="SQLX")

for row in cursor:                                            # 遍历字段
    city = row.getValue("SQLX")                          # 获取cityName字段信息
    outFc = path + '\\' + city + ".shp"                       # 导出的要素路径和名称
    # where_clause = '"NAME" = \'%s\''%(city)
    where_clause = '"SQLX"' + " = " + "'" + city + "'"   # 导出要素的条件，即根据不同cityName导出
    if arcpy.Exists(outFc):                                   # 判断是否已有相同名称的导出要素
        # (arcpy.Exists(outFc)== True)
        arcpy.Delete_management(outFc)                        # 删除有相同名称的要素
        arcpy.Select_analysis(inFc, outFc, where_clause)      # 根据条件导出要素
        print (u"成功导出：" + outFc)
    else:
        arcpy.Select_analysis(inFc, outFc, where_clause)      # 根据条件导出要素
        print (u"成功导出：" + outFc)