import logging
# 创建全局日志记录器
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_file = 'playlet.log'  # 指定日志文件路径
handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 将日志处理器添加到日志记录器
logger.addHandler(handler)