# -*- coding: utf-8 -*-
"""在Pycharm中设置arcpy库的运行条件"""


def arcpy_Set():
    """设置arcpy库运行条件"""
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')  # 设置默认编码格式为'utf-8'
    arcpy_path = [r'G:\install\ArcGIS\Desktop10.7\ArcGIS10.2\Lib\site-packages',
                  r'G:\install\ArcGIS\Desktop10.7\arcpy',
                  r'G:\install\ArcGIS\Desktop10.7\bin',
                  r'G:\install\ArcGIS\Desktop10.7\ArcToolbox\Scripts']  # 修改成Arcgis安装对应路径
    sys.path.extend(arcpy_path)
