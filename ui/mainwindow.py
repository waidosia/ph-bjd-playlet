# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        Mainwindow.setObjectName("Mainwindow")
        Mainwindow.resize(943, 998)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        Mainwindow.setFont(font)
        Mainwindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(parent=Mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(21)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.chineseNameEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.chineseNameEdit.setObjectName("chineseNameEdit")
        self.horizontalLayout_2.addWidget(self.chineseNameEdit)
        self.label_9 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.yearEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.yearEdit.setObjectName("yearEdit")
        self.horizontalLayout_2.addWidget(self.yearEdit)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.debugBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.debugBrowser.setObjectName("debugBrowser")
        self.gridLayout_2.addWidget(self.debugBrowser, 2, 1, 5, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.seasonBox = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.seasonBox.setMinimum(1)
        self.seasonBox.setObjectName("seasonBox")
        self.horizontalLayout_10.addWidget(self.seasonBox)
        self.label_18 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_10.addWidget(self.label_18)
        self.type = QtWidgets.QComboBox(parent=self.centralwidget)
        self.type.setEditable(True)
        self.type.setObjectName("type")
        self.horizontalLayout_10.addWidget(self.type)
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_10.addWidget(self.label_3)
        self.source = QtWidgets.QComboBox(parent=self.centralwidget)
        self.source.setEditable(True)
        self.source.setObjectName("source")
        self.horizontalLayout_10.addWidget(self.source)
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_10.addWidget(self.label_6)
        self.team = QtWidgets.QComboBox(parent=self.centralwidget)
        self.team.setEditable(True)
        self.team.setObjectName("team")
        self.horizontalLayout_10.addWidget(self.team)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.videoPath = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.videoPath.setText("")
        self.videoPath.setDragEnabled(True)
        self.videoPath.setClearButtonEnabled(True)
        self.videoPath.setObjectName("videoPath")
        self.horizontalLayout.addWidget(self.videoPath)
        self.selectVideoFolderButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selectVideoFolderButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 3px 6px;\n"
"    font-size: 14px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.selectVideoFolderButton.setObjectName("selectVideoFolderButton")
        self.horizontalLayout.addWidget(self.selectVideoFolderButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_17 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_5.addWidget(self.label_17)
        self.coverPath = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.coverPath.setText("")
        self.coverPath.setDragEnabled(True)
        self.coverPath.setClearButtonEnabled(True)
        self.coverPath.setObjectName("coverPath")
        self.horizontalLayout_5.addWidget(self.coverPath)
        self.selectCoverFolderButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selectCoverFolderButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 3px 6px;\n"
"    font-size: 14px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.selectCoverFolderButton.setObjectName("selectCoverFolderButton")
        self.horizontalLayout_5.addWidget(self.selectCoverFolderButton)
        self.uploadCoverButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.uploadCoverButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 3px 6px;\n"
"    font-size: 14px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.uploadCoverButton.setObjectName("uploadCoverButton")
        self.horizontalLayout_5.addWidget(self.uploadCoverButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_19 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_4.addWidget(self.label_19)
        self.info = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.info.setObjectName("info")
        self.horizontalLayout_4.addWidget(self.info)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 6, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox_0 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_0.setObjectName("checkBox_0")
        self.horizontalLayout_6.addWidget(self.checkBox_0)
        self.checkBox_1 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_1.setObjectName("checkBox_1")
        self.horizontalLayout_6.addWidget(self.checkBox_1)
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_6.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_6.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_6.addWidget(self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout_6.addWidget(self.checkBox_5)
        self.checkBox_6 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.horizontalLayout_6.addWidget(self.checkBox_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 7, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.checkBox_7 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_7.setObjectName("checkBox_7")
        self.horizontalLayout_11.addWidget(self.checkBox_7)
        self.checkBox_8 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_8.setObjectName("checkBox_8")
        self.horizontalLayout_11.addWidget(self.checkBox_8)
        self.checkBox_9 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_9.setObjectName("checkBox_9")
        self.horizontalLayout_11.addWidget(self.checkBox_9)
        self.checkBox_10 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_10.setObjectName("checkBox_10")
        self.horizontalLayout_11.addWidget(self.checkBox_10)
        self.checkBox_11 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_11.setObjectName("checkBox_11")
        self.horizontalLayout_11.addWidget(self.checkBox_11)
        self.checkBox_12 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_12.setObjectName("checkBox_12")
        self.horizontalLayout_11.addWidget(self.checkBox_12)
        self.checkBox_13 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_13.setObjectName("checkBox_13")
        self.horizontalLayout_11.addWidget(self.checkBox_13)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 8, 0, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_11 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_6.addWidget(self.label_11)
        self.introBrowser = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.introBrowser.setObjectName("introBrowser")
        self.verticalLayout_6.addWidget(self.introBrowser)
        self.gridLayout_2.addLayout(self.verticalLayout_6, 8, 1, 2, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_12 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_13 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_3.addWidget(self.label_13)
        self.mainTitleBrowser = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.mainTitleBrowser.setUndoRedoEnabled(True)
        self.mainTitleBrowser.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.WidgetWidth)
        self.mainTitleBrowser.setObjectName("mainTitleBrowser")
        self.horizontalLayout_3.addWidget(self.mainTitleBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_14 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_7.addWidget(self.label_14)
        self.secondTitleBrowser = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.secondTitleBrowser.setReadOnly(False)
        self.secondTitleBrowser.setObjectName("secondTitleBrowser")
        self.horizontalLayout_7.addWidget(self.secondTitleBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_15 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_8.addWidget(self.label_15)
        self.fileNameBrowser = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.fileNameBrowser.setObjectName("fileNameBrowser")
        self.horizontalLayout_8.addWidget(self.fileNameBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.getNameButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getNameButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 6px 6px;\n"
"    font-size: 14px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.getNameButton.setObjectName("getNameButton")
        self.verticalLayout_2.addWidget(self.getNameButton)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.makeTorrentButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.makeTorrentButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 3px 6px;\n"
"    font-size: 14px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.makeTorrentButton.setObjectName("makeTorrentButton")
        self.verticalLayout_5.addWidget(self.makeTorrentButton)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 9, 0, 2, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_10 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10)
        self.mediainfoBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.mediainfoBrowser.setTabStopDistance(80.0)
        self.mediainfoBrowser.setObjectName("mediainfoBrowser")
        self.verticalLayout_4.addWidget(self.mediainfoBrowser)
        self.getMediaInfoButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getMediaInfoButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 6px 6px;\n"
"    font-size: 14px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.getMediaInfoButton.setObjectName("getMediaInfoButton")
        self.verticalLayout_4.addWidget(self.getMediaInfoButton)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 10, 1, 2, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.getPictureButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getPictureButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 6px 6px;\n"
"    font-size: 14px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.getPictureButton.setObjectName("getPictureButton")
        self.gridLayout.addWidget(self.getPictureButton, 3, 0, 1, 1)
        self.pictureUrlBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.pictureUrlBrowser.setObjectName("pictureUrlBrowser")
        self.gridLayout.addWidget(self.pictureUrlBrowser, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 11, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.writeButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.writeButton.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.writeButton.setFont(font)
        self.writeButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 15px 25px;\n"
"    font-size: 24px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 20px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.writeButton.setObjectName("writeButton")
        self.horizontalLayout_9.addWidget(self.writeButton)
        self.sendTjuButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.sendTjuButton.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sendTjuButton.setFont(font)
        self.sendTjuButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 15px 25px;\n"
"    font-size: 24px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 20px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.sendTjuButton.setObjectName("sendTjuButton")
        self.horizontalLayout_9.addWidget(self.sendTjuButton)
        self.sendPeterButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.sendPeterButton.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sendPeterButton.setFont(font)
        self.sendPeterButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 15px 25px;\n"
"    font-size: 24px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 20px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.sendPeterButton.setObjectName("sendPeterButton")
        self.horizontalLayout_9.addWidget(self.sendPeterButton)
        self.sendAgsvButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.sendAgsvButton.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sendAgsvButton.setFont(font)
        self.sendAgsvButton.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 15px 25px;\n"
"    font-size: 24px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 20px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.sendAgsvButton.setObjectName("sendAgsvButton")
        self.horizontalLayout_9.addWidget(self.sendAgsvButton)
        self.seedMak = QtWidgets.QPushButton(parent=self.centralwidget)
        self.seedMak.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.seedMak.setFont(font)
        self.seedMak.setStyleSheet("QPushButton {\n"
"    display: inline-block;\n"
"    padding: 15px 25px;\n"
"    font-size: 24px;\n"
"    cursor: pointer;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    outline: none;\n"
"    color:#fff;\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #16bf9d,\n"
"                                      stop:1 #10a266);\n"
"    border: none;\n"
"    border-radius: 20px;\n"
"    box-shadow: 0 9px #999;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #11b998,\n"
"                                      stop:1 #08965e);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: \n"
"                qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #0e9278,\n"
"                                      stop:1 #0e925c);\n"
"}\n"
"")
        self.seedMak.setObjectName("seedMak")
        self.horizontalLayout_9.addWidget(self.seedMak)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 12, 0, 1, 2)
        Mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=Mainwindow)
        self.statusbar.setObjectName("statusbar")
        Mainwindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(parent=Mainwindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 943, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        Mainwindow.setMenuBar(self.menubar)
        self.actionsettings = QtGui.QAction(parent=Mainwindow)
        self.actionsettings.setObjectName("actionsettings")
        self.menu.addAction(self.actionsettings)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(Mainwindow)
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

    def retranslateUi(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("Mainwindow", "ph-bjd"))
        self.label_7.setText(_translate("Mainwindow", "Publish Helper for Playlet"))
        self.label_16.setText(_translate("Mainwindow", "输入"))
        self.label_4.setText(_translate("Mainwindow", "debug窗口"))
        self.label.setText(_translate("Mainwindow", "中文名称："))
        self.label_9.setText(_translate("Mainwindow", "发布年份："))
        self.label_8.setText(_translate("Mainwindow", "季数："))
        self.label_18.setText(_translate("Mainwindow", "类型："))
        self.label_3.setText(_translate("Mainwindow", "来源："))
        self.label_6.setText(_translate("Mainwindow", "小组："))
        self.label_2.setText(_translate("Mainwindow", "资源路径："))
        self.selectVideoFolderButton.setText(_translate("Mainwindow", "文件夹"))
        self.label_17.setText(_translate("Mainwindow", "封面路径："))
        self.selectCoverFolderButton.setText(_translate("Mainwindow", "浏览"))
        self.uploadCoverButton.setText(_translate("Mainwindow", "1、上传"))
        self.label_19.setText(_translate("Mainwindow", " 简介："))
        self.checkBox_0.setText(_translate("Mainwindow", "剧情"))
        self.checkBox_1.setText(_translate("Mainwindow", "爱情"))
        self.checkBox_2.setText(_translate("Mainwindow", "喜剧"))
        self.checkBox_3.setText(_translate("Mainwindow", "甜虐"))
        self.checkBox_4.setText(_translate("Mainwindow", "甜宠"))
        self.checkBox_5.setText(_translate("Mainwindow", "恐怖"))
        self.checkBox_6.setText(_translate("Mainwindow", "动作"))
        self.checkBox_7.setText(_translate("Mainwindow", "穿越"))
        self.checkBox_8.setText(_translate("Mainwindow", "重生"))
        self.checkBox_9.setText(_translate("Mainwindow", "逆袭"))
        self.checkBox_10.setText(_translate("Mainwindow", "科幻"))
        self.checkBox_11.setText(_translate("Mainwindow", "武侠"))
        self.checkBox_12.setText(_translate("Mainwindow", "都市"))
        self.checkBox_13.setText(_translate("Mainwindow", "古装"))
        self.label_11.setText(_translate("Mainwindow", "正文"))
        self.label_12.setText(_translate("Mainwindow", "命名"))
        self.label_13.setText(_translate("Mainwindow", "主标题："))
        self.label_14.setText(_translate("Mainwindow", "副标题："))
        self.label_15.setText(_translate("Mainwindow", "文件名："))
        self.getNameButton.setText(_translate("Mainwindow", "2、获取标准命名"))
        self.makeTorrentButton.setText(_translate("Mainwindow", "3、制作种子"))
        self.label_10.setText(_translate("Mainwindow", "MediaInfo"))
        self.mediainfoBrowser.setHtml(_translate("Mainwindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'微软雅黑\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.getMediaInfoButton.setText(_translate("Mainwindow", "4、获取"))
        self.getPictureButton.setText(_translate("Mainwindow", "5、一键生成简介"))
        self.label_5.setText(_translate("Mainwindow", "截图"))
        self.writeButton.setText(_translate("Mainwindow", "写入txt文件中"))
        self.sendTjuButton.setText(_translate("Mainwindow", "发北洋"))
        self.sendPeterButton.setText(_translate("Mainwindow", "发猫站"))
        self.sendAgsvButton.setText(_translate("Mainwindow", "发末日"))
        self.seedMak.setText(_translate("Mainwindow", "做种"))
        self.menu.setTitle(_translate("Mainwindow", "工具"))
        self.actionsettings.setText(_translate("Mainwindow", "设置"))
