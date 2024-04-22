import os
import re
import shutil
import sys
import time
from pathlib import Path

from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog

from ui.mainwindow import Ui_Mainwindow
from util.festival import get_festival_blessing
from util.log import logger
from .common import title_tem, medio_tem, prohibit
from .mediainfo import get_media_info
from .ptgen import fetch_and_format_ptgen_data
from .rename import get_video_info
from .screenshot import upload_screenshot
from .seed import qb_download, tr_download
from .setting import Settings
from .tool import get_settings, get_file_path, get_folder_path, check_path_and_find_video, create_torrent, load_names, \
    chinese_name_to_pinyin, \
    get_video_files, extract_and_get_thumbnails, rename_directory_if_needed, rename_video_files, \
    replace_fullwidth_symbols
from .upload.agsv import upload_agsv
from .upload.kylin import upload_kylin
from .upload.pter import upload_pter
from .upload.red_leaves import upload_red_leaves
from .upload.tjupt import upload_tjupt


def starui():
    logger.info("程序启动")
    app = QApplication(sys.argv)
    myMainwindow = MainWindow()
    myico = QIcon("static/playlet.ico")
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

        self.tjuTorrentLink = None
        self.agsvTorrentLink = None
        self.peterTorrentLink = None
        self.kylinTorrentLink = None
        self.redLeavesTorrentLink = None
        self.tjuTorrentPath = None
        self.agsvTorrentPath = None
        self.peterTorrentPath = None
        self.kylinTorrentPath = None
        self.redLeavesTorrentPath = None

        self.english_name = ""
        self.category = None
        self.names = None
        self.seed_start = 0

        self.progress = 100
        # 初始化
        self.videoPath.setDragEnabled(True)
        self.introBrowser.setText("")
        self.pictureUrlBrowser.setText("")
        self.mediainfoBrowser.setText("")
        self.debugBrowser.setText("")
        self.initialize_team_combobox()
        self.initialize_source_combobox()
        self.initialize_type_combobox()
        self.feed.setChecked(True)

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
        self.sendredLeavesButton.clicked.connect(self.sendredLeavesClicked)
        self.sendKylinButton.clicked.connect(self.sendKylinClicked)
        self.seedMak.clicked.connect(self.seedMakClicked)
        self.clear.clicked.connect(self.clear_all_text_inputs)
        self.makeTorrentButton.clicked.connect(self.makeTorrentButtonClicked)
        self.writeButton.clicked.connect(self.writeButtonClicked)
        self.generateButtot.clicked.connect(self.getPtGenClicked)

        self.debugBrowser.append("程序初始化成功，使用前请查看设置中的说明")
        logger.info("程序初始化成功")

    def initialize_team_combobox(self):
        team_names = load_names('static/team.json', 'team')
        for name in team_names:
            self.team.addItem(name)
        logger.info(f"加载团队名称")

    def initialize_source_combobox(self):
        source_names = load_names('static/source.json', 'source')
        for name in source_names:
            self.source.addItem(name)
        logger.info(f"加载资源来源")

    def initialize_type_combobox(self):
        type_names = load_names('static/type.json', 'type')
        for name in type_names:
            self.type.addItem(name)
        logger.info(f"加载资源类型")

    def selectCoverFolderButtonClicked(self):
        path = get_file_path()
        logger.info(f"选择封面文件夹：{path}")
        self.coverPath.setText(path)

    def selectVideoFolderButtonClicked(self):
        path = get_folder_path()
        logger.info(f"选择视频文件夹：{path}")
        self.videoPath.setText(path)

    def clear_all_text_inputs(self):
        # 加入问询框，是否确认清空
        reply = QMessageBox.question(self, "确认", "是否确认清空所有输入框？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        self.ptGen.setText("")
        self.videoPath.setText("")
        self.coverPath.setText("")
        self.mainTitleBrowser.setText("")
        self.secondTitleBrowser.setText("")
        self.introBrowser.setText("")
        self.pictureUrlBrowser.setText("")
        self.mediainfoBrowser.setText("")
        self.torrentPathBrowser.setText("")
        self.chineseNameEdit.setText("")
        self.yearEdit.setText("")
        self.info.setText("")
        self.coverUrl.setText("")
        self.tjuTorrentLink = None
        self.agsvTorrentLink = None
        self.peterTorrentLink = None
        self.kylinTorrentLink = None
        self.redLeavesTorrentPath = None
        self.tjuTorrentPath = None
        self.agsvTorrentPath = None
        self.peterTorrentPath = None
        self.kylinTorrentPath = None
        self.progress = 100
        self.debugBrowser.append("所有输入框已清空")
        logger.info("所有输入框已清空")

    def get_selected_categories(self):
        categories = [
            '剧情', '爱情', '喜剧', '甜虐', '甜宠', '恐怖', '动作', '穿越', '重生', '逆袭', '科幻', '武侠', '都市', '古装'
        ]

        selected_categories = [categories[i] for i in range(len(categories)) if
                               getattr(self, f"checkBox_{i}").isChecked()]

        logger.info(f"选择的类型为：{selected_categories}")

        return ' '.join(selected_categories)

    def settingsClicked(self):  # click对应的槽函数
        self.mySettings = Settings()
        self.mySettings.getSettings()
        myico = QIcon("static/playlet.ico")
        self.mySettings.setWindowIcon(myico)
        self.mySettings.show()

    def getPictureButtonClicked(self):
        getPicture = UploadImages(self)
        logger.info("点击获取截图按钮")
        getPicture.getPictureButtonClicked()

    def uploadCoverButtonClicked(self):
        uploadCover = UploadImages(self)
        logger.info("点击上传封面按钮")
        uploadCover.uploadCoverButtonClicked()

    def getNameButtonClicked(self):
        get_name = GetName(self)
        logger.info("点击获取名称按钮")
        get_name.getNameButtonClicked()

    def makeTorrentButtonClicked(self):
        make_torrent = MakeTorrent(self)
        logger.info("点击制作种子按钮")
        make_torrent.makeTorrentButtonClicked()

    def getMediaInfoButtonClicked(self):
        get_media_info = GetMediaInfo(self)
        logger.info("点击获取MediaInfo按钮")
        get_media_info.getMediaInfoButtonClicked()

    def writeButtonClicked(self):
        write_file = WriteFile(self)
        logger.info("点击写入文件按钮")
        write_file.writeButtonClicked()

    def getPtGenClicked(self):
        get_pt_gen = GetPtGen(self)
        logger.info("点击获取PTGen按钮")
        get_pt_gen.getPtGenClicked()

    def sendTjuClicked(self):
        upload_handler = UploadHandler(self)
        logger.info("点击上传TJUPT按钮")
        upload_handler.sendTjuClicked()

    def sendAgsvClicked(self):
        upload_handler = UploadHandler(self)
        logger.info("点击上传agsv按钮")
        upload_handler.sendAgsvClicked()

    def sendPeterClicked(self):
        upload_handler = UploadHandler(self)
        logger.info("点击上传Pter按钮")
        upload_handler.sendPeterClicked()

    def sendKylinClicked(self):
        upload_handler = UploadHandler(self)
        logger.info("点击上传Kylin按钮")
        upload_handler.sendKylinClicked()

    def sendredLeavesClicked(self):
        upload_handler = UploadHandler(self)
        logger.info("点击上传redLeaves按钮")
        upload_handler.sendredLeavesClicked()

    def seedMakClicked(self):
        if self.progress != 100:
            QMessageBox.warning(self, "警告", "文件移动未完成", QMessageBox.StandardButton.Ok)
            return

        seed_mak = SeedMak(self)
        logger.info("点击做种按钮")
        # 判断选择的是qb还是tr
        seed_type = get_settings("buttonGroup")
        if seed_type == "-2":
            self.debugBrowser.append("选择的是qb")
            logger.info("选择的是qb")
            seed_mak.seed_qb()
        elif seed_type == "-3":
            self.debugBrowser.append("选择的是tr")
            logger.error("选择的是tr")
            seed_mak.seed_tr()
        else:
            print("未选择做种类型")
            self.debugBrowser.append("未选择做种类型")
            logger.error("未选择做种类型")


class UploadImages(QObject):
    result_signal = pyqtSignal(bool, dict, str, bool, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.upload_cover_thread = None
        self.upload_picture_threads = []
        self.finished_threads = 0

    def uploadCoverButtonClicked(self):
        # 点击上传封面按钮，需要同时判断中文名称，年份，简介与类型是否填写
        if not self.parent.ptGen.text():
            if not self.parent.chineseNameEdit.text() or not self.parent.yearEdit.text() or not self.parent.info.text():
                # 弹出警告框
                QMessageBox.warning(self.parent, "警告", "请先填写中文名，年份，简介", QMessageBox.StandardButton.Ok)
                return
            # 判断是否选择了类型
            if not self.parent.get_selected_categories():
                QMessageBox.warning(self.parent, "警告", "请先选择类型", QMessageBox.StandardButton.Ok)
                return

        if self.parent.coverPath.text():
            logger.info(f"上传封面{self.parent.coverPath.text()}")
            self.parent.debugBrowser.append("上传封面" + self.parent.coverPath.text())
            figureBedPath = get_settings("figureBedPath")  # 图床地址
            figureBedToken = get_settings("figureBedToken")  # 图床Token
            self.upload_cover_thread = UploadPictureThread(figureBedPath, figureBedToken, self.parent.coverPath.text(),
                                                           True)
            self.upload_cover_thread.result_signal.connect(self.handleUploadPictureResult)  # 连接信号
            self.upload_cover_thread.start()  # 启动线程
            logger.info("上传图床线程启动")
            self.parent.debugBrowser.append("上传图床线程启动")
        else:
            # 弹出警告框
            QMessageBox.warning(self.parent, "警告", "请先选择封面文件夹", QMessageBox.StandardButton.Ok)

    def getPictureButtonClicked(self):
        if not self.parent.videoPath.text():
            QMessageBox.warning(self.parent, "警告", "请先选择视频文件夹", QMessageBox.StandardButton.Ok)
            return
        self.parent.pictureUrlBrowser.setText("")
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())

        if isVideoPath == 1 or isVideoPath == 2:
            self.parent.debugBrowser.append(f"获取视频 {videoPath} 的截图")
            self.parent.debugBrowser.append("参数获取成功，开始执行截图函数")
            logger.info(f"获取视频 {videoPath} 的截图")

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

            screenshot_success, images = extract_and_get_thumbnails(videoPath, screenshotPath, screenshotNumber,
                                                                    screenshotThreshold, screenshotStart,
                                                                    screenshotEnd,
                                                                    getThumbnails, rows, cols)

            if screenshot_success:
                self.handle_screenshot_result(images, figureBedPath, figureBedToken, autoUploadScreenshot)
                logger.info(f"截图成功")
            else:
                self.parent.debugBrowser.append("截图失败: ")
                logger.error(f"截图失败")

        else:
            self.parent.debugBrowser.append("您的视频文件路径有误")
            logger.error(f"您的视频文件路径有误")

    def handle_screenshot_result(self, images, figureBedPath, figureBedToken, autoUploadScreenshot):
        self.parent.debugBrowser.append("成功获取截图：" + str(images['screenshot']))
        logger.info(f"成功获取截图：{images['screenshot']}")

        if autoUploadScreenshot:
            self.parent.debugBrowser.append(f"开始自动上传截图到图床 {figureBedPath}")
            logger.info(f"开始自动上传截图到图床 {figureBedPath}")
            self.parent.pictureUrlBrowser.setText("")
            self.upload_picture_threads = []  # 清空之前的上传线程列表
            for i, screenshot in enumerate(images['screenshot'][:6]):  # 限制上传至多6张截图
                upload_thread = UploadPictureThread(figureBedPath, figureBedToken, screenshot, False)
                upload_thread.result_signal.connect(self.handleUploadPictureResult)  # 连接信号
                self.upload_picture_threads.append(upload_thread)
                upload_thread.start()
                time.sleep(0.5)
            # 单独上传最后的缩略图
            if images.get("thumbnails") != "":
                self.parent.debugBrowser.append(f"开始上传缩略图 {images['thumbnails']}")
                if images['thumbnails'] != "":
                    upload_thread = UploadPictureThread(figureBedPath, figureBedToken, images['thumbnails'], False)
                    upload_thread.result_signal.connect(self.handleUploadPictureResult)
                    self.upload_picture_threads.append(upload_thread)
                    upload_thread.start()
            else:
                self.parent.debugBrowser.append(f"未获取到缩略图")
            self.parent.debugBrowser.append("上传图床线程启动")
        else:
            self.parent.debugBrowser.append("未选择自动上传图床功能，图片已储存在本地")
            logger.info("未选择自动上传图床功能，图片已储存在本地")
            output = "\n".join(images['screenshot'])
            self.parent.pictureUrlBrowser.setText(output)

    def handle_upload_result(self, upload_success, api_response, screenshot_path, is_cover):
        print("接受到线程请求的结果")
        logger.info("接受到线程请求的结果")
        self.parent.debugBrowser.append("接受到线程请求的结果")
        pasteScreenshotUrl = bool(get_settings("pasteScreenshotUrl"))
        deleteScreenshot = bool(get_settings("deleteScreenshot"))
        bbsurl = ""
        if upload_success:
            if api_response.get("statusCode", "") == "200":
                bbsurl = str(api_response.get("bbsurl", ""))
                self.parent.pictureUrlBrowser.append(bbsurl)
                logger.info(f"成功上传截图到图床 {bbsurl}")
            else:
                if api_response.get("statusCode", "") == "":
                    self.parent.debugBrowser.append("未接受到图床的任何响应" + '\n')
                    logger.error("未接受到图床的任何响应")
                else:
                    self.parent.debugBrowser.append(str(api_response) + '\n')
            if pasteScreenshotUrl:
                if bbsurl != "":
                    if is_cover:
                        # 如果ptgen不为空，且introBrowser存在内容，将封面链接替换原有封面链接
                        if self.parent.ptGen.text() != "" and self.parent.introBrowser.toPlainText() != "":
                            # 替换封面链接
                            intro_text = self.parent.introBrowser.toPlainText()
                            intro_text = re.sub(r"\[img\].*?\[\/img\]", f"{bbsurl}", intro_text, 1)
                            self.parent.introBrowser.setText("")
                            self.parent.introBrowser.setText(intro_text)
                        else:
                            text = ""
                            if self.parent.feed.isChecked():
                                text = prohibit
                            category = self.parent.get_selected_categories()
                            print('类型为：' + category)
                            text = text + title_tem.format(bbsurl, self.parent.chineseNameEdit.text(),
                                                           self.parent.yearEdit.text(), category,
                                                           self.parent.info.text())
                            self.parent.introBrowser.append(text)
                            self.parent.debugBrowser.append("成功将封面链接粘贴到简介前")
                            logger.info("成功将封面链接粘贴到简介前")
                    else:
                        self.parent.introBrowser.append(bbsurl)
                        self.parent.debugBrowser.append("成功将图片链接粘贴到简介后")
                        logger.info("成功将封面链接粘贴到简介后")
                    if deleteScreenshot:
                        self.delete_screenshot(screenshot_path)
                    self.parent.coverUrl.setText(bbsurl)

        else:
            self.parent.debugBrowser.append("图床响应不是有效的JSON格式")
            logger.error("图床响应不是有效的JSON格式")

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
        if not is_cover:
            self.finished_threads += 1
            if self.finished_threads == len(self.upload_picture_threads):
                # 所有线程都已完成
                self.allThreadsFinished()
        self.handle_upload_result(upload_success, api_response, screenshot_path, is_cover)

    def allThreadsFinished(self):
        # 所有线程都已完成，进行页面提示
        self.finished_threads = 0
        self.parent.debugBrowser.append("所有图片上传完成")


class GetName(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.move_file_thread = None

    def getNameButtonClicked(self):
        # 针对PTGen的处理，如果可以，从PTGen获取中文名，年份，简介，类型
        if not self.parent.ptGen.text():
            # 如果没有中文名，年份，类型，资源路径 点击获取名称按钮会弹出警告框
            if not self.parent.chineseNameEdit.text() or not self.parent.yearEdit.text():
                QMessageBox.warning(self.parent, "警告", "请先填写中文名，年份", QMessageBox.StandardButton.Ok)
                return
            if not self.parent.get_selected_categories():
                QMessageBox.warning(self.parent, "警告", "请先选择类型", QMessageBox.StandardButton.Ok)
                return
        if not self.parent.videoPath.text():
            QMessageBox.warning(self.parent, "警告", "请先选择视频文件夹", QMessageBox.StandardButton.Ok)
            return
        if self.parent.ptGen.text() and not self.parent.chineseNameEdit.text():
            QMessageBox.warning(self.parent, "警告", "请先点击PTGen生成按钮", QMessageBox.StandardButton.Ok)
            return

        # 弹窗判断英文名是否正确，不正确则允许修改，同时获取修改后的值
        first_chinese_name = self.parent.chineseNameEdit.text()
        self.parent.debugBrowser.append('获取中文名成功：' + first_chinese_name)
        first_english_name = self.parent.english_name
        if first_english_name == "":
            first_english_name = chinese_name_to_pinyin(first_chinese_name)
        # 弹窗显示英文名，并允许修改
        first_english_name, ok = QInputDialog.getText(self.parent, "验证英文名", "英文名:", text=first_english_name)
        if not ok:
            return
        logger.info('获取英文名成功：' + first_english_name)

        # 对英文名中的全角符号进行替换
        first_english_name = replace_fullwidth_symbols(first_english_name)
        first_english_name = first_english_name.replace('.', ' ')
        self.parent.debugBrowser.append('获取英文名成功：' + first_english_name)
        logger.info('获取英文名成功：' + first_english_name)

        year = self.parent.yearEdit.text()
        season = self.parent.seasonBox.text().zfill(2)

        width = ""
        format = ""
        hdr_format = ""
        commercial_name = ""
        channel_layout = ""
        rename_file = get_settings("renameFile")
        move_file = get_settings("moveFile")
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())
        get_video_info_success, output = get_video_info(videoPath)
        print(get_video_info_success, output)

        if isVideoPath != 2:
            self.parent.debugBrowser.append("您的视频文件路径有误")
            logger.error("您的视频文件路径有误")
            return

        video_files = get_video_files(self.parent.videoPath.text())
        print(video_files)
        self.parent.debugBrowser.append("获取到关键参数：" + str(output))

        if videoPath is not None:
            width, format, hdr_format, commercial_name, channel_layout = output[:5]

        source = self.parent.source.currentText()
        team = self.parent.team.currentText()
        type = self.parent.type.currentText()
        category = self.parent.get_selected_categories()

        main_title = f"{first_english_name} {year} S{season} {width} {source} {format} {hdr_format} {commercial_name}{channel_layout}-{team}"
        main_title = ' '.join(main_title.split())

        festival = get_festival_blessing()
        print(main_title)

        # 副标题生成时，需根据内容不同，生成不同的副标题
        if self.parent.ptGen.text():
            category = ' / '.join(self.parent.category)
            names = ' / '.join(self.parent.names)
            second_title = f"{first_chinese_name} | 全{len(video_files)}集 | {year}年 | {type} | 类型：{category} | 演员：{names} {festival}"
        else:
            second_title = f"{first_chinese_name} | 全{len(video_files)}集 | {year}年 | {type} | 类型：{category} {festival}"
        print("SecondTitle" + second_title)

        file_name = f"{first_chinese_name}.{first_english_name}.{year} S{season}E??.{width}.{source}.{format}.{hdr_format}.{commercial_name}{channel_layout}-{team}"
        file_name = file_name.replace(' – ', '.').replace(': ', '.').replace(' ', '.').replace('..', '.')
        print("FileName" + file_name)

        self.parent.mainTitleBrowser.setText(main_title)
        self.parent.secondTitleBrowser.setText(second_title)

        if rename_file:
            self.parent.debugBrowser.append("开始对文件重新命名")
            logger.info("开始对文件重新命名")

            renamed_files = rename_video_files(video_files, file_name)
            for renamed_file in renamed_files:
                if renamed_file:
                    # self.parent.videoPath.setText(renamed_file)
                    videoPath = renamed_file
                    self.parent.debugBrowser.append("视频成功重新命名为：" + videoPath)
                    logger.info("视频成功重新命名为：" + videoPath)
                else:
                    self.parent.debugBrowser.append("重命名失败")
                    logger.error("重命名失败")
                    return

            logger.info("对文件夹重新命名")
            self.parent.debugBrowser.append("开始对文件夹重新命名")

            renamed_directory = rename_directory_if_needed(videoPath, file_name)
            if renamed_directory:
                self.parent.videoPath.setText(renamed_directory)
                videoPath = renamed_directory
                self.parent.debugBrowser.append("视频地址成功重新命名为：" + videoPath)
                logger.info("视频地址成功重新命名为：" + videoPath)
            else:
                self.parent.debugBrowser.append("重命名失败：")
                logger.error("重命名失败")
                return

        if move_file:
            # 将文件夹移动到做种的路径
            resource_path = get_settings("moveFilePath")
            if resource_path == "" or resource_path is None or resource_path == "None":
                self.parent.debugBrowser.append("未设置转移路径，自动跳过文件转移")
                logger.warning("未设置转移路径，自动跳过文件转移")
                return
            else:
                # 判断原文件夹与做种文件是否相同
                if resource_path == os.path.dirname(videoPath):
                    self.parent.debugBrowser.append("原文件夹与转移文件夹相同，无需转移")
                    logger.warning("原文件夹与转移文件夹相同，无需转移")
                    return
                # 转移文件需要异步执行，防止界面卡死
                self.parent.progress = 0
                self.parent.debugBrowser.append("开始移动文件到做种路径")
                logger.info("开始移动文件到做种路径")
                self.move_file_thread = MoveFileThread(videoPath, resource_path, self.parent.torrentPathBrowser
                                                       .toPlainText())
                logger.info("移动文件类初始化成功")
                self.move_file_thread.result_signal.connect(self.handleMoveFileResult)  # 连接信号
                logger.info("连接信号成功")
                self.move_file_thread.start()
                self.parent.debugBrowser.append("移动文件线程启动成功")

    def handleMoveFileResult(self, get_success, progress, res):
        print("开始处理移动文件后的逻辑")
        if get_success:
            self.parent.progress = progress
            if progress != 100:
                self.parent.debugBrowser.append(f"文件移动中，当前进度：{progress}%")
            else:
                while self.parent.torrentPathBrowser.toPlainText() == "" and self.parent.seed_start == 1:
                    self.parent.debugBrowser.append("种子路径为空，等待种子制作完成")
                    time.sleep(3)

                shutil.rmtree(self.parent.videoPath.text())
                self.parent.videoPath.setText(res)
                self.parent.debugBrowser.append("文件移动成功")
                logger.info("文件移动成功")
        else:
            self.parent.progress = 100
            self.parent.debugBrowser.append("文件移动失败：" + res)
            logger.error("文件移动失败：" + res)


class WriteFile:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def writeButtonClicked(self):
        # 判断主标题，副标题，发种排版信息，种子路径是否正常生成
        if not self.parent.mainTitleBrowser.toPlainText() or not self.parent.secondTitleBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先点击重命名文件文件夹按钮，生成标准名称",
                                QMessageBox.StandardButton.Ok)
            return
        if not self.parent.torrentPathBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先制作种子", QMessageBox.StandardButton.Ok)
            return
        if not self.parent.introBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请按照流程，生成发种排版信息", QMessageBox.StandardButton.Ok)
            return
        # 中文标题
        chinese_name = self.parent.chineseNameEdit.text() + ".txt"
        # 主标题
        mainTitle = self.parent.mainTitleBrowser.toPlainText().replace(' ', '.')
        # 副标题
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        # 种子路径
        torrentPath = self.parent.torrentPathBrowser.toPlainText()
        # 简介
        introBrowser = self.parent.introBrowser.toPlainText()
        # mediaInfo
        mediainfo = self.parent.mediainfoBrowser.toPlainText()

        # 获取保存目录
        video_info = get_settings("videoInfo")
        # 拼接文件路径
        file_path = os.path.join(video_info, chinese_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f'主标题为： {mainTitle}\n')
                file.write(f'副标题为： {secondTitle}\n')
                file.write(f'种子路径为： {torrentPath}\n')
                file.write(f'发种排版信息为： \n{introBrowser}\n')
                file.write(f'MediaInfo为： \n{mediainfo}\n')
            self.parent.debugBrowser.append("写入文件成功")
        except Exception as e:
            self.parent.debugBrowser.append(f"发生异常: {e}")
            logger.error(f"发生异常: {e}")


