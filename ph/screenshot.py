import json

import requests
from requests import RequestException

from . import logger


def upload_screenshot(api_url, api_token, frame_path):
    global res
    logger.info("开始上传图床")
    print("开始上传图床")
    url = api_url

    # 判断frame_path为url还是本地路径
    if frame_path.startswith("http") or frame_path.startswith("https"):
        logger.info("输入一个在线图片链接")
        file_type = 'image/jpeg'
        # 请求文件拿到文件流
        try:
            res = requests.get(frame_path)
            logger.info("已成功获取文件流")
            print("已成功获取文件流")
        except RequestException as e:
            logger.error("请求过程中出现错误:" + str(e))
            print("请求过程中出现错误:", e)
            return False, {"请求过程中出现错误:" + str(e)}
        files = {'uploadedFile': (frame_path, res.content, file_type)}
    else:
        # Determine the MIME type based on file extension
        file_type = 'image/jpeg'  # default
        if frame_path.lower().endswith('.png'):
            file_type = 'image/png'
        elif frame_path.lower().endswith('.bmp'):
            file_type = 'image/bmp'
        elif frame_path.lower().endswith('.gif'):
            file_type = 'image/gif'
        elif frame_path.lower().endswith('.webp'):
            file_type = 'image/webp'

        # 打开文件，把文件流复制变量并关闭文件
        file_sterm = open(frame_path, 'rb')
        file_stream = file_sterm.read()
        file_sterm.close()

        files = {'uploadedFile': (frame_path, file_stream, file_type)}

    data = {'api_token': api_token, 'image_compress': 0, 'image_compress_level': 80}

    retry_count = 0
    while retry_count < 3:
        try:
            # 发送POST请求
            res = requests.post(url, data=data, files=files)
            logger.info("已成功发送上传图床的请求")
            print("已成功发送上传图床的请求")
            break  # 请求成功，跳出重试循环
        except RequestException as e:
            logger.error("请求过程中出现错误:" + str(e))
            print("请求过程中出现错误:", e)
            retry_count += 1
            if retry_count < 3:
                logger.info("进行第" + str(retry_count) + "次重试")
                print("进行第", retry_count, "次重试")
            else:
                logger.error("重试次数已用完")
                return False, {"请求过程中出现错误:" + str(e)}

    # 将响应文本转换为字典
    try:
        api_response = json.loads(res.text)
    except json.JSONDecodeError:
        logger.error("响应不是有效的JSON格式")
        print("响应不是有效的JSON格式")
        return False, {}

    # 返回完整的响应数据，以便进一步处理
    return True, api_response
