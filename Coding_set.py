# coding=utf-8
"""修改编码方式，读取中文"""

# 方法一：
# 在代码开头处声明Python使用UTF-8编码显示字符，这样就可以显示中文了。代码如下：
# #coding: UTF-8


# 方法二： 在中文字符前面加 u, 例如：print  u"我是中文"。加U的作用就是要以UTF-8的形式显示中文，这样就不会出现乱码。


# 方法三：
# import sys
# reload(sys)  # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
# sys.setdefaultencoding('utf-8')


# 方法四：遇到需要处理中文的地方，就随时进行UTF-8编码。
# 经常会遇到的是，进行了第一步和第二步设置后，还是无法正常显示和处理中文字符，这时也只能随用随编码了。
# 假设待处理字符串为string
# 使用下面的语句进行utf-8编码：

def encode_utf8(string):
    return string.encode('utf-8')


def decode_utf8(string):
    return unicode(string, encoding='utf-8')


"""编码问题"""
# 最近处理中文数据，python2各种编码问题，看了好多博客和文章，终于弄懂了一些，所以在这里总结一发。供大家学习和参考！
# 1.编码
# （1）ASCII码
# ASCII码是规定的最早的计算机系统将英文文字转为数字存储的编码方式，一共规定了128个字符的编码，即7个bit。而1byte=8bit，
# 所以占一个字节的ASCII码的最高位（没用到）为0。
#
# （2）Unicode
# 由于ASCII码只包含了大小写英文字母、数字和一些符号，如果用来表示其他语言，那么是不行的。因此产生了一些非ASCII编码方式。
# 简体中文常见的编码方式是GB2312，使用两个字节表示一个汉字，所以理论上最多可以表示256x256=65536个符号。但是每个地方的
# 编码标准都不一样，如何统一呢？Unicode就出现了。
# Unicode叫做万国码，采用32位二进制(4字节)表示一个字符。但是需要注意的是，Unicode只是一个符号集(指定字符到二进制数之间的对应关系)，
# 它只规定了符号的二进制代码，却没有规定这个二进制代码应该如何存储。
#
# （3）UTF-8
# Unicode的实现方式有很多种，比如
#
# UTF-8 ：(变长的编码方式,可以使用2~4个字节表示一个符号，根据不同的符号而变化字节长度）
# UTF-16：(变长的编码方式,可以使用2~4个字节表示一个符号，根据不同的符号而变化字节长度）
# UTF-32：(每个字符固定占4字节)
# 而UTF-8（8-bit Unicode Transformation Format）是在互联网上使用最广的一种Unicode的实现方式。
#
# 2.Python 编码
# python2默认以ASCII编码，但是在实际编码过程中，我们会用到很多中文，为了不使包含中文的程序报错，也是为了符合国际通用惯例，一般将我们的
# 文件编码设置为utf-8格式。
# 如何设置：一般在文件开头声明
#
#  # -*- coding:utf-8 -*-
# 1
# Python中有两个常用的由basestring派生出来的表示字符串的类型：str, unicode。
# 其中，str类似于C中的字符数组或者Java中的byte数组。
# 对于unicode类型，Python在内存中存储和使用的时候是按照UTF-8方式，在代码中的表示为字符串前加u。
#
# 而unicode与str之间的转换，则用到了encode和deocde方法。
# decode解码：表示将一个(str)字符串按照给定的编码解析为unicode类型，encode编码：表示将一个unicode字符串按照指定编码解析为字节数组(str)
#
# 3.sys.setdefaultencoding(‘utf-8’) 问题
# 为什么我们有时候遇到编码问题时，还经常看到一种解决方式reload（sys），sys.setdefaultencoding(‘utf-8’) ？
#
# 这里我看到一篇博客，讲的挺好的，在这里谢谢这位仁兄，我复制粘贴过来供大家膜拜：
# python中sys.setdefaultencoding(‘utf-8’)的作用
#
# 若str对象调用encode会默认先按系统默认编码方式 decode成unicode对象再encode，忽视了中间默认的decode往往导致报错。
# 比如有如下代码：
#
# 　　# -*- coding: utf-8 -*-
# 　　s = '中文字符'  # 这里的 str 是 str 类型的，而不是 unicode
# 　　s.encode('gb2312')
#
# 这句代码将 s 重新编码为 gb2312 的格式，即进行 unicode -> str 的转换。因为 s 本身就是 str 类型的，因此
# Python 会自动的先将 s 解码为 unicode ，然后再编码成 gb2312。因为解码是python自动进行的，我们没有指明解码方式，python 就会使用
# sys.defaultencoding 指明的方式来解码。很多情况下 sys.defaultencoding为ANSCII，如果 s 不是这个类型就会出错。
#
# UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position
# 　　0: ordinal not in range(128)
#
# 对于这种情况，我们有两种方法来改正错误：
# （1）明确的指示出 s 的编码方式
#
# 　#! /usr/bin/env python
# 　　# -*- coding: utf-8 -*-
# 　　s = '中文字符'
# 　　s.decode('utf-8').encode('gb2312')
#
# （2）更改 sys.defaultencoding 为文件的编码方式
#
# 　　# -*- coding: utf-8 -*-
# 　　import sys
# 　　reload(sys) # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
# 　　sys.setdefaultencoding('utf-8')
#
# 　　str = '中文字符'
# 　　str.encode('gb2312')
#
# 总结：
# 1. 编码问题在python2中还是挺麻烦的，尤其是处理中文，里面的坑大概我都遇到过了。我建议一上来先加coding那句话，顺带把reload也加上吧。这样避免
# 之后程序报错又重新来找问题。（我也有看到文章说reload(sys)似乎并不是很好，我觉得其实最好的办法是我们都换python3 吧^_^）
#
# 2. 搞懂Unicode和UTF-8之间的关系（只是实现方式）。
#
# 3. 搞懂 python中编码encode和解码decode是在干什么。str到unicode为解码，unicode到str为编码。如果某种str到另一种str，其中会先用系统
# 默认方式decode解码，再encode编码。
# 参考博客：
# 阮一峰-字符编码笔记：ASCII，Unicode和UTF-8
# （写的很赞啊！我的很多地方都是看了他的博客弄懂的）
# 聊一聊 Python 2 中的编码
# 这篇文章encode，decode写的很清楚呀~而且也非常通俗易懂，膜拜大佬~
# ————————————————
# 版权声明：本文为CSDN博主「up酱」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/danlei94/article/details/77116984
