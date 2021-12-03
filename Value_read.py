def value(path):
    # 导入模块
    from dbfread import DBF
    import numpy as np

    # 数据表文件名
    table = DBF(path)
    shuzu = np.empty([100000, 4], dtype=float)
    m = 0
    for record in table:
        n = 0
        for field in record:
            shuzu[m, n] = record[field]
            n = n + 1
        m = m + 1
    return shuzu

# if __name__ == "__main__":
#     inshp = u'E:\\工作三\\水旱普查\\py3\\临时_加载\\tin_triangle.shp'
#     outputfile = u'E:\\工作三\\水旱普查\\py3\\临时_结果\\tin_triangle.shp'
#     copy(inshp, outputfile)