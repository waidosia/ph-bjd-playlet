from qbittorrentapi import Client, LoginFailed


# 调用qbittorrent的API下载种子进行做种
def qb_download(qbittorrent_host, qbittorrent_user, qbittorrent_pass, torrent_urls, path) -> (bool, str):
    result_text = ""
    qb = Client(host=qbittorrent_host, username=qbittorrent_user, password=qbittorrent_pass)
    try:
        qb.auth_log_in()
    except LoginFailed:
        print("登陆失败")
        return False, "登陆失败, 请检查地址或账号密码"
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
