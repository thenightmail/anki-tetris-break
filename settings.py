import os
from aqt.qt import (
    Qt,
    QVBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
    QFileDialog,
    QPushButton,
    QPixmap,
    QCheckBox
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
        self.lbHighContrast = QLabel("High contrast")
        self.layout.addWidget(self.lbHighContrast)
        self.chkHighContrast = QCheckBox()
        self.layout.addWidget(self.chkHighContrast)

        # Background image
        self.backgroundImage = consts.CONFIG["backgroundImage"]
        self.backgroundImagePath = (
            consts.ADDON_PATH + "/web/" + consts.CONFIG["backgroundImage"]
        )

        self.lbBgImg = QLabel("Background image")
        self.layout.addWidget(self.lbBgImg)

        self.previewBgImg = QLabel()
        self.previewBgImg.setFixedWidth(200)
        self.previewBgImg.setFixedHeight(200)
        self.previewBgImg.setPixmap(
            QPixmap(self.backgroundImagePath).scaled(
                self.previewBgImg.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.layout.addWidget(self.previewBgImg)

        self.btnBgImg = QPushButton("Select / Replace Image", self)
        self.btnBgImg.clicked.connect(self.selectBgImg)

        self.btnBgImgClear = QPushButton("Clear Image", self)
        self.btnBgImgClear.clicked.connect(self.clearBgImg)
        self.layout.addWidget(self.btnBgImg)
        self.layout.addWidget(self.btnBgImgClear)

        # Save and cancel buttons
        self.btnSave = QPushButton("Save Settings", self)
        self.btnSave.clicked.connect(self.save)
        self.layout.addWidget(self.btnSave)
        self.btnCancel = QPushButton("Cancel", self)
        self.btnCancel.clicked.connect(self.reject)
        self.layout.addWidget(self.btnCancel)

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
