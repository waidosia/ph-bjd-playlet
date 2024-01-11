import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from qbittorrentapi import Client, LoginFailed


# 编码字典


def upload(cookies_str, torrent_file, main_title, compose, descr, chinese_name):
    try:
        browser = webdriver.Chrome()
        browser.get('https://tjupt.org')
        for name, value in cookie_parse(cookies_str).items():
            cookie_dict = {
                'domain': '.tjupt.org',
                'name': name,
                'value': value,
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            browser.add_cookie(cookie_dict)
        browser.refresh()
        # 跳转到上传页面
        print("开始跳转")
        browser.get('https://tjupt.org/upload.php')
        # 等待页面跳转
        time.sleep(5)
        # 开始填写内容
        # 上传文件
        browser.find_element("xpath", '//*[@id="torrent"]').send_keys(torrent_file)
        time.sleep(5)
        # 选择资源类型
        dropdown = browser.find_element("xpath", '//*[@id="browsecat"]')
        select = Select(dropdown)
        select.select_by_value('402')
        time.sleep(1)
        # 填写中文名
        browser.find_element("xpath", '//*[@id="cname"]').send_keys(chinese_name)
        # 填写主标题
        browser.find_element("xpath", '//*[@id="ename"]').send_keys(main_title)
        # 选择剧集类型
        browser.find_element("xpath", '//*[@id="specificcat1"]').click()
        # 填写副标题
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[5]/td[2]/input').send_keys(compose)
        # 填写简介
        browser.find_element("xpath", '//*[@id="descr"]').send_keys(descr)
        time.sleep(1)
        # 勾选标签
        # 驻站
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[11]/td[2]/label[2]/input').click()
        # 禁转
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[11]/td[2]/label[3]/input').click()
        # 等30秒检查后点击提交
        time.sleep(30)
        # 提交
        browser.find_element("xpath", '//*[@id="qr"]').click()
        # 等待页面跳转
        time.sleep(5)
        # 判断页面是否正常跳转，跳转后的页面地址为https://tjupt.org/details.php?id=
        # 判断地址中是否包含指定的字符串
        if 'https://tjupt.org/details.php' in browser.current_url:
            # 获取当前页面的源码
            html = browser.page_source
            # 关闭浏览器
            browser.close()
            # 使用BeautifulSoup解析页面
            soup = BeautifulSoup(html, 'html.parser')
            # 获取种子下载链接
            torrent_url = soup.find('a', {'id': 'direct_link'}).get('href')
            # 返回种子下载链接
            return torrent_url
        else:
            # 上传失败
            torrent_url = ''
            # 关闭浏览器
            browser.close()
            return torrent_url
    except Exception as e:
        print(e)

    return


def cookie_parse(cookies_str):
    if not cookies_str:
        return {}
    cookie_dict = {}
    cookies = cookies_str.split(';')
    for cookie in cookies:
        _ = cookie.split('=')
        if len(_) > 1:
            cookie_dict[_[0].strip()] = _[1].strip()
    return cookie_dict


def qb_download(qbittorrent_host, qbittorrent_user, qbittorrent_pass, torrent_url, path) -> bool:
    qb = Client(host=qbittorrent_host, username=qbittorrent_user, password=qbittorrent_pass)
    try:
        qb.auth_log_in()
    except LoginFailed:
        print("登陆失败")
        return False
    is_add = qb.torrents_add(urls=torrent_url, is_paused=True,savepath=path)
    if is_add != 'Ok.':
        print('添加失败')
        return False

    print('添加成功')
    qb.auth_log_out()
    return True
