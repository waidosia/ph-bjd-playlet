import os
import re
import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication

from ui.mainwindow import Ui_Mainwindow
from . import logger
from .common import title_tem, medio_tem
from .mediainfo import get_media_info
from .rename import get_video_info
from .screenshot import upload_screenshot
from .setting import Settings
from .tool import get_settings, get_file_path, get_folder_path, check_path_and_find_video, create_torrent, load_names, \
    chinese_name_to_pinyin, \
    get_video_files, extract_and_get_thumbnails, rename_directory_if_needed, rename_video_files
from .upload import upload_tjupt, upload_agsv


def starui():
    app = QApplication(sys.argv)
    myMainwindow = MainWindow()
    myico = QIcon("static/apr-bjd.ico")
    myMainwindow.setWindowIcon(myico)
    myMainwindow.show()
    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"发生异常: {e}")
        print(f"发生异常: {e}")


class MainWindow(QMainWindow, Ui_Mainwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置界面
        self.mySettings = None

        self.get_pt_gen_thread = None
        self.get_pt_gen_for_name_thread = None
        self.upload_thread = None
        self.torrent_path = None

        self.tjuTorrentLink = None
        self.agsvTorrentLink = None
        self.peterTorrentLink = None
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
        self.sendTjuButton.clicked.connect(self.sendTjuClicked)
        self.sendAgsvButton.clicked.connect(self.sendAgsvClicked)
        self.sendPeterButton.clicked.connect(self.sendPeterClicked)
        self.seedMak.clicked.connect(self.seedMakClicked)
        self.makeTorrentButton.clicked.connect(self.makeTorrentButtonClicked)
        self.writeButton.clicked.connect(self.writeButtonClicked)

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

    def selectCoverFolderButtonClicked(self):
        path = get_file_path()
        self.coverPath.setText(path)

    def selectVideoFolderButtonClicked(self):
        path = get_folder_path()
        self.videoPath.setText(path)

    def clear_all_text_inputs(self):
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
        self.info.setText("")
        self.debugBrowser.append("所有输入框已清空")

    def get_selected_categories(self):
        categories = [
            '剧情', '爱情', '喜剧', '甜虐', '甜宠', '恐怖', '动作', '穿越', '重生', '逆袭', '科幻', '武侠', '都市', '古装'
        ]

        selected_categories = [categories[i] for i in range(len(categories)) if
                               getattr(self, f"checkBox_{i}").isChecked()]
        return ' '.join(selected_categories)

    def settingsClicked(self):  # click对应的槽函数
        self.mySettings = Settings()
        self.mySettings.getSettings()
        myico = QIcon("static/apr-bjd.ico")
        self.mySettings.setWindowIcon(myico)
        self.mySettings.show()

    def getPictureButtonClicked(self):
        getPicture = UploadImages(self)
        getPicture.getPictureButtonClicked()

    def uploadCoverButtonClicked(self):
        uploadCover = UploadImages(self)
        uploadCover.uploadCoverButtonClicked()

    def getNameButtonClicked(self):
        get_name = GetName(self)
        get_name.getNameButtonClicked()

    def makeTorrentButtonClicked(self):
        make_torrent = MakeTorrent(self)
        make_torrent.makeTorrentButtonClicked()

    def getMediaInfoButtonClicked(self):
        get_media_info = GetMediaInfo(self)
        get_media_info.getMediaInfoButtonClicked()

    def writeButtonClicked(self):
        write_file = WriteFile(self)
        write_file.writeButtonClicked()

    def sendTjuClicked(self):
        upload_handler = UploadHandler(self)
        upload_handler.sendTjuClicked()

    def sendAgsvClicked(self):
        upload_handler = UploadHandler(self)
        upload_handler.sendAgsvClicked()

    def sendPeterClicked(self):
        upload_handler = UploadHandler(self)
        upload_handler.sendPeterClicked()

    def seedMakClicked(self):
        seed_mak = SeedMak(self)
        seed_mak.seedMak()


class UploadImages(QObject):
    result_signal = pyqtSignal(bool, dict, str, bool, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.upload_cover_thread = None
        self.upload_picture_thread0 = None
        self.upload_picture_thread1 = None
        self.upload_picture_thread2 = None
        self.upload_picture_thread3 = None
        self.upload_picture_thread4 = None
        self.upload_picture_thread5 = None

    def uploadCoverButtonClicked(self):
        if self.parent.coverPath.text():
            self.parent.debugBrowser.append("上传封面" + self.parent.coverPath.text())
            figureBedPath = get_settings("figureBedPath")  # 图床地址
            figureBedToken = get_settings("figureBedToken")  # 图床Token
            self.upload_cover_thread = UploadPictureThread(figureBedPath, figureBedToken, self.parent.coverPath.text(),
                                                           True)
            self.upload_cover_thread.result_signal.connect(self.handleUploadPictureResult)  # 连接信号
            self.upload_cover_thread.start()  # 启动线程
            print("上传图床线程启动")
            self.parent.debugBrowser.append("上传图床线程启动")

    def getPictureButtonClicked(self):
        self.parent.pictureUrlBrowser.setText("")
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())

        if isVideoPath == 1 or isVideoPath == 2:
            self.parent.debugBrowser.append(f"获取视频 {videoPath} 的截图")
            self.parent.debugBrowser.append("参数获取成功，开始执行截图函数")

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

            screenshot_success, res = extract_and_get_thumbnails(videoPath, screenshotPath, screenshotNumber,
                                                                 screenshotThreshold, screenshotStart,
                                                                 screenshotEnd,
                                                                 getThumbnails, rows, cols)

            if screenshot_success:
                self.handle_screenshot_result(res, figureBedPath, figureBedToken, autoUploadScreenshot)
            else:
                self.parent.debugBrowser.append("截图失败: " + str(res))
        else:
            self.parent.debugBrowser.append("您的视频文件路径有误")

    def handle_screenshot_result(self, res, figureBedPath, figureBedToken, autoUploadScreenshot):
        self.parent.debugBrowser.append("成功获取截图：" + str(res))

        if autoUploadScreenshot:
            self.parent.debugBrowser.append(f"开始自动上传截图到图床 {figureBedPath}")
            self.parent.pictureUrlBrowser.setText("")
            for i, screenshot in enumerate(res[:6]):  # 限制上传至多6张截图
                self.upload_screenshot(figureBedPath, figureBedToken, screenshot, False, index=i)
            self.parent.debugBrowser.append("上传图床线程启动")
        else:
            self.parent.debugBrowser.append("未选择自动上传图床功能，图片已储存在本地")
            output = "\n".join(res)
            self.parent.pictureUrlBrowser.setText(output)

    def upload_screenshot(self, figureBedPath, figureBedToken, screenshot, is_cover, index):
        thread_class = UploadPictureThread
        upload_thread = thread_class(figureBedPath, figureBedToken, screenshot, is_cover)
        upload_thread.result_signal.connect(lambda success, api_response, path=screenshot: self.handle_upload_result(
            success, api_response, path, is_cover, self.paste_url_cover if is_cover else self.paste_url_image))
        setattr(self, f"upload_picture_thread{index}", upload_thread)
        upload_thread.start()

    def handle_upload_result(self, upload_success, api_response, screenshot_path, is_cover, paste_url_callback):
        print("接受到线程请求的结果")
        self.parent.debugBrowser.append("接受到线程请求的结果")
        pasteScreenshotUrl = bool(get_settings("pasteScreenshotUrl"))
        deleteScreenshot = bool(get_settings("deleteScreenshot"))
        if upload_success:
            if api_response.get("statusCode", "") == "200":
                bbsurl = str(api_response.get("bbsurl", ""))
                self.parent.pictureUrlBrowser.append(bbsurl)
                api_response = bbsurl
            else:
                if api_response.get("statusCode", "") == "":
                    self.parent.debugBrowser.append("未接受到图床的任何响应" + '\n')
                else:
                    self.parent.debugBrowser.append(str(api_response) + '\n')
            if pasteScreenshotUrl:
                if is_cover:
                    category = self.parent.get_selected_categories()
                    print('类型为：' + category)
                    text = title_tem.format(api_response, self.parent.chineseNameEdit.text(),
                                            self.parent.yearEdit.text(), category,
                                            self.parent.info.text())
                    self.parent.introBrowser.append(text)
                    self.parent.debugBrowser.append("成功将封面链接粘贴到简介前")
                else:
                    paste_url_callback(api_response)
                    self.parent.debugBrowser.append("成功将图片链接粘贴到简介后")
                if deleteScreenshot:
                    self.delete_screenshot(screenshot_path)

        else:
            self.parent.debugBrowser.append("图床响应不是有效的JSON格式")

    def paste_url_cover(self, api_response):
        self.parent.introBrowser.append(api_response)
        self.parent.debugBrowser.append("成功将封面链接粘贴到简介前")

    def paste_url_image(self, api_response):
        self.parent.introBrowser.append(api_response)
        self.parent.debugBrowser.append("成功将图片链接粘贴到简介后")

    def delete_screenshot(self, screenshot_path):
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            print(f"文件 {screenshot_path} 已被删除。")
            self.parent.debugBrowser.append(f"文件 {screenshot_path} 已被删除。")
        else:
            print(f"文件 {screenshot_path} 不存在。")
            self.parent.debugBrowser.append(f"文件 {screenshot_path} 不存在。")

    def handleUploadPictureResult(self, upload_success, api_response, screenshot_path, is_cover, error):
        if error != "":
            self.parent.debugBrowser.append("上传失败：" + error)
        self.handle_upload_result(upload_success, api_response, screenshot_path, is_cover, self.paste_url_cover)


class GetName:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def getNameButtonClicked(self):
        first_chinese_name = self.parent.chineseNameEdit.text()
        if not first_chinese_name:
            self.parent.debugBrowser.append('获取中文名失败')
            return

        print('获取中文名成功：' + first_chinese_name)
        self.parent.debugBrowser.append('获取中文名成功：' + first_chinese_name)

        first_english_name = chinese_name_to_pinyin(first_chinese_name)
        year = self.parent.yearEdit.text()
        season = self.parent.seasonBox.text().zfill(2)

        width = ""
        format = ""
        hdr_format = ""
        commercial_name = ""
        channel_layout = ""
        rename_file = get_settings("renameFile")
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())
        get_video_info_success, output = get_video_info(videoPath)
        print(get_video_info_success, output)

        if isVideoPath != 2:
            self.parent.debugBrowser.append("您的视频文件路径有误")
            return

        video_files = get_video_files(self.parent.videoPath.text())
        print(video_files)
        print("获取到关键参数：" + str(output))
        self.parent.debugBrowser.append("获取到关键参数：" + str(output))

        if videoPath is not None:
            width, format, hdr_format, commercial_name, channel_layout = output[:5]

        source = self.parent.source.currentText()
        team = self.parent.team.currentText()
        type = self.parent.type.currentText()
        category = self.parent.get_selected_categories()

        main_title = f"{first_english_name} {year} S{season} {width} {source} {format} {hdr_format} {commercial_name}{channel_layout}-{team}"
        main_title = ' '.join(main_title.split())
        print(main_title)

        second_title = f"{first_chinese_name} | 全{len(video_files)}集 | {year}年 | {type} | 类型：{category}"
        print("SecondTitle" + second_title)

        file_name = f"{first_chinese_name}.{first_english_name}.{year} S{season}E??.{width}.{source}.{format}.{hdr_format}.{commercial_name}{channel_layout}-{team}"
        file_name = file_name.replace(' – ', '.').replace(': ', '.').replace(' ', '.').replace('..', '.')
        print("FileName" + file_name)

        self.parent.mainTitleBrowser.setText(main_title)
        self.parent.secondTitleBrowser.setText(second_title)
        self.parent.fileNameBrowser.setText(file_name)

        if rename_file:
            print("对文件重新命名")
            self.parent.debugBrowser.append("开始对文件重新命名")

            renamed_files = rename_video_files(video_files, file_name)
            for renamed_file in renamed_files:
                if renamed_file:
                    self.parent.videoPath.setText(renamed_file)
                    videoPath = renamed_file
                    self.parent.debugBrowser.append("视频成功重新命名为：" + videoPath)
                else:
                    self.parent.debugBrowser.append("重命名失败：" + output)

            print("对文件夹重新命名")
            self.parent.debugBrowser.append("开始对文件夹重新命名")

            renamed_directory = rename_directory_if_needed(videoPath, file_name)
            if renamed_directory:
                self.parent.videoPath.setText(renamed_directory)
                videoPath = renamed_directory
                self.parent.debugBrowser.append("视频地址成功重新命名为：" + videoPath)
            else:
                self.parent.debugBrowser.append("重命名失败：" + output)


