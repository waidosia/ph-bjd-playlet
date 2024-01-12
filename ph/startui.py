import os
import re
import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog

from .mediainfo import get_media_info
from .rename import get_video_info
from .screenshot import extract_complex_keyframes, upload_screenshot, upload_free_screenshot, get_thumbnails
from .tool import update_settings, get_settings, get_file_path, rename_file_with_same_extension, \
    get_folder_path, check_path_and_find_video, rename_directory, create_torrent, load_names, chinese_name_to_pinyin, \
    get_video_files
from .ui.mainwindow import Ui_Mainwindow
from .ui.settings import Ui_Settings
from .upload import upload, qb_download


def starui():
    app = QApplication(sys.argv)
    myMainwindow = MainWindow()
    myico = QIcon("static/apr-bjd.ico")
    myMainwindow.setWindowIcon(myico)
    myMainwindow.show()
    sys.exit(app.exec())


class MainWindow(QMainWindow, Ui_Mainwindow):
    def __init__(self):
        super().__init__()
        self.upload_cover_thread = None
        self.upload_free_cover_thread = None
        self.setupUi(self)  # 设置界面
        self.mySettings = None

        self.get_pt_gen_thread = None
        self.get_pt_gen_for_name_thread = None
        self.upload_picture_thread0 = None
        self.upload_picture_thread1 = None
        self.upload_picture_thread2 = None
        self.upload_picture_thread3 = None
        self.upload_picture_thread4 = None
        self.upload_picture_thread5 = None
        self.upload_free_picture_thread0 = None
        self.upload_free_picture_thread1 = None
        self.upload_free_picture_thread2 = None
        self.upload_free_picture_thread3 = None
        self.upload_free_picture_thread4 = None
        self.upload_free_picture_thread5 = None
        self.make_torrent_thread = None
        self.torrent_path = None
        self.upload_cover_thread = None

        # 初始化
        self.videoPath.setDragEnabled(True)
        self.introBrowser.setText("")
        self.pictureUrlBrowser.setText("")
        self.mediainfoBrowser.setText("")
        self.debugBrowser.setText("")
        self.initialize_team_combobox()
        self.initialize_source_combobox()
        self.initialize_type_combobox()

        # 绑定点击信号和槽函数
        self.actionsettings.triggered.connect(self.settingsClicked)
        self.getPictureButton.clicked.connect(self.getPictureButtonClicked)
        self.uploadCoverButton.clicked.connect(self.uploadCoverButtonClicked)
        self.selectVideoFolderButton.clicked.connect(self.selectVideoFolderButtonClicked)
        self.selectCoverFolderButton.clicked.connect(self.selectCoverFolderButtonClicked)
        self.getMediaInfoButton.clicked.connect(self.getMediaInfoButtonClicked)
        self.getNameButton.clicked.connect(self.getNameButtonClicked)
        self.startButton.clicked.connect(self.startButtonClicked)
        self.makeTorrentButton.clicked.connect(self.makeTorrentButtonClicked)

        self.debugBrowser.append("程序初始化成功，使用前请查看设置中的说明")

    def initialize_team_combobox(self):
        team_names = load_names('static/team.json', 'team')
        for name in team_names:
            self.team.addItem(name)

    def initialize_source_combobox(self):
        source_names = load_names('static/source.json', 'source')
        for name in source_names:
            self.source.addItem(name)

    def initialize_type_combobox(self):
        type_names = load_names('static/type.json', 'type')
        for name in type_names:
            self.type.addItem(name)

    def startButtonClicked(self):
        # 调用发种函数
        cookie_str = get_settings("cookie")
        # 主标题
        mainTitle = self.mainTitleBrowser.toPlainText().replace(' ', '.')
        # 副标题
        secondTitle = self.secondTitleBrowser.toPlainText()
        # 简介
        introBrowser = self.introBrowser.toPlainText()
        # 中文标题
        chinese_name = self.chineseNameEdit.text()
        # 种子路径
        torrent_path = self.torrent_path
        # 判断种子路径是绝对路径还是相对路径，如果是相对则转换为绝对路径
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        self.upload_cover_thread = UploadThread(cookie_str, torrent_path, mainTitle, secondTitle, introBrowser,
                                                chinese_name)
        self.upload_cover_thread.finished_signal.connect(self.uploadFinished)
        self.upload_cover_thread.start()

    def uploadFinished(self, torrent_url):
        # qbittorrent的地址
        qbittorrent_host = get_settings("qbPath")
        # qbittorrent的用户名
        qbittorrent_user = get_settings("qbUser")
        # qbittorrent的密码
        qbittorrent_pass = get_settings("qbPasswd")
        # path = os.path.abspath(os.path.join(self.videoPath.text(), ".."))
        path = get_settings("resourcePath")
        if torrent_url:
            self.debugBrowser.append("发种成功：" + torrent_url)
            is_add = qb_download(qbittorrent_host, qbittorrent_user, qbittorrent_pass, torrent_url, path)
            if is_add:
                self.debugBrowser.append("做种成功：" + torrent_url)

            else:
                self.debugBrowser.append("做种失败：")
        else:
            self.debugBrowser.append("发种失败或获取种子链接失败,自行检查")
        self.videoPath.setText("")
        self.coverPath.setText("")
        self.mainTitleBrowser.setText("")
        self.secondTitleBrowser.setText("")
        self.introBrowser.setText("")
        self.pictureUrlBrowser.setText("")
        self.mediainfoBrowser.setText("")
        self.fileNameBrowser.setText("")
        self.chineseNameEdit.setText("")
        self.yearEdit.setText("")
        self.seasonBox.setText("")
        self.info.setText("")
        self.debugBrowser.append("所有输入框已清空")

    def settingsClicked(self):  # click对应的槽函数
        self.mySettings = Settings()
        self.mySettings.getSettings()
        myico = QIcon("static/apr-bjd.ico")
        self.mySettings.setWindowIcon(myico)
        self.mySettings.show()  # 加上self避免页面一闪而过

    def uploadCoverButtonClicked(self):
        cover_path = self.coverPath.text()
        if cover_path:
            self.debugBrowser.append("上传封面" + cover_path)
            figureBedPath = get_settings("figureBedPath")  # 图床地址
            figureBedToken = get_settings("figureBedToken")  # 图床Token
            if figureBedPath == "https://img.agsvpt.com/api/upload/" or figureBedPath == ("http://img.agsvpt.com/api"
                                                                                          "/upload/"):

                self.upload_cover_thread = UploadPictureThread(figureBedPath, figureBedToken, cover_path, True)
                self.upload_cover_thread.result_signal.connect(self.handleUploadPictureResult)  # 连接信号
                self.upload_cover_thread.start()  # 启动线程
                print("上传图床线程启动")
                self.debugBrowser.append("上传图床线程启动")
            else:
                self.upload_free_cover_thread = UploadFreePictureThread(figureBedPath, figureBedToken, cover_path, True)
                self.upload_free_cover_thread.result_signal.connect(self.handleUploadFreePictureResult)  # 连接信号
                self.upload_free_cover_thread.start()  # 启动线程

                print("上传图床线程启动")
                self.debugBrowser.append("上传图床线程启动")

    def getPictureButtonClicked(self):
        self.pictureUrlBrowser.setText("")
        isVideoPath, videoPath = check_path_and_find_video(self.videoPath.text())

        if isVideoPath == 1 or isVideoPath == 2:
            self.debugBrowser.append(f"获取视频 {videoPath} 的截图")
            self.debugBrowser.append("参数获取成功，开始执行截图函数")

            screenshotPath = get_settings("screenshotPath")
            figureBedPath = get_settings("figureBedPath")
            figureBedToken = get_settings("figureBedToken")
            screenshotNumber = int(get_settings("screenshotNumber"))
            screenshotThreshold = float(get_settings("screenshotThreshold"))
            screenshotStart = float(get_settings("screenshotStart"))
            screenshotEnd = float(get_settings("screenshotEnd"))
            getThumbnails = bool(get_settings("getThumbnails"))
            rows = int(get_settings("rows"))
            cols = int(get_settings("cols"))
            autoUploadScreenshot = bool(get_settings("autoUploadScreenshot"))

            # 截图函数执行

            screenshot_success, res = self.extract_and_get_thumbnails(videoPath, screenshotPath, screenshotNumber,
                                                                      screenshotThreshold, screenshotStart,
                                                                      screenshotEnd,
                                                                      getThumbnails, rows, cols)

            if screenshot_success:
                self.handle_screenshot_result(res, figureBedPath, figureBedToken, autoUploadScreenshot)
            else:
                self.debugBrowser.append("截图失败: " + str(res))
        else:
            self.debugBrowser.append("您的视频文件路径有误")

    @staticmethod
    def extract_and_get_thumbnails(videoPath, screenshotPath, screenshotNumber, screenshotThreshold,
                                   screenshotStart, screenshotEnd, getThumbnails, rows, cols):
        # 执行截图函数
        screenshot_success, res = extract_complex_keyframes(videoPath, screenshotPath, screenshotNumber,
                                                            screenshotThreshold, screenshotStart,
                                                            screenshotEnd, min_interval_pct=0.01)

        # 获取缩略图
        if getThumbnails:
            get_thumbnails_success, sv_path = get_thumbnails(videoPath, screenshotPath, rows, cols, screenshotStart,
                                                             screenshotEnd)
            if get_thumbnails_success:
                res.append(sv_path)

        return screenshot_success, res

    def handle_screenshot_result(self, res, figureBedPath, figureBedToken, autoUploadScreenshot):
        self.debugBrowser.append("成功获取截图：" + str(res))

        if autoUploadScreenshot:
            self.debugBrowser.append(f"开始自动上传截图到图床 {figureBedPath}")
            self.pictureUrlBrowser.setText("")
            for i, screenshot in enumerate(res[:6]):  # 限制上传至多6张截图
                self.upload_screenshot(figureBedPath, figureBedToken, screenshot, False, index=i)
            self.debugBrowser.append("上传图床线程启动")
        else:
            self.debugBrowser.append("未选择自动上传图床功能，图片已储存在本地")
            output = "\n".join(res)
            self.pictureUrlBrowser.setText(output)

    def upload_screenshot(self, figureBedPath, figureBedToken, screenshot, is_cover, index):
        thread_class = UploadPictureThread if (
                    "img.agsvpt.com/api/upload/" in figureBedPath) else UploadFreePictureThread

        upload_thread = thread_class(figureBedPath, figureBedToken, screenshot, is_cover)
        upload_thread.result_signal.connect(lambda success, api_response, path=screenshot: self.handle_upload_result(
            success, api_response, path, is_cover, self.paste_url_cover if is_cover else self.paste_url_image,
            False if ("img.agsvpt.com/api/upload/" in figureBedPath) else True))
        setattr(self, f"upload_picture_thread{index}", upload_thread)
        upload_thread.start()

    def handle_upload_result(self, upload_success, api_response, screenshot_path, is_cover, paste_url_callback,
                             is_free):
        print("接受到线程请求的结果")
        self.debugBrowser.append("接受到线程请求的结果")
        pasteScreenshotUrl = bool(get_settings("pasteScreenshotUrl"))
        deleteScreenshot = bool(get_settings("deleteScreenshot"))
        if upload_success:
            if not is_free:
                if api_response.get("statusCode", "") == "200":
                    bbsurl = str(api_response.get("bbsurl", ""))
                    self.pictureUrlBrowser.append(bbsurl)
                    api_response = bbsurl
                else:
                    if api_response.get("statusCode", "") == "":
                        self.debugBrowser.append("未接受到图床的任何响应" + '\n')
                    else:
                        self.debugBrowser.append(str(api_response) + '\n')
            else:
                self.pictureUrlBrowser.append(api_response)
            if pasteScreenshotUrl:
                if is_cover:
                    category = self.get_selected_categories()
                    print('类型为：' + category)
                    temp = self.introBrowser.toPlainText()
                    temp += '[quote][size=4]因组内调整，之后新发布，均禁止[color=Red]转载 [color=Black]谢谢！！[/size][/quote]\n'
                    temp += api_response
                    temp += '\n[img]https://img.pterclub.com/images/2024/01/10/GodDramas-.png[/img]\n'
                    self.introBrowser.setText(temp)

                    text = ('◎片　　名  {}\n◎年　　代  {}\n◎产　　地　大陆\n◎类　　别  {}\n◎语　　言  国语\n◎简　　介  {}'
                            .format(self.chineseNameEdit.text(), self.yearEdit.text(), category, self.info.text()))

                    self.introBrowser.append(text)
                    self.debugBrowser.append("成功将封面链接粘贴到简介前")
                else:
                    paste_url_callback(api_response)
                    self.debugBrowser.append("成功将图片链接粘贴到简介后")
                if deleteScreenshot:
                    self.delete_screenshot(screenshot_path)

        else:
            self.debugBrowser.append("图床响应不是有效的JSON格式")

    def get_selected_categories(self):
        categories = [
            '剧情', '爱情', '喜剧', '甜虐', '甜宠', '恐怖', '动作', '穿越', '重生', '逆袭', '科幻', '武侠', '都市', '古装'
        ]

        selected_categories = [categories[i] for i in range(len(categories)) if
                               getattr(self, f"checkBox_{i}").isChecked()]
        return ' '.join(selected_categories)

    def paste_url_cover(self, api_response):
        self.introBrowser.append(api_response)
        self.debugBrowser.append("成功将封面链接粘贴到简介前")

    def paste_url_image(self, api_response):
        self.introBrowser.append(api_response)
        self.debugBrowser.append("成功将图片链接粘贴到简介后")

    def delete_screenshot(self, screenshot_path):
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            print(f"文件 {screenshot_path} 已被删除。")
            self.debugBrowser.append(f"文件 {screenshot_path} 已被删除。")
        else:
            print(f"文件 {screenshot_path} 不存在。")
            self.debugBrowser.append(f"文件 {screenshot_path} 不存在。")

    def handleUploadPictureResult(self, upload_success, api_response, screenshot_path, is_cover):
        self.handle_upload_result(upload_success, api_response, screenshot_path, is_cover, self.paste_url_cover, False)

    def handleUploadFreePictureResult(self, upload_success, api_response, screenshot_path, is_cover):
        self.handle_upload_result(upload_success, api_response, screenshot_path, is_cover, self.paste_url_image, True)

    def selectCoverFolderButtonClicked(self):
        path = get_file_path()
        self.coverPath.setText(path)

    def selectVideoFolderButtonClicked(self):
        path = get_folder_path()
        self.videoPath.setText(path)

    def get_video_info_success(self):
        is_video_path, video_path = check_path_and_find_video(self.videoPath.text())
        if is_video_path == 2:
            return True, get_video_info(video_path)
        else:
            return False, "您的视频文件路径有误"

    def getMediaInfoButtonClicked(self):
        self.mediainfoBrowser.setText("")
        isVideoPath, videoPath = check_path_and_find_video(self.videoPath.text())  # 视频资源的路径
        if isVideoPath == 1 or isVideoPath == 2:
            get_media_info_success, mediainfo = get_media_info(videoPath)
            if get_media_info_success:
                self.mediainfoBrowser.setText(mediainfo)
                mediainfo_text = ('\n[img]https://img.pterclub.com/images/2024/01/10/49401952f8353abd4246023bff8de2cc'
                                  '.png[/img]\n[quote]') + mediainfo + '[/quote]'
                self.introBrowser.append(mediainfo_text)
                self.introBrowser.append('[img]https://img.pterclub.com/images/2024/01/10'
                                         '/3a3a0f41d507ffa05df76996a1ed69e7.png[/img]')
                self.debugBrowser.append("成功获取到MediaInfo")
            else:
                self.debugBrowser.append(mediainfo)
        else:
            self.debugBrowser.append("您的视频文件路径有误")

    def getNameButtonClicked(self):
        first_chinese_name = self.chineseNameEdit.text()
        if first_chinese_name:
            print('获取中文名成功：' + first_chinese_name)
            self.debugBrowser.append('获取中文名成功：' + first_chinese_name)
            first_english_name = chinese_name_to_pinyin(first_chinese_name)
            year = self.yearEdit.text()
            season = self.seasonBox.text()
            if len(season) < 2:
                season = '0' + season
            width = ""
            format = ""
            hdr_format = ""
            commercial_name = ""
            channel_layout = ""
            rename_file = get_settings("renameFile")
            isVideoPath, videoPath = check_path_and_find_video(self.videoPath.text())
            get_video_info_success, output = get_video_info(videoPath)
            print(get_video_info_success, output)
            if isVideoPath == 2:

                get_video_files_success, video_files = get_video_files(self.videoPath.text())
                print(video_files)
                print("获取到关键参数：" + str(output))
                self.debugBrowser.append("获取到关键参数：" + str(output))
                if get_video_info_success:
                    width = output[0]
                    format = output[1]
                    hdr_format = output[2]
                    commercial_name = output[3]
                    channel_layout = output[4]
                source = self.source.currentText()
                team = self.team.currentText()
                print("关键参数赋值成功")
                self.debugBrowser.append("关键参数赋值成功")
                type = self.type.currentText()
                category = self.get_selected_categories()
                mainTitle = first_english_name + ' ' + year + ' S' + season + ' ' + width + ' ' + source + ' ' + format + ' ' + hdr_format + ' ' + commercial_name + '' + channel_layout + '-' + team
                mainTitle = mainTitle.replace('  ', ' ')
                print(mainTitle)
                secondTitle = (first_chinese_name + ' | 全' + str(
                    len(video_files)) + '集 | ' + year + '年 | ' + type + ' | 类型：' + category)
                print("SecondTitle" + secondTitle)
                # NPC我要跟你谈恋爱 | 全95集 | 2023年 | 网络收费短剧 | 类型：剧集 爱情
                fileName = (
                        first_chinese_name + '.' + first_english_name + '.' + year + '.' + ' S' + season + 'E??' + '.' + width + '.' + source + '.' +
                        format + '.' + hdr_format + '.' + commercial_name + '' + channel_layout + '-' + team)
                fileName = fileName.replace(' – ', '.')
                fileName = fileName.replace(': ', '.')
                fileName = fileName.replace(' ', '.')
                fileName = fileName.replace('..', '.')
                print("FileName" + fileName)
                self.mainTitleBrowser.setText(mainTitle)
                self.secondTitleBrowser.setText(secondTitle)
                self.fileNameBrowser.setText(fileName)
                if rename_file:
                    print("对文件重新命名")
                    self.debugBrowser.append("开始对文件重新命名")
                    for video_file in video_files:
                        # 使用正则提取集数，分为2种情况，一种是E??，一种是???
                        # 先尝试使用E??提取,如果提取不到则更换???,否则退出
                        episode_number = 0
                        # 拆分出最后的文件名
                        _, file_base = os.path.split(video_file)
                        match_e = re.search(r'E(\d+)', file_base)
                        if match_e:
                            # 如果匹配成功，则提取集数
                            episode_number = match_e.group(1)
                        else:
                            # 如果使用E??提取不到，尝试使用纯数字匹配
                            match_digits = re.search(r'(\d+)', file_base)
                            if match_digits:
                                # 如果匹配成功，则提取集数
                                episode_number = match_digits.group(1)
                        if episode_number == 0:
                            # 如果集数为0，则退出
                            self.debugBrowser.append("提取集数失败，退出")
                            break
                        e = str(episode_number)
                        while len(e) < len(str(len(video_files))):
                            e = '0' + e
                        rename_file_success, output = rename_file_with_same_extension(video_file,
                                                                                      fileName.replace('??', e))

                        if rename_file_success:
                            self.videoPath.setText(output)
                            videoPath = output
                            self.debugBrowser.append("视频成功重新命名为：" + videoPath)
                        else:
                            self.debugBrowser.append("重命名失败：" + output)

                    print("对文件夹重新命名")
                    self.debugBrowser.append("开始对文件夹重新命名")
                    rename_directory_success, output = rename_directory(os.path.dirname(videoPath),
                                                                        fileName.replace('E??', ''))
                    if rename_directory_success:
                        self.videoPath.setText(output)
                        videoPath = output
                        self.debugBrowser.append("视频地址成功重新命名为：" + videoPath)
                    else:
                        self.debugBrowser.append("重命名失败：" + output)
            else:
                self.debugBrowser.append("您的视频文件路径有误")
        else:
            self.debugBrowser.append('获取中文名失败')

    def makeTorrentButtonClicked(self):
        isVideoPath, videoPath = check_path_and_find_video(self.videoPath.text())  # 视频资源的路径
        if isVideoPath == 1 or isVideoPath == 2:
            torrent_path = str(get_settings("torrentPath"))
            folder_path = os.path.dirname(videoPath)
            self.debugBrowser.append("开始将" + folder_path + "制作种子，储存在" + torrent_path)
            self.make_torrent_thread = MakeTorrentThread(folder_path, torrent_path)
            self.make_torrent_thread.result_signal.connect(self.handleMakeTorrentResult)  # 连接信号
            self.make_torrent_thread.start()  # 启动线程
            self.debugBrowser.append("制作种子线程启动成功")
        else:
            self.debugBrowser.append("制作种子失败：" + videoPath)

    def handleMakeTorrentResult(self, get_success, response):
        if get_success:
            self.debugBrowser.append("成功制作种子：" + response)
            self.torrent_path = response
        else:
            self.debugBrowser.append("制作种子失败：" + response)


