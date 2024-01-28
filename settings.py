import os
from aqt.qt import (
    Qt,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
    QFileDialog,
    QPushButton,
    QPixmap,
    QCheckBox,
    QWidget,
    QGroupBox,
    QDrag,
    QDropEvent,
    QMimeData
)
from aqt import mw

import shutil

from . import consts, main
from importlib import reload
import sys

class SettingsDialog(QDialog):
    hasBgImageToBeCopied = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle(consts.ADDON_TITLE + " Settings")

        self.layout = QVBoxLayout()
        
        with open(consts.ADDON_PATH + "/style-settings.qss", "r") as f:
            _style = f.read()
            self.setStyleSheet(_style)

        # Cards to play
        self.lbCardsToPlay = QLabel("Number of cards needed to play the game")
        self.layout.addWidget(self.lbCardsToPlay)
        self.txtCardsToPlay = QLineEdit()
        self.layout.addWidget(self.txtCardsToPlay)

        # Lines per play
        self.lbLinesPerPlay = QLabel("Number of lines to be cleared per play")
        self.layout.addWidget(self.lbLinesPerPlay)
        self.txtLinesPerPlay = QLineEdit()
        self.layout.addWidget(self.txtLinesPerPlay)

        # self.separator1 = QFrame()
        # self.separator1.setFrameShape(QFrame.HLine)
        # self.layout.addWidget(self.separator1)

        # High contrast
        # self.lbHighContrast = QLabel("High contrast")
        # self.layout.addWidget(self.lbHighContrast)
        self.chkHighContrast = QCheckBox()
        self.chkHighContrast.setText("High contrast")
        # self.layout.addWidget(self.chkHighContrast)
        
        # self.highContrastLayout = QHBoxLayout()
        # self.highContrastLayout.setContentsMargins(0, 0, 0, 0)
        # self.highContrastLayout.addWidget(self.lbHighContrast)
        # self.highContrastLayout.addWidget(self.chkHighContrast, stretch=1)
        # self.highContrast = QWidget()
        # self.highContrast.setLayout(self.highContrastLayout)
        self.layout.addWidget(self.chkHighContrast)
        

        # Background image
        self.backgroundImage = consts.CONFIG["backgroundImage"]
        self.backgroundImagePath = (
            consts.ADDON_PATH + "/web/" + consts.CONFIG["backgroundImage"]
        )
        
        self.lbBgImg = QLabel("Background image")
        # self.layout.addWidget(self.lbBgImg)

        self.previewBgImg = QLabel()
        self.previewBgImg.setFixedWidth(200)
        self.previewBgImg.setFixedHeight(200)
        self.previewBgImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previewBgImg.setPixmap(
            QPixmap(self.backgroundImagePath).scaled(
                self.previewBgImg.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.previewBgImg.setStyleSheet(
            "QLabel { border: 1px solid #555; }"
        )
        # self.layout.addWidget(self.previewBgImg)

        self.btnBgImg = QPushButton("Select / Replace Image", self)
        self.btnBgImg.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btnBgImg.clicked.connect(self.selectBgImg)

        self.btnBgImgClear = QPushButton("Clear Image", self)
        self.btnBgImgClear.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btnBgImgClear.clicked.connect(self.clearBgImg)
        
        self.imgBtnsLayout = QHBoxLayout()
        self.imgBtnsLayout.addWidget(self.btnBgImg)
        self.imgBtnsLayout.addWidget(self.btnBgImgClear)
        self.imgBtns = QWidget()
        self.imgBtns.setLayout(self.imgBtnsLayout)
        # self.layout.addWidget(self.imgBtns)
        

        self.imgBox = QGroupBox()
        self.imgBoxLayout = QVBoxLayout()
        self.imgBox.setLayout(self.imgBoxLayout)
        self.imgBoxLayout.addWidget(self.lbBgImg)
        self.imgBoxLayout.addWidget(self.previewBgImg)
        self.imgBoxLayout.addWidget(self.imgBtns)
        self.layout.addWidget(self.imgBox)

        # Save and cancel buttons
        self.btnSave = QPushButton("Save Settings", self)
        self.btnSave.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.btnSave.clicked.connect(self.save)
        # self.layout.addWidget(self.btnSave)
        self.btnCancel = QPushButton("Cancel", self)
        self.btnCancel.clicked.connect(self.reject)
        # self.layout.addWidget(self.btnCancel)
        
        self.bottomBtnsLayout = QHBoxLayout()
        self.bottomBtnsLayout.addWidget(self.btnSave)
        self.bottomBtnsLayout.addWidget(self.btnCancel)
        self.bottomBtns = QWidget()
        self.bottomBtns.setLayout(self.bottomBtnsLayout)
        self.layout.addWidget(self.bottomBtns)

        self.setLayout(self.layout)

    def save(self):
        settings = {
            "cardsToPlay": self.txtCardsToPlay.text(),
            "linesPerPlay": self.txtLinesPerPlay.text(),
            "backgroundImage": self.backgroundImage,
            "highContrast": self.chkHighContrast.isChecked(),
        }
        if self.hasBgImageToBeCopied == True:
            shutil.copyfile(
                self.bgImageToBeCopied["source"], self.bgImageToBeCopied["destination"]
            )
            bgImg = os.path.relpath(
                self.bgImageToBeCopied["destination"], consts.ADDON_PATH + "/web/"
            )
            self.backgroundImage = bgImg
            settings["backgroundImage"] = bgImg
        
        mw.addonManager.writeConfig(consts.ADDON_NAME, settings)
        consts.CONFIG = mw.addonManager.getConfig(consts.ADDON_NAME)
        
        # Reload the module with the new configuration
        main.unload()
        reload(sys.modules[consts.ADDON_NAME + ".main"])
        
        self.accept()

    def clearBgImg(self):
        self.hasBgImageToBeCopied = False
        self.backgroundImage = ""
        self.previewBgImg.setPixmap(QPixmap())

    def selectBgImg(self):
        bgImgFile, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*.*)"
        )

        if bgImgFile != "":
            ext = os.path.splitext(bgImgFile)[1]
            self.hasBgImageToBeCopied = True
            self.bgImageToBeCopied = {
                "source": bgImgFile,
                "destination": consts.ADDON_PATH + "/web/userdata/bg" + ext,
            }

            self.previewBgImg.setPixmap(
                QPixmap(bgImgFile).scaled(
                    self.previewBgImg.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    transformMode=Qt.TransformationMode.SmoothTransformation,
                )
            )

    def open(self):
        self.txtCardsToPlay.setText(str(consts.CONFIG["cardsToPlay"]))
        self.txtLinesPerPlay.setText(str(consts.CONFIG["linesPerPlay"]))
        if(consts.CONFIG["highContrast"] == True):
            self.chkHighContrast.setChecked(True)
        self.exec()