class WriteFile:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def writeButtonClicked(self):
        # 中文标题
        chinese_name = self.parent.chineseNameEdit.text() + ".txt"
        # 主标题
        mainTitle = self.parent.mainTitleBrowser.toPlainText().replace(' ', '.')
        # 副标题
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        # 简介
        introBrowser = self.parent.introBrowser.toPlainText()
        # 获取保存目录
        video_info = get_settings("vedioInfo")
        # 拼接文件路径
        file_path = os.path.join(video_info, chinese_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f'主标题为： {mainTitle}\n')
                file.write(f'副标题为： {secondTitle}\n')
                file.write(f'简介为： \n{introBrowser}\n')
            self.parent.clear_all_text_inputs()
        except Exception as e:
            self.parent.debugBrowser.append(f"发生异常: {e}")
            self.parent.clear_all_text_inputs()


class GetMediaInfo(MainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def getMediaInfoButtonClicked(self):
        self.parent.mediainfoBrowser.setText("")
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())  # 视频资源的路径
        if isVideoPath == 1 or isVideoPath == 2:
            get_media_info_success, mediainfo = get_media_info(videoPath)
            if get_media_info_success:
                self.parent.mediainfoBrowser.setText(mediainfo)
                mediainfo_text = medio_tem.format(mediainfo)
                self.parent.introBrowser.append(mediainfo_text)
                self.parent.debugBrowser.append("成功获取到MediaInfo")
            else:
                self.parent.debugBrowser.append("获取MediaInfo失败,请重试")
        else:
            self.parent.debugBrowser.append("您的视频文件路径有误")