class GetPtGen(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.pt_gen_thread = None

    def getPtGenClicked(self):
        if not self.parent.ptGen.text():
            QMessageBox.warning(self.parent, "警告", "请先填写PTGen", QMessageBox.StandardButton.Ok)
            return
        pt_gen = self.parent.ptGen.text()
        pt_gen_path = get_settings("ptGenPath")
        self.parent.debugBrowser.append("开始获取PTGen")
        self.pt_gen_thread = GetPtGenThread(pt_gen_path, pt_gen)
        self.pt_gen_thread.result_signal.connect(self.handlePtGenResult)  # 连接信号
        self.pt_gen_thread.start()
        self.parent.debugBrowser.append("获取PTGen线程启动成功")
        logger.info("制作种子线程启动成功")

    def handlePtGenResult(self, get_success, response, info):
        print("开始处理生成后的逻辑")
        if get_success:
            if self.parent.feed.isChecked():
                response = prohibit + response
            self.parent.debugBrowser.append("成功获取到PTGen")
            self.parent.introBrowser.append(response)
            logger.info("成功获取到PTGen")
            if info:
                self.parent.coverPath.setText(info['poster'])
                self.parent.chineseNameEdit.setText(info['chinese_name'])
                self.parent.yearEdit.setText(info['year'])
                self.parent.english_name = info['trans_title']
                self.parent.debugBrowser.append(f"PTGen中提取的英文名为：{info['trans_title']}")
                self.parent.category = info['category']
                self.parent.debugBrowser.append(f"PTGen中提取的标签为：{info['category']}")
                self.parent.names = info['names']
        else:
            self.parent.debugBrowser.append("获取PTGen失败：" + response)
            logger.error(f"发生异常: {response}")


class GetMediaInfo:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def getMediaInfoButtonClicked(self):
        if not self.parent.videoPath.text():
            QMessageBox.warning(self.parent, "警告", "请先选择视频文件夹", QMessageBox.StandardButton.Ok)
            return
        self.parent.mediainfoBrowser.setText("")
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())  # 视频资源的路径
        if isVideoPath == 1 or isVideoPath == 2:
            get_media_info_success, mediainfo = get_media_info(videoPath)
            if get_media_info_success:
                self.parent.mediainfoBrowser.setText(mediainfo)
                mediainfo_text = medio_tem.format(mediainfo)
                self.parent.introBrowser.append(mediainfo_text)
                self.parent.debugBrowser.append("成功获取到MediaInfo")
                logger.info("成功获取到MediaInfo")
            else:
                self.parent.debugBrowser.append("获取MediaInfo失败,请重试")
                logger.error("获取MediaInfo失败,请重试")
        else:
            self.parent.debugBrowser.append("您的视频文件路径有误")
            logger.error("您的视频文件路径有误")


