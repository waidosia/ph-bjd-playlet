
"""
处理设置页面的逻辑，包括设置页面的初始化、保存、取消
"""
from PyQt6.QtWidgets import QDialog
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
        self.tjuCookie.setText(get_settings("tjuCookie"))
        self.agsvCookie.setText(get_settings("agsvCookie"))
        self.pterCookie.setText(get_settings("pterCookie"))
        self.kylinCookie.setText(get_settings("kylinCookie"))
        self.qbPath.setText(get_settings("qbPath"))
        self.qbUser.setText(get_settings("qbUser"))
        self.qbPasswd.setText(get_settings("qbPasswd"))
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
        update_settings("tjuCookie", str(self.tjuCookie.text()))
        update_settings("agsvCookie", str(self.agsvCookie.text()))
        update_settings("pterCookie", str(self.pterCookie.text()))
        update_settings("kylinCookie", str(self.kylinCookie.text()))
        update_settings("qbPath", str(self.qbPath.text()))
        update_settings("qbUser", str(self.qbUser.text()))
        update_settings("qbPasswd", str(self.qbPasswd.text()))
        update_settings("resourcePath", str(self.resourcePath.text()))
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
        if self.renameFile.isChecked():
            update_settings("renameFile", "True")
        else:
            update_settings("renameFile", "")
