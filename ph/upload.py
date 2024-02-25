import os
import time

from lxml import etree

import requests
from bs4 import BeautifulSoup
from util.log import logger

agsv_resolution_map = {
    '480P': '4',
    '720P': '3',
    '1080P': '1',
    '4K': '5',
}

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

red_leaves_resolution_map = {
    '720P': '3',
    '1080P': '1',
    '4K': '5',
}

proxies = {}


###############TJUPT################

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


def upload_tjupt(cookies_str, torrent_file, main_title, compose, descr, chinese_name, proxy) -> (bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_tjupt(cookies_str)
    if not get_success:
        return False, get_str
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
        return False, '打开种子文件失败，请检查是否制作种子'

    data = {
        'referid': '',
        'type': '402',
        'cname': chinese_name,
        'ename': main_title,
        'specificcat1': '大陆',
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
                get_success, torrent_link = get_tjupt_torrent(cookies_str, torrent_id)
                if get_success:
                    return True, torrent_link
                else:
                    return False, torrent_link
        else:
            logger.info(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}'

    except Exception as e:
        logger.info(f'发布失败,错误原因为{e}')
        return False, '发布失败'


def get_tjupt_torrent(cookies_str, torrent_id) -> (bool, str):
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
    try:
        response = requests.get(f'https://tjupt.org/details.php?id={torrent_id}', headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            soup = BeautifulSoup(response.text, 'html.parser')
            torrent_url = soup.find('a', {'id': 'direct_link'}).get('href')
            logger.info(f'获取种子下载地址成功{torrent_url}')
            return True, torrent_url
        else:
            logger.info(f'获取种子下载地址失败,状态码为:{response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:', response.status_code
    except Exception as e:
        logger.error(f'获取种子下载地址失败:{e}')
        return False, '获取种子下载地址失败'


###############AGSVPT################


def get_agsv(cookies_str) -> (bool, str):
    global proxies
    headers = {
        'Host': 'www.agsvpt.com',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://www.agsvpt.com/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get('https://www.agsvpt.com/index.php', headers=headers, timeout=10, allow_redirects=False)
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
            logger.error(f'获取主页失败,状态码为:{response.status_code}')
            return False, f'获取主页失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.exception(f'获取主页失败，错误为:{e}')
        return False, '获取主页失败'


def upload_agsv(cookies_str, torrent_file, main_title, compose, descr, media_info, proxy) -> (bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_agsv(cookies_str)
    if not get_success:
        return False, get_str
    global proxies
    if proxy != '' or proxy is not None:
        logger.info(f'使用代理:{proxy}')
        proxies = {
            'http': proxy,
            'https': proxy
        }

    headers = {
        'Host': 'www.agsvpt.com',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://www.agsvpt.com/upload.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Origin': 'https://www.agsvpt.com',

    }
    try:
        file = open(torrent_file, 'rb').read()
    except Exception as e:
        logger.error(f'打开种子文件失败{e}')
        return False, '打开种子文件失败，请检查是否制作种子'

    # 从主标题中提取分辨率
    if len(main_title.split(' ')) > 4:
        resolution = main_title.split(' ')[-4].upper()
    else:
        return False, '主标题格式错误,无法正确获取分辨率'
    data = {
        'name': main_title,
        'small_descr': compose,
        'price': '',
        'descr': descr,
        'color': '0',
        'font': '0',
        'size': '0',
        # media_info信息
        'technical_info': media_info,
        # 类型 短剧
        'type': '419',
        # 媒介 web_dl
        'medium_sel[4]': '10',
        # 编码 h.264,avc
        'codec_sel[4]': '1',
        # 音频编码 aac
        'audiocodec_sel[4]': '6',
        # 分辨率
        'standard_sel[4]': agsv_resolution_map.get(resolution, '0'),
        # 制作组
        'team_sel[4]': '23',
        # 标签 紧转 国语 中字 完结 驻站 冰种
        'tags[4][]': [1, 5, 6, 19, 44, 34],
        # 匿名发布
        'uplver': 'yes',

    }
    # 验证一下，文件名带后缀，且去掉前面的路径
    filename = os.path.basename(torrent_file)
    files = {'file': (filename, file, 'application/x-bittorrent')}

    try:
        response = requests.request("POST", 'https://www.agsvpt.com/takeupload.php', headers=headers,
                                    data=data, files=files, allow_redirects=False,
                                    timeout=10)
        if response.status_code == 302:
            # 正常的重定向
            # 提取重定向后的地址
            redirect_url = response.headers['Location']
            time.sleep(1)
            get_success, torrent_link = get_agsv_torrent(cookies_str, redirect_url)
            if get_success:
                return True, torrent_link
            else:
                return False, torrent_link
        else:
            logger.error(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}'

    except Exception as e:
        logger.exception(f'发布失败,错误为:{e}')
        return False, '发布失败'


def get_agsv_torrent(cookies_str, torrent_link) -> (bool, str):
    global proxies
    headers = {
        'Host': 'www.agsvpt.com',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://www.agsvpt.com/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get(torrent_link, headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            html = response.text
            tree = etree.HTML(html, etree.HTMLParser())
            result = tree.xpath('//a[@title="可在BT客户端使用，当天有效。"]')
            if result:
                result = result[0].get('href')
                logger.info(f'获取种子下载地址成功{result}')
                return True, result
            else:
                logger.info('获取种子下载地址失败')
                return False, '获取种子下载地址失败'

        else:
            logger.error(f'获取种子下载地址失败,状态码为: {response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.exception(f'获取种子下载地址失败，错误为:{e}')
        return False, '获取种子下载地址失败'


###############Pter################

def get_pter(cookies_str) -> (bool, str):
    global proxies
    headers = {
        'Host': 'pterclub.com',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://pterclub.com/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get('https://pterclub.com/index.php', headers=headers, timeout=10, allow_redirects=False)
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
            return False, '获取主页失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.error('获取主页失败', e)
        return False, '获取主页失败'


def upload_pter(cookies_str, torrent_file, main_title, compose, descr, proxy) -> (bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_pter(cookies_str)
    if not get_success:
        return False, get_str
    global proxies
    if proxy != '' or proxy is not None:
        logger.info(f'使用代理:{proxy}')
        proxies = {
            'http': proxy,
            'https': proxy
        }

    headers = {
        'Host': 'pterclub.com',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://pterclub.com/upload.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Origin': 'https://pterclub.com',

    }
    try:
        file = open(torrent_file, 'rb').read()
    except Exception as e:
        logger.error(f'打开种子文件失败{e}')
        return False, '打开种子文件失败，请检查是否制作种子'

    data = {
        'name': main_title,
        'small_descr': compose,
        'descr': descr,
        'color': '0',
        'font': '0',
        'size': '0',
        # 类型 电视剧
        'type': '404',
        # 媒介 web_dl
        'source_sel': '5',
        # 地区 大陆
        'team_sel': '1',
        # 禁转
        'jinzhuan': 'yes',
        # 国语
        'guoyu': 'yes',
        # 中字
        'zhongzi': 'yes',
        # 匿名
        'uplver': 'yes',
    }
    # 验证一下，文件名带后缀，且去掉前面的路径
    filename = os.path.basename(torrent_file)
    files = {'file': (filename, file, 'application/x-bittorrent')}

    try:
        response = requests.request("POST", 'https://pterclub.com/takeupload.php', headers=headers,
                                    data=data, files=files, allow_redirects=False,
                                    timeout=10)
        if response.status_code == 302:
            # 正常的重定向
            # 提取重定向后的地址
            redirect_url = response.headers['Location']
            # /details.php?id=450830&uploaded=1

            if 'details.php' in redirect_url:
                logger.info('发布成功,尝试获取种子id')
                torrent_id = redirect_url.split('id=')[1].split('&')[0]
                logger.info(f'获取种子id成功{torrent_id}')
                time.sleep(1)
                get_success, torrent_link = get_pter_torrent(cookies_str, torrent_id)
                if get_success:
                    return True, torrent_link
                else:
                    return False, torrent_link
            else:
                logger.error(f'发布失败,重定向地址为:{redirect_url}')
                return False, f'发布失败,重定向地址为:{redirect_url}'
        else:
            logger.error(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}'

    except Exception as e:
        logger.error(f'发布失败,错误原因为:{e}')
        return False, '发布失败'


def get_pter_torrent(cookies_str, torrent_id) -> (bool, str):
    global proxies
    headers = {
        'Host': 'pterclub.com',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://pterclub.com/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get(f"https://pterclub.com/details.php?id={torrent_id}", headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            html = response.text
            tree = etree.HTML(html, etree.HTMLParser())
            result = tree.xpath('//a[@class="faqlink"]')
            if result:
                result = result[0].get('href')
                # 地址需要拼接
                result = 'https://pterclub.com/' + result
                logger.info(f'获取种子下载地址成功{result}')
                return True, result
            else:
                logger.error('获取种子下载地址失败')
                return False, '获取种子下载地址失败'

        else:
            logger.error(f'获取种子下载地址失败,状态码为:{response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.error(f'获取种子下载地址失败{e}')
        return False, '获取种子下载地址失败'


###############Kylin################
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


def upload_kylin(cookies_str, torrent_file, main_title, compose, descr, year, proxy) -> (bool, str):
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
        return False, get_str
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
        return False, '打开种子文件失败，请检查是否制作种子'

    # 从主标题中提取分辨率
    if len(main_title.split(' ')) > 6:
        resolution = main_title.split(' ')[-4].upper()
    else:
        return False, '主标题格式错误,无法正确获取分辨率或年'

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
            time.sleep(1)
            get_success, torrent_link = get_kylin_torrent(cookies_str, redirect_url)
            if get_success:
                return True, torrent_link
            else:
                return False, torrent_link
        else:
            logger.error(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}'

    except Exception as e:
        logger.error(f'发布失败{e}')
        return False, '发布失败'


def get_kylin_torrent(cookies_str, torrent_link) -> (bool, str):
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
        response = requests.get(torrent_link, headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            html = response.text
            tree = etree.HTML(html, etree.HTMLParser())
            result = tree.xpath('//a[@title="可在BT客户端使用，当天有效。"]')
            if result:
                result = result[0].get('href')
                logger.info(f'获取种子下载地址成功{result}')
                return True, result
            else:
                logger.error('获取种子下载地址失败')
                return False, '获取种子下载地址失败'

        else:
            logger.error(f'获取种子下载地址失败,状态码为:{response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.exception(f'获取种子下载地址失败{e}')
        return False, '获取种子下载地址失败'


###############红叶################

def get_red_leaves(cookies_str) -> (bool, str):
    global proxies
    headers = {
        'Host': 'leaves.red',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://leaves.red/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get('https://leaves.red/index.php', headers=headers, timeout=10, allow_redirects=False,
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


def upload_red_leaves(cookies_str, torrent_file, main_title, compose, descr, media_info, proxy) -> (bool, str):
    global proxies
    if proxy != '' or proxy is not None:
        logger.info(f'使用代理:{proxy}')
        proxies = {
            'http': proxy,
            'https': proxy
        }
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_red_leaves(cookies_str)
    if not get_success:
        return False, get_str
    headers = {
        'Host': 'leaves.red',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://leaves.red/upload.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Origin': 'https://leaves.red',

    }
    try:
        file = open(torrent_file, 'rb').read()
    except Exception as e:
        logger.error(f'打开种子文件失败{e}')
        return False, '打开种子文件失败，请检查是否制作种子'

    # 从主标题中提取分辨率
    if len(main_title.split(' ')) > 6:
        resolution = main_title.split(' ')[-4].upper()
    else:
        return False, '主标题格式错误,无法正确获取分辨率或年'

    data = {
        'name': main_title,
        'small_descr': compose,
        'descr': descr,
        # media_info信息
        'technical_info': media_info,
        # 类型 短剧
        'type': '439',
        # 媒介 web_dl
        'medium_sel[5]': '8',
        # 视频编码 h.264
        'codec_sel[5]': '1',
        # 音频编码 aac
        'audiocodec_sel[5]': '6',
        # 分辨率
        'standard_sel[5]': red_leaves_resolution_map.get(resolution, '0'),
        # 地区 中国
        'processing_sel[5]': '2',
        # 制作组
        'team_sel[5]': '29',
        # 标签
        'tags[5][]': [1, 3, 5, 6, 28],
        # 匿名发布
        'uplver': 'yes',
    }
    # 验证一下，文件名带后缀，且去掉前面的路径
    filename = os.path.basename(torrent_file)
    files = {'file': (filename, file, 'application/x-bittorrent')}

    try:
        response = requests.request("POST", 'https://leaves.red/takeupload.php', headers=headers,
                                    data=data, files=files, allow_redirects=False,
                                    timeout=10, proxies=proxies)
        if response.status_code == 302:
            # 正常的重定向
            # 提取重定向后的地址
            redirect_url = response.headers['Location']
            time.sleep(1)
            get_success, torrent_link = get_red_leaves_torrent(cookies_str, redirect_url)
            if get_success:
                return True, torrent_link
            else:
                return False, torrent_link
        else:
            logger.error(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}'

    except Exception as e:
        logger.error(f'发布失败{e}')
        return False, '发布失败'


def get_red_leaves_torrent(cookies_str, torrent_link) -> (bool, str):
    global proxies
    headers = {
        'Host': 'leaves.red',
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://leaves.red/index.php',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get(torrent_link, headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            html = response.text
            tree = etree.HTML(html, etree.HTMLParser())
            result = tree.xpath('//a[@title="可在BT客户端使用，当天有效。"]')
            if result:
                result = result[0].get('href')
                logger.info(f'获取种子下载地址成功{result}')
                return True, result
            else:
                logger.error('获取种子下载地址失败')
                return False, '获取种子下载地址失败'

        else:
            logger.error(f'获取种子下载地址失败,状态码为:{response.status_code}' )
            return False, f'获取种子下载地址失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.exception(f'获取种子下载地址失败{e}')
        return False, '获取种子下载地址失败'
