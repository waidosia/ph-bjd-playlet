import logging

# 创建全局日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_file = 'playlet.log'  # 指定日志文件路径
handler = logging.FileHandler(log_file, encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 将日志处理器添加到日志记录器
logger.addHandler(handler)
