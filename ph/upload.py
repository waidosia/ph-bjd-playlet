import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# 编码字典
encod_map = {
    'AVC': '1',
}
# 音频编码字典
audio_map = {
    'AAC': '6',
}

# 分辨率字典
resolution_map = {
    "720P": '3',
    "1080P": '1',
    "2160P": '5',
}


def upload(cookies_str, torrent_file, main_title, compose, descr, media):
    try:
        resolution, encoding, audio = get_info(main_title)
        browser = webdriver.Chrome()
        browser.get('https://agsvpt.com/agsvpt')
        for name, value in cookie_parse(cookies_str).items():
            cookie_dict = {
                'domain': '.agsvpt.com',
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
        browser.get('https://abroad.agsvpt.com/upload.php')
        # 等待页面跳转
        time.sleep(10)
        # 开始填写内容
        # 上传文件
        browser.find_element("xpath", '//*[@id="torrent"]').send_keys(torrent_file)
        time.sleep(5)
        # 填写主标题，先清空再填写
        browser.find_element("xpath", '//*[@id="name"]').clear()
        time.sleep(1)
        browser.find_element("xpath", '//*[@id="name"]').send_keys(main_title)
        time.sleep(1)
        # 填写副标题
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[4]/td[2]/input').send_keys(compose)
        time.sleep(1)
        # 填写简介
        browser.find_element("xpath", '//*[@id="descr"]').send_keys(descr)
        time.sleep(1)
        # 填写MediaInfo
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[10]/td[2]/textarea').send_keys(media)
        # 选择类型
        dropdown = browser.find_element("xpath", '//*[@id="browsecat"]')
        select = Select(dropdown)
        select.select_by_value('419')
        time.sleep(1)
        # 选择媒介
        dropdown = browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[12]/td[2]/select[1]')
        select = Select(dropdown)
        select.select_by_value('10')
        time.sleep(1)
        # 选择编码
        dropdown = browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[12]/td[2]/select[2]')
        select = Select(dropdown)
        select.select_by_value(encod_map[encoding])
        time.sleep(1)
        # 选择音频编码
        dropdown = browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[12]/td[2]/select[3]')
        select = Select(dropdown)
        select.select_by_value(audio_map[audio])
        time.sleep(1)
        # 选择分辨率
        dropdown = browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[12]/td[2]/select[4]')
        select = Select(dropdown)
        select.select_by_value(resolution_map[resolution])
        time.sleep(1)
        # 选择小组
        dropdown = browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[12]/td[2]/select[5]')
        select = Select(dropdown)
        select.select_by_value('23')
        time.sleep(1)
        # 勾选标签
        # 国语
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[14]/td[2]/label[5]/input').click()
        # 中字
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[14]/td[2]/label[9]/input').click()
        # 完结
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[14]/td[2]/label[11]/input').click()
        # 驻站
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[14]/td[2]/label[19]/input').click()
        # 冰种
        browser.find_element("xpath", '//*[@id="compose"]/table/tbody/tr[14]/td[2]/label[20]/input').click()
        # 等30秒检查后点击提交
        time.sleep(5)
        # 提交
        browser.find_element("xpath", '//*[@id="qr"]').click()
        # 等待页面跳转
        time.sleep(5)
        print(browser.current_url)
        browser.close()
        # 判断页面是否正常跳转，跳转后的页面地址为https://abroad.agsvpt.com/details.php?id=
    #     # 判断地址中是否包含指定的字符串
    #     if 'https://abroad.agsvpt.com/details.php?id=' in browser.current_url:
    #         # 获取种子地址给qb
    #         torrent_url = browser.find_element("xpath", '//*[@id="outer"]/table[1]/tbody/tr[7]/td[2]/a').get_attribute(
    #             'href')
    #     else:
    #         # 上传失败
    #         torrent_url = ''
    except Exception as e:
        print(e)
    #     torrent_url = ''
    # print(torrent_url)

    return ""


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


# 从主标题提取信息
def get_info(main_title):
    # Hei An Yuan Cheng 2023 S01 1080P WEB-DL AVC AAC-GodDramas
    # 提取分辨率
    resolution = main_title.split(' ')[-4]
    # 提取编码
    encoding = main_title.split(' ')[-2]
    # 提取音频编码
    audio = main_title.split(' ')[-1]
    audio = audio.split('-')[0]
    return resolution, encoding, audio

