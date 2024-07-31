import subprocess
from configparser import ConfigParser


def data_create():
    error_count = 0
    config = ConfigParser()
    # 读取配置文件
    config.read('config.ini')
    # 指定JMeter的bin目录和JMX脚本路径D:/app/oneid.jtl
    jmeter_bin = config.get('DEFAULT', 'jmeter_bin')
    jmx_script = config.get('DEFAULT', 'jmx_script')
    cmd = f"{jmeter_bin}jmeter -n -t {jmx_script}"
    while error_count <= 10:
        # 使用subprocess模块调用JMeter命令行执行JMX脚本
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            # 打印执行结果
            if process.returncode == 0:
                break
            else:
                error_count += 1
        except Exception as e:
            pass
