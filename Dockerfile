FROM registry.cn-shanghai.aliyuncs.com/devcon/spiderdev:v3.0
ADD . /app
WORKDIR /app
RUN mkdir /app/log
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]