class MakeTorrent(QObject):
    result_signal = pyqtSignal(bool, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.make_torrent_thread = None

    def makeTorrentButtonClicked(self):
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())  # 视频资源的路径
        if isVideoPath == 1 or isVideoPath == 2:
            torrent_path = str(get_settings("torrentPath"))
            folder_path = os.path.dirname(videoPath)
            self.parent.debugBrowser.append("开始将" + folder_path + "制作种子，储存在" + torrent_path)
            self.make_torrent_thread = MakeTorrentThread(folder_path, torrent_path)
            self.make_torrent_thread.result_signal.connect(self.handleMakeTorrentResult)  # 连接信号
            self.make_torrent_thread.start()
            self.parent.debugBrowser.append("制作种子线程启动成功")
        else:
            self.parent.debugBrowser.append("制作种子失败：" + videoPath)

    def handleMakeTorrentResult(self, get_success, response, error):
        print("开始处理制作后的逻辑")
        if error == "":
            if get_success:
                self.parent.debugBrowser.append("成功制作种子：" + response)
                self.parent.torrent_path = response
            else:
                self.parent.debugBrowser.append("制作种子失败：" + response)
        else:
            logger.error(f"发生异常: {error}")


class UploadHandler:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def sendTjuClicked(self):
        self.parent.debugBrowser.append("开始上传种子到TJUPT")
        cookie_str = get_settings("tjuCookie")
        mainTitle = self.parent.mainTitleBrowser.toPlainText().replace(' ', '.')
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        introBrowser = self.parent.introBrowser.toPlainText()
        chinese_name = self.parent.chineseNameEdit.text()
        torrent_path = self.parent.torrent_path
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        upload_success,tju_link = upload_tjupt(cookie_str, torrent_path, mainTitle, secondTitle, introBrowser, chinese_name)
        if upload_success:
            self.parent.tjuTorrentLink = tju_link
            self.parent.debugBrowser.append("上传种子到TJUPT成功,种子链接为："+tju_link)
        else:
            self.parent.debugBrowser.append("上传种子到TJUPT失败，失败原因为："+tju_link)

    def sendAgsvClicked(self):
        self.parent.debugBrowser.append("开始上传种子到agsv")
        cookie_str = get_settings("agsvCookie")
        mainTitle = self.parent.mainTitleBrowser.toPlainText().replace('.', ' ')
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        introBrowser = self.parent.introBrowser.toPlainText()
        # 去除指定一段落的内容

        modified_content = re.sub(
            r'\[img\]https://img.pterclub.com/images/2024/01/10/49401952f8353abd4246023bff8de2cc.png\[/img\].*?\[mediainfo\].*?\[/mediainfo\]',
            '', introBrowser, flags=re.DOTALL)
        media_info = self.parent.mediainfoBrowser.toPlainText()
        torrent_path = self.parent.torrent_path
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        upload_success, agsv_link = upload_agsv(cookie_str, torrent_path, mainTitle, secondTitle, modified_content,
                                                media_info)
        if upload_success:
            self.parent.agsvTorrentLink = agsv_link
            self.parent.debugBrowser.append("上传种子到agsv成功,种子链接为：" + agsv_link)
        else:
            self.parent.debugBrowser.append("上传种子到agsv失败，失败原因为：" + agsv_link)

    def sendPeterClicked(self):
        self.parent.debugBrowser.append("开始上传种子到Pter")
        self.parent.peterTorrentLink = "Pter"
        self.parent.debugBrowser.append("上传种子到Pter成功")


