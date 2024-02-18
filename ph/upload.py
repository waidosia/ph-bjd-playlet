import os
from lxml import etree

import requests
from bs4 import BeautifulSoup

agsv_resolution_map = {
    '480P': '4',
    '720P': '3',
    '1080P': '1',
    '4K': '5',
}


###############TJUPT################

def get_tjupt(cookies_str) -> (bool, str):
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
        response = requests.get('https://tjupt.org/index.php', headers=headers, timeout=10)
        if response.status_code == 200:
            # 判断是否有登录字样，如果有则说明cookie过期
            if '一周之内自动登录' in response.text:
                print('cookie过期')
                return False, 'cookie过期'
            print('获取主页成功')
            return True, response.text
        else:
            print(f'获取主页失败,状态码为:{response.status_code}')
            return False, '获取主页失败,状态码为:{response.status_code}'
    except Exception as e:
        print('获取主页失败', e)
        return False, '获取主页失败'


def upload_tjupt(cookies_str, torrent_file, main_title, compose, descr, chinese_name) -> (bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_tjupt(cookies_str)
    if not get_success:
        return False, 'cookie已过期,请更新cookie'
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
        print('打开种子文件失败', e)
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
            # 提取重定向后的地址
            redirect_url = response.headers['Location']
            # details.php?id=399109&uploaded=1
            if 'details.php' in redirect_url:
                print('发布成功,尝试获取种子id')
                torrent_id = redirect_url.split('id=')[1].split('&')[0]
                print('获取种子id成功', torrent_id)
                get_success, torrent_link = get_tjupt_torrent(cookies_str, torrent_id)
                if get_success:
                    return True, torrent_link
                else:
                    return False, torrent_link
        else:
            print(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}'

    except Exception as e:
        print('发布失败', e)
        return False, '发布失败'


def get_tjupt_torrent(cookies_str, torrent_id) -> (bool, str):
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
            print('获取种子下载地址成功', torrent_url)
            return True, torrent_url
        else:
            print('获取种子下载地址失败,状态码为:', response.status_code)
            return False, '获取种子下载地址失败,状态码为:', response.status_code
    except Exception as e:
        print('获取种子下载地址失败', e)
        return False, '获取种子下载地址失败'


###############AGSVPT################


def get_agsv(cookies_str) -> (bool, str):
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
        response = requests.get('https://www.agsvpt.com/index.php', headers=headers, timeout=10)
        if response.status_code == 200:
            # 判断是否有登录字样，如果有则说明cookie过期
            if '已有账户,点此登录' in response.text:
                print('cookie过期')
                return False, 'cookie过期'
            print('获取主页成功')
            return True, response.text
        else:
            print(f'获取主页失败,状态码为:{response.status_code}')
            return False, '获取主页失败,状态码为:{response.status_code}'
    except Exception as e:
        print('获取主页失败', e)
        return False, '获取主页失败'


def upload_agsv(cookies_str, torrent_file, main_title, compose, descr, media_info) -> (bool, str):
    # 发布前，先请求一次主站，确定cookie是否是过期的
    get_success, get_str = get_agsv(cookies_str)
    if not get_success:
        return False, 'cookie已过期,请更新cookie'

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
        print('打开种子文件失败', e)
        return False, '打开种子文件失败，请检查是否制作种子'

    # 从主标题中提取分辨率
    resolution = main_title.split(' ')[-4].upper()

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
        'standard_sel[4]': agsv_resolution_map[resolution],
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
            get_success, torrent_link = get_agsv_torrent(cookies_str, redirect_url)
            if get_success:
                return True, torrent_link
            else:
                return False, torrent_link
        else:
            print(f'发布失败,状态码为:{response.status_code}')
            return False, f'发布失败,状态码为:{response.status_code}'

    except Exception as e:
        print('发布失败', e)
        return False, '发布失败'


def get_agsv_torrent(cookies_str, torrent_link) -> (bool, str):
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
            tree = etree.HTML(html,etree.HTMLParser())
            result = tree.xpath('//a[@title="可在BT客户端使用，当天有效。"]')
            if result:
                result = result[0].get('href')
                print('获取种子下载地址成功', result)
                return True, result
            else:
                print('获取种子下载地址失败')
                return False, '获取种子下载地址失败'

        else:
            print('获取种子下载地址失败,状态码为:', response.status_code)
            return False, '获取种子下载地址失败,状态码为:', response.status_code
    except Exception as e:
        print('获取种子下载地址失败', e)
        return False, '获取种子下载地址失败'

