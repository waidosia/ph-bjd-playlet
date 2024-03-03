import json

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from ph.tool import get_settings
from util.log import logger

global token

proxies = {}

# 二次封装，把upload_screenshot函数封装成一个公共函数，在函数里调用不同的上传图床API
def upload_screenshot(api_url, api_token, frame_path):
    global proxies
    proxy = get_settings("proxyUrl")
    if proxy != '' or proxy is not None:
        logger.info(f'使用代理:{proxy}')
        proxies = {
            'http': proxy,
            'https': proxy
        }
    if "agsvpt" in api_url:
        logger.info("使用AGSV图床")
        return upload_agsv_screenshot(api_url, api_token, frame_path)
    elif "pterclub" in api_url:
        logger.info("使用猫图床")
        return chevereto_cookie_upload(api_url, api_token, frame_path)
    else:
        logger.error("未知图床")
        return False, {}


def upload_agsv_screenshot(api_url, api_token, frame_path):
    logger.info("开始上传图床")
    print("开始上传图床")
    url = api_url

    # 判断frame_path为url还是本地路径
    if frame_path.startswith("http") or frame_path.startswith("https"):
        logger.info("输入一个在线图片链接")
        file_type = 'image/jpeg'
        # 请求文件拿到文件流
        try:
            result = requests.get(frame_path)
            logger.info("已成功获取文件流")
            print("已成功获取文件流")
        except RequestException as e:
            logger.error("请求过程中出现错误:" + str(e))
            return False, {}
        files = {'uploadedFile': (frame_path, result.content, file_type)}
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
    res = None
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
                return False, {}
    # 将响应文本转换为字典
    print(res.text)
    try:
        api_response = json.loads(res.text)
    except json.JSONDecodeError:
        logger.error("响应不是有效的JSON格式")
        print("响应不是有效的JSON格式")
        return False, {}

    # 返回完整的响应数据，以便进一步处理
    return True, api_response


def get_token(api_url, api_token):
    global proxies
    global token
    if token:
        return token
    headers = {
        'cookie': api_token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.51 Safari/537.36'}
    try:
        response = requests.get(url=api_url, headers=headers, proxies=proxies, timeout=10)
    except Exception as r:
        logger.error(f'获取token失败，原因:{r}')
        return ''
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    for link in soup.find_all("a"):
        links = link.get("href")
        if 'auth_token' in links:
            token = links[links.find('auth_token') + 11:]
            return token
    return ''


def chevereto_cookie_upload(api_url, api_token, frame_path):
    global token
    global proxies
    token = ''
    auth_token = get_token(api_url, api_token)
    if auth_token == '':
        logger.error('未找到auth_token')
        return False, {}

    logger.info("开始上传图床")
    print("开始上传图床")

    # 判断frame_path为url还是本地路径
    if frame_path.startswith("http") or frame_path.startswith("https"):
        logger.info("输入一个在线图片链接")
        # 请求文件拿到文件流
        try:
            result = requests.get(frame_path)
            logger.info("已成功获取文件流")
            print("已成功获取文件流")
        except RequestException as e:
            logger.error("请求过程中出现错误:" + str(e))
            print("请求过程中出现错误:", e)
            return False, {}
        files = {'source': result.content}
    else:
        # 打开文件，把文件流复制变量并关闭文件
        file_sterm = open(frame_path, 'rb')
        file_stream = file_sterm.read()
        file_sterm.close()

        files = {'source': file_stream}

    headers = {'cookie': api_token}
    data = {'type': 'file', 'action': 'upload', 'nsfw': 0, 'auth_token': auth_token}

    try:
        req = requests.post(f'{api_url}/json', data=data, files=files, headers=headers, proxies=proxies)
        logger.info(req.text)
    except Exception as r:
        logger.error(f'requests 获取失败，原因: {r}')
        return False, {}
    try:
        res = req.json()
        logger.info(res)
    except json.decoder.JSONDecodeError:
        res = {}
    if not req.ok:
        logger.error(
            f"上传图片失败: HTTP {req.status_code}, reason: {req.reason} "
            f"{res['error'].get('message') if 'error' in res else ''}")
        return False, {}
    if 'error' in res:
        logger.error(
            f"上传图片失败: [{res['error'].get('code')}] {res['error'].get('context')} {res['error'].get('message')}")
        return {}
    if 'status_code' in res and res.get('status_code') != 200:
        logger.error(f"上传图片失败: [{res['status_code']}] {res.get('status_txt')}")
        return False, {}
    if 'image' not in res or 'url' not in res['image']:
        logger.error(f"图片直链获取失败")
        return False, {}
    return True, {"statusCode": str(res['status_code']), "bbsurl": "[img]" + res['image']['url'] + "[/img]"}
