from configparser import ConfigParser
import os
import yaml

class YamlHandler:
    def __init__(self, file):
        self.file = file

    def read_yaml(self, encoding='utf-8'):
        """读取yaml数据"""
        with open(self.file, encoding=encoding) as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)


if __name__ == '__main__':
    # 读取config.yaml配置文件数据
    read_data = YamlHandler('./config/config.yaml').read_yaml()
    print(read_data)