class SeedMak:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def seedMak(self):
        self.parent.debugBrowser.append(f"开始做种Tju:{self.parent.tjuTorrentLink}")
        self.parent.debugBrowser.append(f"开始做种Agsv:{self.parent.agsvTorrentLink}")
        self.parent.debugBrowser.append(f"开始做种Pter:{self.parent.peterTorrentLink}")


class UploadPictureThread(QThread):
    # 创建一个信号，用于在数据处理完毕后与主线程通信
    result_signal = pyqtSignal(bool, dict, str, bool, str)

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
            self.result_signal.emit(upload_success, api_response, self.screenshot_path, self.is_cover, "")
            print("返回结果成功")
        except Exception as e:
            print(f"异常发生: {e}")
            self.result_signal.emit(False, f"错误消息为：{e}", self.screenshot_path, self.is_cover, str(e))


class MakeTorrentThread(QThread):
    # 创建一个信号，用于在数据处理完毕后与主线程通信
    result_signal = pyqtSignal(bool, str, str)

    def __init__(self, folder_path, torrent_path, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.torrent_path = torrent_path

    def run(self):
        try:
            # 这里放置耗时的制作torrent操作
            get_success, response = create_torrent(self.folder_path, self.torrent_path)
            # 发送信号
            print("Torrent请求成功，开始等待返回结果")
            self.result_signal.emit(get_success, response, "")
            print("返回结果成功")
        except Exception as e:
            logger.error("制作种子出现异常")
            print(f"异常发生: {e}")
            self.result_signal.emit(False, f"异常发生: {e}", str(e))

# class UploadThread(QThread):
#     finished_signal = pyqtSignal(str, str)  # 信号，用于在上传完成时发送消息
#
#     def __init__(self, cookie_str, torrent_path, mainTitle, secondTitle, introBrowser, chinese_name):
#         super().__init__()
#         self.cookie_str = cookie_str
#         self.torrent_path = torrent_path
#         self.mainTitle = mainTitle
#         self.secondTitle = secondTitle
#         self.introBrowser = introBrowser
#         self.chinese_name = chinese_name
#
#     def run(self):
#         # 在这里执行上传操作
#         try:
#             torrent_url = upload(self.cookie_str, self.torrent_path, self.mainTitle, self.secondTitle,
#                                  self.introBrowser,
#                                  self.chinese_name)
#             self.finished_signal.emit(torrent_url, "")  # 发送上传完成的信号
#         except Exception as e:
#             print(f"异常发生: {e}")
#             # 这里可以发射一个包含错误信息的信号
#             self.finished_signal.emit("", str(e))
