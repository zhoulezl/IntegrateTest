# 使用官方Python运行时作为父镜像  
FROM openeuler/openeuler:23.09
  
# 设置工作目录  
WORKDIR /app  
  
# 将当前目录下的文件复制到位于/app中的容器中  

  
# 安装JMeter  
RUN yum update -y
RUN yum install -y git
RUN git clone https://gitee.com/liuyu18801113053/open-api-auoto-test.git /app
RUN yum install -y java wget tar python3-pip
RUN wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
RUN tar -xzvf apache-jmeter-5.6.3.tgz && rm apache-jmeter-5.6.3.tgz 
RUN mv apache-jmeter-5.6.3 jmeter  
#
  
# 假设你的Python脚本需要某些Python库，使用pip安装  
RUN pip install -r /app/apiAutoTest/requirements.txt  
  
# 定义环境变量  
ENV PATH="/app/jmeter/bin:$PATH"

RUN useradd -u 1000 -m appuser  
RUN chown -R 1000:1000 /app/apiAutoTest/
USER appuser
# 当容器启动时，运行Python脚本  
CMD ["python3", "/app/apiAutoTest/app/send_email.py"]
