# -*- coding: utf-8 -*-


def del_file(path):
    """删除path路径下所有文件"""
    # import sys
    # reload(sys)
    # sys.setdefaultencoding('utf8')  # 设置默认编码格式为'utf-8'
    import os
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def setDir(filepath):
    import os
    import shutil
    '''
    如果文件夹不存在就创建，如果文件存在就清空！
    :param filepath:需要创建的文件夹路径
    :return:
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)


# if __name__ == "__main__":
#     filepath = r"E:\工作三\水旱普查\py3\临时_加载"
#     setDir(filepath)