class MakeTorrent(QObject):
    result_signal = pyqtSignal(bool, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.make_torrent_thread = None

    def makeTorrentButtonClicked(self):
        if not self.parent.videoPath.text():
            QMessageBox.warning(self.parent, "警告", "请先选择视频文件夹", QMessageBox.StandardButton.Ok)
            return
        isVideoPath, videoPath = check_path_and_find_video(self.parent.videoPath.text())  # 视频资源的路径
        if isVideoPath == 1 or isVideoPath == 2:
            torrent_path = str(get_settings("torrentPath"))
            folder_path = os.path.dirname(videoPath)
            self.parent.seed_start = 1
            self.parent.debugBrowser.append("开始将" + folder_path + "制作种子，储存在" + torrent_path)
            logger.info("开始将" + folder_path + "制作种子，储存在" + torrent_path)
            self.make_torrent_thread = MakeTorrentThread(folder_path, torrent_path)
            self.make_torrent_thread.result_signal.connect(self.handleMakeTorrentResult)  # 连接信号
            self.make_torrent_thread.start()
            self.parent.debugBrowser.append("制作种子线程启动成功")
            logger.info("制作种子线程启动成功")
        else:
            self.parent.debugBrowser.append("制作种子失败：" + videoPath)
            logger.error("制作种子失败：" + videoPath)

    def handleMakeTorrentResult(self, get_success, response, error):
        print("开始处理制作后的逻辑")
        self.parent.seed_start = 0
        if error == "":
            if get_success:
                self.parent.debugBrowser.append("成功制作种子：" + response)
                logger.info("成功制作种子：" + response)
                # self.parent.torrent_path = response
                torrent_path = response
                current_working_directory = os.getcwd()

                if torrent_path:
                    if not os.path.isabs(torrent_path):
                        torrent_path = os.path.join(current_working_directory, torrent_path)
                        torrent_path = os.path.abspath(torrent_path)
                        torrent_path = Path(torrent_path)
                self.parent.torrentPathBrowser.setText(str(torrent_path))
            else:
                self.parent.debugBrowser.append("制作种子失败：" + response)
                logger.error("制作种子失败：" + response)
        else:
            logger.error(f"发生异常: {error}")


class UploadHandler:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.proxy_url = get_settings("proxyUrl")
        self.torrent_path = get_settings("torrentSavePath")

    def sendTjuClicked(self):
        if not self.parent.mainTitleBrowser.toPlainText() or not self.parent.secondTitleBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先点击重命名文件文件夹按钮，生成标准名称",
                                QMessageBox.StandardButton.Ok)
            return
        if not self.parent.torrentPathBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先制作种子", QMessageBox.StandardButton.Ok)
            return
        if not self.parent.introBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请按照流程，生成发种排版信息", QMessageBox.StandardButton.Ok)
            return
        self.parent.debugBrowser.append("开始上传种子到TJUPT")
        logger.info("开始上传种子到TJUPT")
        cookie_str = get_settings("tjuCookie")

        mainTitle = self.parent.mainTitleBrowser.toPlainText()
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        introBrowser = self.parent.introBrowser.toPlainText()
        chinese_name = self.parent.chineseNameEdit.text()
        torrent_path = self.parent.torrentPathBrowser.toPlainText()
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        upload_success, tju_link, tju_path = upload_tjupt(cookie_str, torrent_path, mainTitle, secondTitle,
                                                          introBrowser,
                                                          chinese_name, self.proxy_url, self.torrent_path,
                                                          self.parent.feed.isChecked())
        if upload_success:
            self.parent.tjuTorrentLink = tju_link
            self.parent.tjuTorrentPath = tju_path
            self.parent.debugBrowser.append("上传种子到TJUPT成功,种子链接为：" + tju_link)
            logger.info("上传种子到TJUPT成功,种子链接为：" + tju_link)
        else:
            self.parent.debugBrowser.append("上传种子到TJUPT失败，失败原因为：" + tju_link)
            logger.error("上传种子到TJUPT失败，失败原因为：" + tju_link)

    def sendAgsvClicked(self):
        if not self.parent.mainTitleBrowser.toPlainText() or not self.parent.secondTitleBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先点击重命名文件文件夹按钮，生成标准名称",
                                QMessageBox.StandardButton.Ok)
            return
        if not self.parent.mediainfoBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先获取MediaInfo", QMessageBox.StandardButton.Ok)
            return
        if not self.parent.torrentPathBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先制作种子", QMessageBox.StandardButton.Ok)
            return
        if not self.parent.introBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请按照流程，生成发种排版信息", QMessageBox.StandardButton.Ok)
            return
        self.parent.debugBrowser.append("开始上传种子到agsv")
        logger.info("开始上传种子到agsv")
        cookie_str = get_settings("agsvCookie")
        mainTitle = self.parent.mainTitleBrowser.toPlainText()
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        introBrowser = self.parent.introBrowser.toPlainText()
        media_info = self.parent.mediainfoBrowser.toPlainText()
        torrent_path = self.parent.torrentPathBrowser.toPlainText()
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        upload_success, agsv_link, agsv_path = upload_agsv(cookie_str, torrent_path, mainTitle, secondTitle,
                                                           introBrowser,
                                                           media_info, self.proxy_url, self.torrent_path,
                                                           self.parent.feed.isChecked())
        if upload_success:
            self.parent.agsvTorrentLink = agsv_link
            self.parent.agsvTorrentPath = agsv_path
            self.parent.debugBrowser.append("上传种子到agsv成功,种子链接为：" + agsv_link)
        else:
            self.parent.debugBrowser.append("上传种子到agsv失败，失败原因为：" + agsv_link)

    def sendPeterClicked(self):
        if not self.parent.mainTitleBrowser.toPlainText() or not self.parent.secondTitleBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先点击重命名文件文件夹按钮，生成标准名称",
                                QMessageBox.StandardButton.Ok)
            return
        if not self.parent.torrentPathBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先制作种子", QMessageBox.StandardButton.Ok)
            return
        if not self.parent.introBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请按照流程，生成发种排版信息", QMessageBox.StandardButton.Ok)
            return
        self.parent.debugBrowser.append("开始上传种子到Pter")
        logger.info("开始上传种子到Pter")
        cookie_str = get_settings("pterCookie")
        mainTitle = self.parent.mainTitleBrowser.toPlainText()
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        introBrowser = self.parent.introBrowser.toPlainText()
        media_info = self.parent.mediainfoBrowser.toPlainText()
        torrent_path = self.parent.torrentPathBrowser.toPlainText()
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        upload_success, pter_link, pter_path = upload_pter(cookie_str, torrent_path, mainTitle, secondTitle,
                                                           introBrowser, media_info,
                                                           self.proxy_url, self.torrent_path,
                                                           self.parent.feed.isChecked(),
                                                           )
        if upload_success:
            self.parent.peterTorrentLink = pter_link
            self.parent.peterTorrentPath = pter_path
            self.parent.debugBrowser.append("上传种子到Pter成功,种子链接为：" + pter_link)
            logger.info("上传种子到Pter成功,种子链接为：" + pter_link)
        else:
            self.parent.debugBrowser.append("上传种子到Pter失败，失败原因为：" + pter_link)
            logger.error("上传种子到Pter失败，失败原因为：" + pter_link)

    def sendKylinClicked(self):
        if not self.parent.mainTitleBrowser.toPlainText() or not self.parent.secondTitleBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先点击重命名文件文件夹按钮，生成标准名称",
                                QMessageBox.StandardButton.Ok)
            return
        if not self.parent.torrentPathBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先制作种子", QMessageBox.StandardButton.Ok)
            return
        if not self.parent.introBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请按照流程，生成发种排版信息", QMessageBox.StandardButton.Ok)
            return
        self.parent.debugBrowser.append("开始上传种子到Kylin")
        logger.info("开始上传种子到Kylin")
        cookie_str = get_settings("kylinCookie")
        mainTitle = self.parent.mainTitleBrowser.toPlainText()
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        introBrowser = self.parent.introBrowser.toPlainText()
        media_info = self.parent.mediainfoBrowser.toPlainText()
        torrent_path = self.parent.torrentPathBrowser.toPlainText()
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        upload_success, kylin_link, kylin_path = upload_kylin(cookie_str, torrent_path, mainTitle, secondTitle,
                                                              introBrowser,media_info,
                                                              self.proxy_url, self.torrent_path,
                                                              self.parent.feed.isChecked()
                                                              )
        if upload_success:
            self.parent.kylinTorrentLink = kylin_link
            self.parent.kylinTorrentPath = kylin_path
            self.parent.debugBrowser.append("上传种子到kylin成功,种子链接为：" + kylin_link)
            logger.info("上传种子到kylin成功,种子链接为：" + kylin_link)
        else:
            self.parent.debugBrowser.append("上传种子到kylin失败，失败原因为：" + kylin_link)
            logger.error("上传种子到kylin失败，失败原因为：" + kylin_link)

    def sendredLeavesClicked(self):
        if not self.parent.mainTitleBrowser.toPlainText() or not self.parent.secondTitleBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先点击重命名文件文件夹按钮，生成标准名称",
                                QMessageBox.StandardButton.Ok)
            return
        if not self.parent.torrentPathBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请先制作种子", QMessageBox.StandardButton.Ok)
            return
        if not self.parent.introBrowser.toPlainText():
            QMessageBox.warning(self.parent, "警告", "请按照流程，生成发种排版信息", QMessageBox.StandardButton.Ok)
            return
        self.parent.debugBrowser.append("开始上传种子到redLeaves")
        logger.info("开始上传种子到redLeaves")
        cookie_str = get_settings("redLeavesCookie")
        mainTitle = self.parent.mainTitleBrowser.toPlainText()
        secondTitle = self.parent.secondTitleBrowser.toPlainText()
        introBrowser = self.parent.introBrowser.toPlainText()
        media_info = self.parent.mediainfoBrowser.toPlainText()
        torrent_path = self.parent.torrentPathBrowser.toPlainText()
        current_working_directory = os.getcwd()
        if torrent_path:
            if not os.path.isabs(torrent_path):
                torrent_path = os.path.join(current_working_directory, torrent_path)
                torrent_path = os.path.abspath(torrent_path)
        upload_success, redLeaves_link, redLeaves_torrent = upload_red_leaves(cookie_str, torrent_path, mainTitle,
                                                                              secondTitle,
                                                                              introBrowser,
                                                                              media_info, self.proxy_url,
                                                                              self.torrent_path,
                                                                              self.parent.feed.isChecked(),
                                                                              )
        if upload_success:
            self.parent.redLeavesTorrentLink = redLeaves_link
            self.parent.redLeavesTorrentPath = redLeaves_torrent
            self.parent.debugBrowser.append("上传种子到redLeaves成功,种子链接为：" + redLeaves_link)
            logger.info("上传种子到redLeaves成功,种子链接为：" + redLeaves_link)


