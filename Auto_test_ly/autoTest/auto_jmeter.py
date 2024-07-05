import subprocess

# 指定JMeter的bin目录和JMX脚本路径D:/app/oneid.jtl
jmeter_bin = "D:/apache-jmeter-5.6.3/bin/"
jmx_script = "D:/PY_pros/pythonProject/autoTest/maoyan.jmx"

# 使用subprocess模块调用JMeter命令行执行JMX脚本
cmd = f"{jmeter_bin}jmeter -n -t {jmx_script}"
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# 打印执行结果
if process.returncode == 0:
    print("JMeter脚本执行成功")
    print(output.decode(encoding='gbk'))
else:
    print("JMeter脚本执行失败")
    print(error.decode(encoding='gbk'))