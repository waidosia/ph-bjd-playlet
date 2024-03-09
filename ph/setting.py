"""
处理设置页面的逻辑，包括设置页面的初始化、保存、取消
"""
from PyQt6.QtWidgets import QDialog, QMessageBox

from ph.seed import qb_download, tr_download
from ph.tool import get_folder_path, get_settings, update_settings
from ui.settings import Ui_Settings


class Settings(QDialog, Ui_Settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置界面
        # 绑定点击信号和槽函数
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.selectScreenshotPathButton.clicked.connect(self.selectScreenshotPathButtonClicked)
        self.selectTorrentPathButton.clicked.connect(self.selectTorrentPathButtonClicked)
        self.selectInfoPathButton.clicked.connect(self.selectInfoPathButtonClicked)
        self.selectmovePathButton.clicked.connect(self.selectmovePathButtonClicked)
        self.testDownloader.clicked.connect(self.testDownloaderClicked)

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

    def selectInfoPathButtonClicked(self):
        path = get_folder_path()
        if path != '':
            self.videoInfo.setText(path)

    def selectmovePathButtonClicked(self):
        path = get_folder_path()
        if path != '':
            self.moveFilePath.setText(path)

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
        self.ptGenPath.setText(get_settings("ptGenPath"))
        self.rows.setValue(int(get_settings("rows")))
        self.cols.setValue(int(get_settings("cols")))
        self.autoUploadScreenshot.setChecked(bool(get_settings("autoUploadScreenshot")))
        self.pasteScreenshotUrl.setChecked(bool(get_settings("pasteScreenshotUrl")))
        self.deleteScreenshot.setChecked(bool(get_settings("deleteScreenshot")))
        self.makeDir.setChecked(bool(get_settings("makeDir")))
        self.moveFile.setChecked(bool(get_settings("moveFile")))
        self.moveFilePath.setText(get_settings("moveFilePath"))
        button_group_value = get_settings("buttonGroup")
        selected_id = int(button_group_value) if button_group_value != "None" else -2
        self.buttonGroup.button(selected_id).setChecked(True)
        self.renameFile.setChecked(bool(get_settings("renameFile")))
        self.torrentSavePath.setText(get_settings("torrentSavePath"))
        self.proxyUrl.setText(get_settings("proxyUrl"))
        self.tjuCookie.setText(get_settings("tjuCookie"))
        self.agsvCookie.setText(get_settings("agsvCookie"))
        self.pterCookie.setText(get_settings("pterCookie"))
        self.kylinCookie.setText(get_settings("kylinCookie"))
        self.redLeavesCookie.setText(get_settings("redLeavesCookie"))
        self.downloaderHost.setText(get_settings("downloaderHost"))
        self.downloaderUser.setText(get_settings("downloaderUser"))
        self.downloaderPass.setText(get_settings("downloaderPass"))
        self.resourcePath.setText(get_settings("resourcePath"))
        self.videoInfo.setText(get_settings("videoInfo"))

    def updateSettings(self):
        update_settings("screenshotPath", self.screenshotPath.text())
        update_settings("torrentPath", self.torrentPath.text())
        update_settings("figureBedPath", self.figureBedPath.text())
        update_settings("figureBedToken", self.figureBedToken.text())
        update_settings("screenshotNumber", str(self.screenshotNumber.text()))
        update_settings("screenshotThreshold", str(self.screenshotThreshold.text()))
        update_settings("screenshotStart", str(self.screenshotStart.text()))
        update_settings("screenshotEnd", str(self.screenshotEnd.text()))
        update_settings("ptGenPath", str(self.ptGenPath.text()))
        update_settings("moveFilePath", str(self.moveFilePath.text()))
        update_settings("proxyUrl", str(self.proxyUrl.text()))
        update_settings("torrentSavePath", str(self.torrentSavePath.text()))
        update_settings("tjuCookie", str(self.tjuCookie.text()))
        update_settings("agsvCookie", str(self.agsvCookie.text()))
        update_settings("pterCookie", str(self.pterCookie.text()))
        update_settings("redLeavesCookie", str(self.redLeavesCookie.text()))
        update_settings("kylinCookie", str(self.kylinCookie.text()))
        update_settings("downloaderHost", str(self.downloaderHost.text()))
        update_settings("downloaderUser", str(self.downloaderUser.text()))
        update_settings("downloaderPass", str(self.downloaderPass.text()))
        update_settings("resourcePath", str(self.resourcePath.text()))
        update_settings("buttonGroup", int(self.buttonGroup.checkedId()))
        update_settings("videoInfo", str(self.videoInfo.text()))
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
        if self.moveFile.isChecked():
            update_settings("moveFile", "True")
        else:
            update_settings("moveFile", "")
        if self.renameFile.isChecked():
            update_settings("renameFile", "True")
        else:
            update_settings("renameFile", "")

    def testDownloaderClicked(self):
        # 测试下载器
        button_group_value = self.buttonGroup.checkedId()
        if button_group_value == -2:
            # qb
            is_success, message = qb_download(self.downloaderHost.text(), self.downloaderUser.text(),
                                              self.downloaderPass.text(), [], [], "")
            if is_success:
                QMessageBox.information(self, "提示", "测试成功", QMessageBox.StandardButton.Ok)
            else:
                # 弹窗提示错误信息
                QMessageBox.warning(self, "警告", message, QMessageBox.StandardButton.Ok)

        elif button_group_value == -3:
            # tr
            is_success, message = tr_download(self.downloaderHost.text(), self.downloaderUser.text(),
                                              self.downloaderPass.text(), [], [], "")
            if is_success:
                QMessageBox.information(self, "提示", "测试成功", QMessageBox.StandardButton.Ok)
            else:
                # 弹窗提示错误信息
                QMessageBox.warning(self, "警告", message, QMessageBox.StandardButton.Ok)
        else:
            # 弹窗提示错误的类型
            QMessageBox.warning(self, "警告", "错误的下载器,请联系开发者", QMessageBox.StandardButton.Ok)