class SeedMak:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.downloaderHost = get_settings("downloaderHost")
        self.downloaderUser = get_settings("downloaderUser")
        self.downloaderPass = get_settings("downloaderPass")
        self.path = get_settings("resourcePath")

    def seed_qb(self):
        torrent_urls = [self.parent.tjuTorrentLink, self.parent.agsvTorrentLink, self.parent.peterTorrentLink,
                        self.parent.kylinTorrentLink, self.parent.redLeavesTorrentLink]
        torrent_paths = [self.parent.tjuTorrentPath, self.parent.agsvTorrentPath, self.parent.peterTorrentPath,
                         self.parent.kylinTorrentPath, self.parent.redLeavesTorrentPath]
        add_success, result_text = qb_download(self.downloaderHost, self.downloaderUser, self.downloaderPass,
                                               torrent_urls, torrent_paths, self.path)
        if add_success:
            self.parent.debugBrowser.append(result_text)
        else:
            self.parent.debugBrowser.append(result_text)

    def seed_tr(self):
        torrent_urls = [self.parent.tjuTorrentLink, self.parent.agsvTorrentLink, self.parent.peterTorrentLink,
                        self.parent.kylinTorrentLink, self.parent.redLeavesTorrentLink]
        torrent_paths = [self.parent.tjuTorrentPath, self.parent.agsvTorrentPath, self.parent.peterTorrentPath,
                         self.parent.kylinTorrentPath, self.parent.redLeavesTorrentPath]
        add_success, result_text = tr_download(self.downloaderHost, self.downloaderUser, self.downloaderPass,
                                               torrent_urls, torrent_paths, self.path)
        if add_success:
            self.parent.debugBrowser.append(result_text)
        else:
            self.parent.debugBrowser.append(result_text)


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
            self.result_signal.emit(False, {}, self.screenshot_path, self.is_cover, str(e))


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


