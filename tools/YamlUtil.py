import  os
import yaml

from configs.conf import *

class YamlReaber:
                                                        #先初始化；文件是否存在
    def __init__(self,yamlfile):                        #yamlfile 文件名
        if os.path.exists(yamlfile):                    #判断yamlfile文件是否存在； os.path.exists 文件存不存在
            self.yamlfile =yamlfile                     #存在赋值给 self.yamlfile
        else:
            print(yamlfile)
            raise FileNotFoundError("文件不存在")       #不存在就是提示
        self._data = None
        self._data_all = None

    def data(self):
        """
        读取单个文档
        yaml文件名称在初始化中
        :return: yaml文件中的所有内容
        """
        if not self._data:                          #如果_all不为空,直接返回之前保存的数据
            with open(self.yamlfile,"rb") as f:     #打开文件
                #print(f)
                self._data = yaml.safe_load(f)      #使用yaml方法读取;方法safe_load() 读取单个文档；
        return  self._data

    def data_all(self):
        """
        读取多个文档
         yaml文件名称在初始化中
        :return: yaml文件中的所有内容
        """
        if not self._data_all:                                #如果_all不为空,直接返回之前保存的数据
            with open(self.yamlfile,"rb") as f:              #打开文件
                self._data_all = list(yaml.safe_load_all(f))  #使用yaml方法读取;多个文档则用safe_load_all()
        return  self._data_all


def Yaml_file_pathS(Yaml_name, filePath="configs"):
    """
    :param Yaml_name：yaml的文件夹名称
    :param filePath: 默认configs文件夹下
    :return: 返回当前yaml文件的绝对路径+文件名称
    """
    _config_path = BASE_DIR +os.sep+filePath
    return _config_path +os.sep+Yaml_name


def Yaml_read(yaml_name="conf.yaml", level_1=None, level_2=None, filePath=None, location=None):
    """
    支持yaml的单文档、多文档遍历
    :param yaml_name:  yaml的文件名称
    :param level_1: yaml文件第一级的名称
    :param level_2: yaml文件第二级的名称
    :param filePath:文件夹名称
    :param location:读取多个文档的下标
    :return:   1、支持返回所有的yaml文件；2、第一级下的所有数据；3、固定某位置的值
    """
    if filePath!=None:
        if location!=None:
            login = tools.YamlUtil.YamlReaber(Yaml_file_pathS(yaml_name,filePath)).data_all()
        else:
            login = tools.YamlUtil.YamlReaber(Yaml_file_pathS(yaml_name,filePath)).data()
    else:
        if location!=None:
            login = tools.YamlUtil.YamlReaber(Yaml_file_pathS(yaml_name)).data_all()
        else:
            # print(yaml_name)
            # print(Yaml_file_pathS(yaml_name))
            login = tools.YamlUtil.YamlReaber(Yaml_file_pathS(yaml_name)).data()
    if level_1==None and level_2==None:
        if location!=None:
            return  login[location]
        else:
            return  login
    elif level_1!= None and level_2==None:
        if location!=None:
            return  login[location][level_1]
        else:
            return  login[level_1]
    elif level_1!=None and level_2!=None:
        if location!=None:
            return  login[location][level_1][level_2]
        else:
            return login[level_1][level_2]


if __name__ == '__main__':
    print(Yaml_read("test.yaml", location=False))