class Settings(QDialog, Ui_Settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置界面

        # 绑定点击信号和槽函数
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.selectScreenshotPathButton.clicked.connect(self.selectScreenshotPathButtonClicked)
        self.selectTorrentPathButton.clicked.connect(self.selectTorrentPathButtonClicked)

    def saveButtonClicked(self):
        self.updateSettings()
        self.close()

    def cancelButtonClicked(self):
        self.close()

    def selectScreenshotPathButtonClicked(self):
        path = get_folder_path()
        if path != '':
            self.screenshotPath.setText(path)

    def selectTorrentPathButtonClicked(self):
        path = get_folder_path()
        if path != '':
            self.torrentPath.setText(path)

    def getSettings(self):
        self.screenshotPath.setText(str(get_settings("screenshotPath")))
        self.torrentPath.setText(str(get_settings("torrentPath")))
        self.figureBedPath.setText(get_settings("figureBedPath"))
        self.figureBedToken.setText(get_settings("figureBedToken"))
        self.screenshotNumber.setValue(int(get_settings("screenshotNumber")))
        self.screenshotThreshold.setValue(float(get_settings("screenshotThreshold")))
        self.screenshotStart.setValue(float(get_settings("screenshotStart")))
        self.screenshotEnd.setValue(float(get_settings("screenshotEnd")))
        self.getThumbnails.setChecked(bool(get_settings("getThumbnails")))
        self.rows.setValue(int(get_settings("rows")))
        self.cols.setValue(int(get_settings("cols")))
        self.autoUploadScreenshot.setChecked(bool(get_settings("autoUploadScreenshot")))
        self.pasteScreenshotUrl.setChecked(bool(get_settings("pasteScreenshotUrl")))
        self.deleteScreenshot.setChecked(bool(get_settings("deleteScreenshot")))
        self.makeDir.setChecked(bool(get_settings("makeDir")))
        self.renameFile.setChecked(bool(get_settings("renameFile")))
        self.cookie.setText(get_settings("cookie"))
        self.qbPath.setText(get_settings("qbPath"))
        self.qbUser.setText(get_settings("qbUser"))
        self.qbPasswd.setText(get_settings("qbPasswd"))
        self.resourcePath.setText(get_settings("resourcePath"))

    def updateSettings(self):
        update_settings("screenshotPath", self.screenshotPath.text())
        update_settings("torrentPath", self.torrentPath.text())
        update_settings("figureBedPath", self.figureBedPath.text())
        update_settings("figureBedToken", self.figureBedToken.text())
        update_settings("screenshotNumber", str(self.screenshotNumber.text()))
        update_settings("screenshotThreshold", str(self.screenshotThreshold.text()))
        update_settings("screenshotStart", str(self.screenshotStart.text()))
        update_settings("screenshotEnd", str(self.screenshotEnd.text()))
        update_settings("cookie", str(self.cookie.text()))
        update_settings("qbPath", str(self.qbPath.text()))
        update_settings("qbUser", str(self.qbUser.text()))
        update_settings("qbPasswd", str(self.qbPasswd.text()))
        update_settings("resourcePath",str(self.resourcePath.text()))
        if self.getThumbnails.isChecked():
            update_settings("getThumbnails", "True")
        else:
            update_settings("getThumbnails", "")
        update_settings("rows", str(self.rows.text()))
        update_settings("cols", str(self.cols.text()))
        if self.autoUploadScreenshot.isChecked():
            update_settings("autoUploadScreenshot", "True")
        else:
            update_settings("autoUploadScreenshot", "")
        if self.pasteScreenshotUrl.isChecked():
            update_settings("pasteScreenshotUrl", "True")
        else:
            update_settings("pasteScreenshotUrl", "")
        if self.deleteScreenshot.isChecked():
            update_settings("deleteScreenshot", "True")
        else:
            update_settings("deleteScreenshot", "")
        if self.makeDir.isChecked():
            update_settings("makeDir", "True")
        else:
            update_settings("makeDir", "")
        if self.renameFile.isChecked():
            update_settings("renameFile", "True")
        else:
            update_settings("renameFile", "")


class UploadPictureThread(QThread):
    # 创建一个信号，用于在数据处理完毕后与主线程通信
    result_signal = pyqtSignal(bool, dict, str, bool)

    def __init__(self, figureBedPath, figureBedToken, screenshot_path, is_cover):
        super().__init__()
        self.figureBedPath = figureBedPath
        self.figureBedToken = figureBedToken
        self.screenshot_path = screenshot_path
        self.is_cover = is_cover

    def run(self):
        try:
            # 这里放置耗时的HTTP请求操作
            upload_success, api_response = upload_screenshot(self.figureBedPath, self.figureBedToken,
                                                             self.screenshot_path)

            # 发送信号，包括请求的结果
            print("上传图床成功，开始返回结果")
            self.result_signal.emit(upload_success, api_response, self.screenshot_path, self.is_cover)
            print("返回结果成功")
            # self.result_signal(upload_success,api_response)
        except Exception as e:
            print(f"异常发生: {e}")
            self.result_signal.emit(False, f"异常发生: {e}", self.screenshot_path, self.is_cover)
            # 这里可以发射一个包含错误信息的信号


class UploadFreePictureThread(QThread):
    # 创建一个信号，用于在数据处理完毕后与主线程通信
    result_signal = pyqtSignal(bool, str, str, bool)

    def __init__(self, figureBedPath, figureBedToken, screenshot_path, is_cover):
        super().__init__()
        self.figureBedPath = figureBedPath
        self.figureBedToken = figureBedToken
        self.screenshot_path = screenshot_path
        self.is_cover = is_cover

    def run(self):
        try:
            # 这里放置耗时的HTTP请求操作
            upload_success, api_response = upload_free_screenshot(self.figureBedPath, self.figureBedToken,
                                                                  self.screenshot_path)

            # 发送信号，包括请求的结果
            print("上传图床成功，开始返回结果")
            self.result_signal.emit(upload_success, api_response, self.screenshot_path, self.is_cover)
            print("返回结果成功")
            # self.result_signal(upload_success,api_response)
        except Exception as e:
            print(f"异常发生: {e}")
            self.result_signal.emit(False, f"异常发生: {e}", self.screenshot_path, self.is_cover)
            # 这里可以发射一个包含错误信息的信号


class MakeTorrentThread(QThread):
    # 创建一个信号，用于在数据处理完毕后与主线程通信
    result_signal = pyqtSignal(bool, str)

    def __init__(self, folder_path, torrent_path):
        super().__init__()
        self.folder_path = folder_path
        self.torrent_path = torrent_path

    def run(self):
        try:
            # 这里放置耗时的制作torrent操作
            get_success, response = create_torrent(self.folder_path, self.torrent_path)

            # 发送信号
            print("Torrent请求成功，开始等待返回结果")
            self.result_signal.emit(get_success, response)
            print("返回结果成功")
            # self.result_signal(upload_success,api_response)
        except Exception as e:
            print(f"异常发生: {e}")
            # 这里可以发射一个包含错误信息的信号


class UploadThread(QThread):
    finished_signal = pyqtSignal(str)  # 信号，用于在上传完成时发送消息

    def __init__(self, cookie_str, torrent_path, mainTitle, secondTitle, introBrowser, chinese_name):
        super().__init__()
        self.cookie_str = cookie_str
        self.torrent_path = torrent_path
        self.mainTitle = mainTitle
        self.secondTitle = secondTitle
        self.introBrowser = introBrowser
        self.chinese_name = chinese_name

    def run(self):
        # 在这里执行上传操作
        torrent_url = upload(self.cookie_str, self.torrent_path, self.mainTitle, self.secondTitle, self.introBrowser,
                             self.chinese_name)

        self.finished_signal.emit(torrent_url)  # 发送上传完成的信号