class GetPtGenThread(QThread):
    # 创建一个信号，用于在数据处理完毕后与主线程通信
    result_signal = pyqtSignal(bool, str, dict)

    def __init__(self, api_url, resource_url):
        super().__init__()
        self.api_url = api_url
        self.resource_url = resource_url

    def run(self):
        try:
            # 这里放置耗时的HTTP请求操作
            get_success, response, info = fetch_and_format_ptgen_data(self.api_url, self.resource_url)
            # 发送信号，包括请求的结果
            print("Pt-Gen请求成功，开始返回结果")
            self.result_signal.emit(get_success, response, info)
            print("返回结果成功")
        except Exception as e:
            print(f"异常发生: {e}")
            self.result_signal.emit(False, str(e), {})


class MoveFileThread(QThread):
    # 创建一个信号，用于在数据处理完毕后与主线程通信
    result_signal = pyqtSignal(bool, int, str)

    def __init__(self, folder_path, target_path, torrent_path):
        super().__init__()
        self.folder_path = folder_path
        self.target_path = target_path
        self.torrent_path = torrent_path

    def run(self):
        try:
            self.folder_path = Path(self.folder_path)
            self.target_path = Path(self.target_path)
            # 需在target_path目录下创建一个与folder_path最后一级目录同名的文件夹
            self.target_path = os.path.join(self.target_path, self.folder_path.name)
            # 创建目标文件夹
            os.makedirs(self.target_path, exist_ok=True)
            p = 0
            file_count = sum(len(files) for _, _, files in os.walk(self.folder_path))
            for root, dirs, files in os.walk(self.folder_path):
                for file in files:
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(self.target_path, file)
                    shutil.copy(str(src_path), str(dst_path))
                    p += 1
                    schedule = int(p / file_count * 100)
                    if schedule % 10 == 0:
                        self.result_signal.emit(True, schedule, str(self.target_path))
                        logger.info(f'当前移动的进度为：{schedule}%')
        except FileNotFoundError as e:
            logger.error(f"文件夹不存在：{e}")
            self.result_signal.emit(False, 0, f"文件夹不存在：{e}")
        except shutil.Error as e:
            logger.error(f"文件拷贝失败：{e}")
            self.result_signal.emit(False, 0, f"文件拷贝失败：{e}")
        except OSError as e:
            logger.error(f"创建目标文件夹失败：{e}")
            self.result_signal.emit(False, 0, f"创建目标文件夹失败：{e}")
        except Exception as e:
            logger.error(f"发生异常: {e}")
            self.result_signal.emit(False, 0, f"发生异常: {e}")
