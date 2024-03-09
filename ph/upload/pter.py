import os
import re
import time
from lxml import etree
import requests
from util.log import logger
from urllib.parse import unquote

proxies = {}


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


def upload_pter(cookies_str, torrent_file, main_title, compose, descr, media_info, proxy, torrent_path, feed) -> (bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_pter(cookies_str)
    if not get_success:
        return False, get_str, ""
    global proxies
    if proxy != '' or proxy is not None:
        logger.info(f'使用代理:{proxy}')
        proxies = {
            'http': proxy,
            'https': proxy
        }
    main_title = main_title.replace('.', ' ')
    logger.info("处理前的主标题为：" + main_title)
    main_title = main_title.replace('AVC', 'H.264')
    main_title = main_title.replace('H264', 'H.264')
    main_title = main_title.replace('H265', 'H.265')
    main_title = main_title.replace('HEVC', 'H.265')
    writing_library = re.search(r'Writing.*library.*:(.*)',
                                media_info)
    if writing_library:
        if 'x264' in writing_library.group(1):
            logger.info("Writing library中存在x264，主标题将被替换")
            main_title = main_title.replace('H.264', 'x264')
        if 'x265' in writing_library.group(1):
            logger.info("Writing library中存在x265，主标题将被替换")
            main_title = main_title.replace('H.265', 'x265')
    logger.info("处理后的主标题为：" + main_title)
    logger.info("副标题为：" + compose)
    descr = descr.replace('[mediainfo]', '[hide=MediaInfo]')
    descr = descr.replace('[/mediainfo]', '[/hide]')
    logger.info("处理后的简介为：" + descr)

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
        return False, '打开种子文件失败，请检查是否制作种子', ""

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
        # 国语
        'guoyu': 'yes',
        # 中字
        'zhongzi': 'yes',
        # 匿名
        'uplver': 'yes',
    }

    if feed:
        data['jinzhuan'] = 'yes'
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
                get_success, torrent_link, torrent_save_path = get_pter_torrent(cookies_str, torrent_id, torrent_path)
                return get_success, torrent_link, torrent_save_path
            else:
                logger.error(f'发布失败,重定向地址为:{redirect_url}')
                return False, f'发布失败,重定向地址为:{redirect_url}', ""
        else:
            logger.error(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}', ""

    except Exception as e:
        logger.error(f'发布失败,错误原因为:{e}')
        return False, '发布失败', ""


def get_pter_torrent(cookies_str, torrent_id, torrent_path) -> (bool, str):
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
    save_path = ""
    if torrent_path != '' and torrent_path is not None and torrent_path != 'None':
        try:
            response = requests.get(f'https://pterclub.com/download.php?id={torrent_id}', headers=headers, timeout=10,
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
                return True, result, save_path
            else:
                logger.error('获取种子下载地址失败')
                return False, '获取种子下载地址失败', ""

        else:
            logger.error(f'获取种子下载地址失败,状态码为:{response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.error(f'获取种子下载地址失败{e}')
        return False, '获取种子下载地址失败', ""
