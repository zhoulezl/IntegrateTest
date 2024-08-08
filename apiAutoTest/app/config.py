from configparser import ConfigParser
import os

def config_read():
    # for root, dirs, files in os.walk('/home'):
    #     level = root.replace('/home', '').count(os.sep)
    #     indent = ' ' * 4 * (level)
    #     print('{}{}/'.format(indent, os.path.basename(root)))
    #     subindent = ' ' * 4 * (level + 1)
    #     for f in files:
    #         print('{}{}'.format(subindent, f))
    config = ConfigParser()
    # 读取配置文件
    config.read('/vault/secrets/mail.yml', encoding='utf-8')
    # 获取邮箱部分的配置
    #print(config.sections())
    os.remove('/vault/secrets/mail.yml')
    return config
