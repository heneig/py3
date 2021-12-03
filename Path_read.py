# coding: UTF-8
"""读取path路径下，特定类型的文件路径"""
import os


# 一、os.listdir()
# os.listdir()函数得到的是仅当前路径下的文件名，不包括子目录中的文件，所有需要使用递归的方法得到全部文件名。
# 直接给出代码，函数将返回类型为‘.jpeg’个文件名：

def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        elif os.path.splitext(file_path)[1] == '.tif':
            # 其中os.path.splitext()函数将路径拆分为文件名 + 扩展名，
            # 例如os.path.splitext(“E: / lena.jpg”)将得到”E: / lena“+".jpg"。
            list_name.append(file_path)
    return list_name


def listdir_name(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        elif os.path.splitext(file_path)[1] == '.tif':
            # 其中os.path.splitext()函数将路径拆分为文件名 + 扩展名，
            # 例如os.path.splitext(“E: / lena.jpg”)将得到”E: / lena“+".jpg"。
            list_name.append(file)
    return list_name


# 二、os.walk()
# 模块os中的walk()函数可以遍历文件夹下所有的文件。
# os.walk(top, topdown=Ture, onerror=None, followlinks=False)
# 该函数可以得到一个三元tupple(dirpath, dirnames, filenames).
# 参数含义：
# dirpath：string，代表目录的路径；
# dirnames：list，包含了当前dirpath路径下所有的子目录名字（不包含目录路径）；
# filenames：list，包含了当前dirpath路径下所有的非目录子文件的名字（不包含目录路径）。
# 注意，dirnames和filenames均不包含路径信息，如需完整路径，可使用os.path.join(dirpath, dirnames)

def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.shp':
                L.append(os.path.join(root, file))
                print(os.path.join(root, file))
    return L


# """调用"""
# list_name = []
# path = u'E:\\工作三\\水旱普查\\20211117\\Linxia\\1Linxiashi\\Plan 02'
# list_name = listdir(path, list_name)
# for LA in list_name:
#     print(LA)

# L = file_name(path)
# print(L)


"""******************************
             切片
    *****************************"""
# # -*- coding:utf-8 -*-
# """
# @author:lei
# """
# import os
#
# # os.path.join() 将分离的部分合成一个整体
# filename = os.path.join('/home/ubuntu/python_coding', 'split_func')
# print
# filename
# # 输出为：/home/ubuntu/python_coding/split_func
#
# # os.path.splitext()将文件名和扩展名分开
# fname, fename = os.path.splitext('/home/ubuntu/python_coding/split_func/split_function.py')
# print
# 'fname is:', fname
# print
# 'fename is:', fename
# # 输出为：
# # fname is:/home/ubuntu/python_coding/split_func/split_function
# # fename is:.py
#
# # os.path.split（）返回文件的路径和文件名
# dirname, filename = os.path.split('/home/ubuntu/python_coding/split_func/split_function.py')
# print
# dirname
# print
# filename
# # 输出为：
# # /home/ubuntu/python_coding/split_func
# # split_function.py
#
# # split（）函数
# # string.split(str="", num=string.count(str))[n]
# # str - - 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
# # num - - 分割次数。
# # [n] - - 选取的第n个分片
# string = "hello.world.python"
# print
# string.split('.')  # 输出为：['hello', 'world', 'python']
# print(string.split('.', 1))  # 输出为：['hello', 'world.python']
# print(string.split('.', 1)[0])  # 输出为：hello
# print(string.split('.', 1)[1])  # 输出为：world.python
# string2 = "hello<python.world>and<c++>end"
# print(string2.split("<", 2)[2].split(">")[0])  # 输出为：c++
