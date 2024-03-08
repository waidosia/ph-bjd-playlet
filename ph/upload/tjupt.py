import os
import time
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
from util.log import logger

proxies = {}


def get_tjupt(cookies_str) -> (bool, str):
    global proxies
    headers = {
        'Host': 'tjupt.org',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://tjupt.org/torrents.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        logger.info('开始获取北洋主页')
        response = requests.get('https://tjupt.org/index.php', headers=headers, timeout=10, allow_redirects=False)
        if response.status_code == 200:
            logger.info('获取主页成功')
            return True, response.text
        elif response.status_code == 302:
            # 判断是否重定向到登录页面
            if 'login.php' in response.headers['Location']:
                logger.info('cookie过期')
                return False, 'cookie过期'
            else:
                logger.info(f'获取主页失败,重定向地址为:{response.headers["Location"]}')
                return False, f'获取主页失败,重定向地址为:{response.headers["Location"]}'
        else:
            logger.info(f'获取主页失败,状态码为:{response.status_code}')
            return False, f'获取主页失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.error(f'获取主页失败{e}')
        return False, '获取主页失败'


def upload_tjupt(cookies_str, torrent_file, main_title, compose, descr, chinese_name, proxy, torrent_path) -> (
        bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_tjupt(cookies_str)
    if not get_success:
        return False, get_str, ""
    global proxies
    if proxy != '' or proxy is not None:
        logger.info(f'使用代理:{proxy}')
        proxies = {
            'http': proxy,
            'https': proxy
        }
    headers = {
        'Host': 'tjupt.org',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://tjupt.org/upload.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',

    }
    try:
        file = open(torrent_file, 'rb').read()
    except Exception as e:
        logger.info(f'打开种子文件失败{e}')
        return False, '打开种子文件失败，请检查是否制作种子', ""

    data = {
        'referid': '',
        'type': '402',
        'cname': chinese_name,
        'ename': main_title,
        'specificcat': '大陆',
        'small_descr': compose,
        'descr': descr,
        'uplver': 'yes',
        'internal_team': 'yes',
        'exclusive': 'yes',
    }
    # 验证一下，文件名带后缀，且去掉前面的路径
    filename = os.path.basename(torrent_file)
    files = {'file': (filename, file, 'application/x-bittorrent')}

    try:
        response = requests.request("POST", 'https://tjupt.org/takeupload.php', headers=headers,
                                    data=data, files=files, allow_redirects=False,
                                    timeout=10)
        if response.status_code == 302:
            # 正常的重定向
            logger.info('发布成功,尝试获取种子id')
            # 提取重定向后的地址
            redirect_url = response.headers['Location']
            # details.php?id=399109&uploaded=1
            if 'details.php' in redirect_url:
                torrent_id = redirect_url.split('id=')[1].split('&')[0]
                logger.info(f'获取种子id成功:{torrent_id}')
                time.sleep(1)
                get_success, torrent_link, torrent_save_path = get_tjupt_torrent(cookies_str, torrent_id, torrent_path)
                return get_success, torrent_link, torrent_save_path
        else:
            logger.info(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}', ""

    except Exception as e:
        logger.info(f'发布失败,错误原因为{e}')
        return False, '发布失败', ""


def get_tjupt_torrent(cookies_str, torrent_id, torrent_path) -> (bool, str):
    global proxies
    headers = {
        'Host': 'tjupt.org',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://tjupt.org/upload.php',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    save_path = ""
    if torrent_path != '' and torrent_path is not None and torrent_path != 'None':
        try:
            response = requests.get(f'https://tjupt.org/download.php?id={torrent_id}', headers=headers, timeout=10,
                                    proxies=proxies)
            if response.status_code == 200:
                # 提取文件名
                filename = response.headers['Content-Disposition'].split('filename=')[1].split(';')[0].replace('"', '')
                decoded_filename = filename.encode('latin-1').decode('utf-8')
                # 处理url编码的问题
                decoded_filename = unquote(decoded_filename)
                # 下载种子
                save_path = f'{torrent_path}/{decoded_filename}'
                with open(f'{torrent_path}/{decoded_filename}', 'wb') as f:
                    f.write(response.content)
                logger.info(f'下载种子成功{filename}')
            else:
                logger.error(f'下载种子失败,状态码为:{response.status_code}')
                return False, f'下载种子失败,状态码为:{response.status_code}', ""
        except Exception as e:
            logger.exception(f'下载种子失败{e}')
            return False, '下载种子失败', ""
    try:
        response = requests.get(f'https://tjupt.org/details.php?id={torrent_id}', headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            soup = BeautifulSoup(response.text, 'html.parser')
            torrent_url = soup.find('a', {'id': 'direct_link'}).get('href')
            logger.info(f'获取种子下载地址成功{torrent_url}')
            return True, torrent_url, save_path
        else:
            logger.info(f'获取种子下载地址失败,状态码为:{response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:', response.status_code, ""
    except Exception as e:
        logger.error(f'获取种子下载地址失败:{e}')
        return False, '获取种子下载地址失败', ""
