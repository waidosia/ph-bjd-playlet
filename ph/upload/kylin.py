import os
import time
from lxml import etree

import requests
from util.log import logger

kylin_year_map = {
    '2022': '2',
    '2023': '1',
    '2024': '10'
}

kylin_resolution_map = {
    '480P': '8',
    '720P': '3',
    '1080P': '1',
    '4K': '6',
}

proxies = {}


def get_kylin(cookies_str) -> (bool, str):
    global proxies
    headers = {
        'Host': 'www.hdkyl.in',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://www.hdkyl.in/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get('https://www.hdkyl.in/index.php', headers=headers, timeout=10, allow_redirects=False,
                                proxies=proxies)
        if response.status_code == 200:
            logger.info('获取主页成功')
            return True, response.text
        elif response.status_code == 302:
            # 判断是否重定向到登录页面
            if 'login.php' in response.headers['Location']:
                logger.error('cookie过期')
                return False, 'cookie过期'
            else:
                logger.error(f'获取主页失败,重定向地址为:{response.headers["Location"]}')
                return False, f'获取主页失败,重定向地址为:{response.headers["Location"]}'
        else:
            logger.error(f'获取主页失败,状态码为:{response.status_code}')
            return False, f'获取主页失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.error(f'获取主页失败{e}')
        return False, '获取主页失败'


def upload_kylin(cookies_str, torrent_file, main_title, compose, descr, year, proxy, torrent_path) -> (bool, str):
    global proxies
    if proxy != '' or proxy is not None:
        logger.info(f'使用代理:{proxy}')
        proxies = {
            'http': proxy,
            'https': proxy
        }
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_kylin(cookies_str)
    if not get_success:
        return False, get_str, ""
    headers = {
        'Host': 'www.hdkyl.in',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://www.hdkyl.in/upload.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Origin': 'https://www.hdkyl.in',

    }
    try:
        file = open(torrent_file, 'rb').read()
    except Exception as e:
        logger.error(f'打开种子文件失败{e}')
        return False, '打开种子文件失败，请检查是否制作种子', ""

    # 从主标题中提取分辨率
    if len(main_title.split(' ')) > 6:
        resolution = main_title.split(' ')[-4].upper()
    else:
        return False, '主标题格式错误,无法正确获取分辨率或年', ""

    data = {
        'name': main_title,
        'small_descr': compose,
        'descr': descr,
        'color': '0',
        'font': '0',
        'size': '0',
        # 类型 短剧
        'type': '421',
        # 年代
        'processing_sel[4]': kylin_year_map.get(year, '0'),
        # 媒介 web_dl
        'medium_sel[4]': '31',
        # 视频编码 h.264
        'codec_sel[4]': '1',
        # 音频编码 aac
        'audiocodec_sel[4]': '6',
        # 分辨率
        'standard_sel[4]': kylin_resolution_map.get(resolution, '0'),
        # 地区 中国
        'source_sel[4]': '15',
        # 制作组
        'team_sel[4]': '9',
        # 标签
        'tags[4][]': [1, 5, 6, 15],
        # 匿名发布
        'uplver': 'yes',
    }
    # 验证一下，文件名带后缀，且去掉前面的路径
    filename = os.path.basename(torrent_file)
    files = {'file': (filename, file, 'application/x-bittorrent')}

    try:
        response = requests.request("POST", 'https://www.hdkyl.in/takeupload.php', headers=headers,
                                    data=data, files=files, allow_redirects=False,
                                    timeout=10, proxies=proxies)
        if response.status_code == 302:
            # 正常的重定向
            # 提取重定向后的地址
            redirect_url = response.headers['Location']
            torrent_id = redirect_url.split('id=')[1].split('&')[0]
            time.sleep(1)
            get_success, torrent_link, torrent_save_path = get_kylin_torrent(cookies_str, torrent_id, torrent_path)
            return get_success, torrent_link, torrent_save_path
        else:
            logger.error(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}', ""

    except Exception as e:
        logger.error(f'发布失败{e}')
        return False, '发布失败', ""


def get_kylin_torrent(cookies_str, torrent_id, torrent_path) -> (bool, str, str):
    global proxies
    headers = {
        'Host': 'www.hdkyl.in',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://www.hdkyl.in/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get(f'https://www.hdkyl.in/details.php?id={torrent_id}', headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            html = response.text
            tree = etree.HTML(html, etree.HTMLParser())
            result = tree.xpath('//a[@title="可在BT客户端使用，当天有效。"]')
            if result:
                result = result[0].get('href')
                logger.info(f'获取种子下载地址成功{result}')
            else:
                logger.error('获取种子下载地址失败')
                return False, '获取种子下载地址失败'

            if torrent_path != '' and torrent_path is not None and torrent_path != 'None':
                response = requests.get(result, headers=headers, timeout=10,
                                        proxies=proxies)
                if response.status_code == 200:
                    # 提取文件名
                    filename = response.headers['Content-Disposition'].split('filename=')[1].split(';')[0].replace('"',
                                                                                                                   '')
                    decoded_filename = filename.encode('latin-1').decode('utf-8')
                    # 下载种子
                    save_path = f'{torrent_path}/{decoded_filename}'
                    with open(f'{torrent_path}/{decoded_filename}', 'wb') as f:
                        f.write(response.content)
                    logger.info(f'下载种子成功{filename}')
                    return True, result, save_path
                else:
                    logger.error(f'下载种子失败,状态码为:{response.status_code}')
                    return False, f'下载种子失败,状态码为:{response.status_code}', ""

        else:
            logger.error(f'获取种子下载地址失败,状态码为:{response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:{response.status_code}', ""
    except Exception as e:
        logger.exception(f'获取种子下载地址失败{e}')
        return False, '获取种子下载地址失败', ""
