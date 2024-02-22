from transmission_rpc import Client as trClient
from qbittorrentapi import Client, LoginFailed

import socket
import re

from util.log import logger


# 调用qbittorrent的API下载种子进行做种
def qb_download(qbittorrent_host, qbittorrent_user, qbittorrent_pass, torrent_urls, path) -> (bool, str):
    # 测试ip与端口是否能连接
    # 使用tcp连接进行测试
    # 正则匹配出host和port
    match = re.match(r"(?:http[s]?://)?([^:/]+)(?::(\d+))", qbittorrent_host)
    if match:
        host = match.group(1)
        port = match.group(2) if match.group(2) else "80"  # 默认端口为80
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((host, int(port)))
            s.shutdown(2)
            s.close()
            logger.info(f'{qbittorrent_host}地址通')
        except Exception as e:
            logger.error(f'无法连接到{qbittorrent_host}, 错误信息: {e}')
            return False, "无法连接到qbittorrent"
    else:
        logger.error(f'无法解析地址{qbittorrent_host}')
        return False, "无法解析地址"

    result_text = ""
    qb = Client(host=qbittorrent_host, username=qbittorrent_user, password=qbittorrent_pass)
    try:
        qb.auth_log_in()
    except LoginFailed:
        print("登陆失败")
        return False, "登陆失败, 请检查地址或账号密码"
    except Exception as e:
        print(f"登陆失败, 错误信息: {e}")
        return False, f"登陆失败, 错误信息: {e}"

    # 打印qb的版本号
    logger.info(f"qbittorrent版本号：{qb.app.version}")
    for torrent_url in torrent_urls:
        if torrent_url is not None:
            is_add = qb.torrents_add(urls=torrent_url, is_paused=True, savepath=path)
            if is_add != 'Ok.':
                print(f'{torrent_url}添加失败')
                result_text += f'{torrent_url}添加失败\n'
    qb.auth_log_out()
    if result_text != "":
        return False, result_text
    return True, "添加成功"


def tr_download(tr_host, tr_user, tr_pass, torrent_urls, path) -> (bool, str):
    match = re.match(r"(?:http[s]?://)?([^:/]+)(?::(\d+))", tr_host)
    if match:
        host = match.group(1)
        port = match.group(2) if match.group(2) else "80"  # 默认端口为80
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((host, int(port)))
            s.shutdown(2)
            s.close()
            logger.info(f'{tr_host}地址通')
        except Exception as e:
            logger.error(f'无法连接到{tr_host}, 错误信息: {e}')
            return False, "无法连接到tr"
    else:
        logger.error(f'无法解析地址{tr_host}')
        return False, "无法解析地址"

    result_text = ""
    try:
        tr = trClient(host=host, port=port, username=tr_user, password=tr_pass)
    except Exception as e:
        logger.error(f'无法连接到{tr_host}, 错误信息: {e}')
        return False, "无法连接到tr"
    # 打印tr的版本号
    version = tr.rpc_version
    logger.info(f"Transmission版本号：{version}")
    for torrent_url in torrent_urls:
        if torrent_url is not None:
            try:
                tr.add_torrent(torrent_url, download_dir=path)
            except Exception as e:
                print(f'{torrent_url}添加失败,error: {e}')
                result_text += f'{torrent_url}添加失败\n'
    if result_text != "":
        return False, result_text
    return True, "添加成功"
