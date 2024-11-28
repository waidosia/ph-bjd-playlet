import os
import re
import time

import requests
from lxml import etree

from util.log import logger

dream_resolution_map = {
    '480P': '7',
    '720P': '8',
    '1080P': '1',
    '2160P': '5',
    '4K': '5',
}

proxies = {}


def get_dream(cookies_str) -> (bool, str):
    global proxies
    headers = {
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://zmpt.cc/index.php',
    }
    try:
        response = requests.get('https://zmpt.cc/index.php', headers=headers, timeout=10, allow_redirects=False)
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


def upload_dream(cookies_str, torrent_file, main_title, compose, descr, proxy, torrent_path, feed) -> (
        bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_dream(cookies_str)
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
    main_title = main_title.replace('H264', 'h.264')
    main_title = main_title.replace('H265', 'h.265')
    main_title = main_title.replace('H 264', 'h.264')
    main_title = main_title.replace('H 265', 'h.265')
    logger.info("处理后的主标题为：" + main_title)
    logger.info("副标题为：" + compose)
    # # 去除指定一段落的内容
    # modified_content = re.sub(
    #     r'\[img\]https://img.pterclub.com/images/2024/01/10/49401952f8353abd4246023bff8de2cc.png\[/img\].*?\[mediainfo\].*?\[/mediainfo\]',
    #     '', descr, flags=re.DOTALL)
    modified_content = descr.replace('[mediainfo]', '[quote]')
    modified_content = descr.replace('[/mediainfo]', '[/quote]')
    logger.info("处理后的简介为：" + modified_content)

    logger.info("种子文件路径为：" + torrent_file)

    headers = {
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://zmpt.cc/upload.php',
    }
    try:
        file = open(torrent_file, 'rb').read()
    except Exception as e:
        logger.error(f'打开种子文件失败{e}')
        return False, '打开种子文件失败，请检查是否制作种子', ""

    # 从主标题中提取分辨率
    if len(main_title.split(' ')) > 4:
        resolution = main_title.split(' ')[-4].upper()
        video_codec = main_title.split(' ')[-2].upper()
    else:
        return False, '主标题格式错误,无法正确获取分辨率', ""
    tags = [17, 5, 6, 13, 12]
    if feed:
        tags.append(1)
    data = {
        'name': main_title,
        'small_descr': compose,
        'descr': modified_content,
        # 类型 短剧
        'type': '427',
        # 媒介 web_dl
        'medium_sel[4]': '10',
        # 分辨率
        'standard_sel[4]': dream_resolution_map.get(resolution, '0'),
        # 制作组
        'team_sel[4]': '10',
        # 标签 紧转 国语 中字 完结 驻站 冰种
        'tags[4][]': tags,
        # 匿名发布
        'uplver': 'yes',

    }
    # 验证一下，文件名带后缀，且去掉前面的路径
    filename = os.path.basename(torrent_file)
    files = {'file': (filename, file, 'application/x-bittorrent')}

    try:
        response = requests.request("POST", 'https://zmpt.cc/takeupload.php', headers=headers,
                                    data=data, files=files, allow_redirects=False,
                                    timeout=10)
        if response.status_code == 302:
            # 正常的重定向
            # 提取重定向后的地址
            redirect_url = response.headers['Location']
            torrent_id = redirect_url.split('id=')[1].split('&')[0]
            time.sleep(1)
            get_success, torrent_link, torrent_save_path = get_dream_torrent(cookies_str, torrent_id, torrent_path)
            return get_success, torrent_link, torrent_save_path
        else:
            logger.error(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}', ""

    except Exception as e:
        logger.exception(f'发布失败,错误为:{e}')
        return False, '发布失败', ""


def get_dream_torrent(cookies_str, torrent_id, torrent_path) -> (bool, str):
    global proxies
    headers = {
        'Cookie': cookies_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.5615.138 Safari/537.36',
        'Referer': 'https://zmpt.cc/index.php',
    }
    save_path = ""
    if torrent_path != '' and torrent_path is not None and torrent_path != 'None':
        try:
            response = requests.get(f'https://zmpt.cc/download.php?id={torrent_id}', headers=headers, timeout=10,
                                    proxies=proxies)
            if response.status_code == 200:
                # 提取文件名
                filename = response.headers['Content-Disposition'].split('filename=')[1].split(';')[0].replace('"', '')
                decoded_filename = filename.encode('latin-1').decode('utf-8')
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
        response = requests.get(f'https://zmpt.cc/details.php?id={torrent_id}', headers=headers, timeout=10)
        if response.status_code == 200:
            # 获取种子下载链接
            html = response.text
            tree = etree.HTML(html, etree.HTMLParser())
            result = tree.xpath('//*[@id="content"]/text()')
            if result:
                result = result[0]
                logger.info(f'获取种子下载地址成功{result}')
                return True, result, save_path
            else:
                logger.info('获取种子下载地址失败')
                return False, '获取种子下载地址失败', ""

        else:
            logger.error(f'获取种子下载地址失败,状态码为: {response.status_code}')
            return False, f'获取种子下载地址失败,状态码为:{response.status_code}'
    except Exception as e:
        logger.exception(f'获取种子下载地址失败，错误为:{e}')
        return False, '获取种子下载地址失败', ""
