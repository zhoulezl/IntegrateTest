import logging
import subprocess
import time



def data_create(config):
    date = time.localtime()
    date_name = fr'{date.tm_year}{date.tm_mon:02}{date.tm_mday:02}'
    config = config

    jmx_list = config.get("'DEFAULT'", "'data_dict_key'").split(',')
    for dic in jmx_list:
        with open(dic+date_name+'.jtl', 'w') as f:
            print(dic+date_name+'.jtl','文件创建完成')
        with open(dic+date_name+'.xml', 'w') as f:
            print(dic + date_name + '.xml', '文件创建完成')
    error_count = 1

    # 指定JMeter的bin目录和JMX脚本路径D:/app/oneid.jtl
    jmeter_bin = config.get("'DEFAULT'", "'jmeter_bin'")
    jmx_script = config.get("'DEFAULT'", "'jmx_script'").split(',')
    print("需要执行的全部脚本：",jmx_script)
    for jmx in jmx_script:
        filename = jmx

        with open(filename, 'r', encoding='utf-8') as f:
            f_content = f.read()
            f_content = f_content.replace('\n', '').replace('a.jtl',date_name+'.jtl')
            f_content = f_content.replace('\n', '').replace('b.xml', date_name+'.xml')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f_content)
        cmd = f"{jmeter_bin}jmeter -n -t {jmx}"
        print("当前执行脚本是：",jmx)
        print(cmd)
        while error_count <= 2:
            # 使用subprocess模块调用JMeter命令行执行JMX脚本
            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()
                # 打印执行结果
                if process.returncode == 0:
                    logging.info('执行成功')
                    break
                else:
                    logging.info('执行失败')
            except Exception as e:
                error_count += 1
                logging.info('e:',e)
                logging.info('执行失败重试')
                continue
            finally:

                if error_count>2:
                    logging.info('重试次数过多，跳过')
