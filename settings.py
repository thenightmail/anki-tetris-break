import os
from aqt.qt import (
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
    QFileDialog,
    QPushButton,
    QPixmap,
    Qt,
    QFrame
)
from aqt import mw

import shutil

from . import consts

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(consts.ADDON_TITLE + " Settings")

        self.layout = QVBoxLayout()

        # Cards to play
        self.lbCardsToPlay = QLabel("Number of cards needed to play the game")
        self.layout.addWidget(self.lbCardsToPlay)
        self.txtCardsToPlay = QLineEdit()
        self.layout.addWidget(self.txtCardsToPlay)

        self.separator1 = QFrame()
        self.separator1.setFrameShape(QFrame.HLine)
        self.layout.addWidget(self.separator1)

        # Background image
        self.hasBgImageToBeCopied = False
        self.backgroundImage = consts.CONFIG["backgroundImage"]
        self.backgroundImagePath = consts.ADDON_PATH + "/web/" + consts.CONFIG["backgroundImage"]
        
        self.lbBgImg = QLabel("Background image")
        self.layout.addWidget(self.lbBgImg)

        self.previewBgImg = QLabel()
        self.previewBgImg.setFixedWidth(200)
        self.previewBgImg.setFixedHeight(200)
        self.previewBgImg.setPixmap(
            QPixmap(self.backgroundImagePath).scaled(
                self.previewBgImg.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.SmoothTransformation,
            )
        )
        self.layout.addWidget(self.previewBgImg)

        self.btnBgImg = QPushButton("Select / Replace Image", self)
        self.btnBgImg.clicked.connect(self.selectBgImg)
        
        self.btnBgImgClear = QPushButton("Clear Image", self)
        self.btnBgImgClear.clicked.connect(self.clearBgImg)
        self.layout.addWidget(self.btnBgImg)
        self.layout.addWidget(self.btnBgImgClear)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def clearBgImg(self):
        self.hasBgImageToBeCopied = False
        self.backgroundImage = ""
        self.previewBgImg.setPixmap(QPixmap())
        
    def selectBgImg(self):
        bgImgFile, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*.*)"
        )

        if bgImgFile:
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
                    transformMode=Qt.SmoothTransformation,
                )
            )


dlg = SettingsDialog()


def openSettings():
    dlg.txtCardsToPlay.setText(consts.CONFIG["cardsToPlay"])
    if dlg.exec():
        if dlg.hasBgImageToBeCopied == True:
            shutil.copyfile(
                dlg.bgImageToBeCopied["source"], dlg.bgImageToBeCopied["destination"]
            )
            dlg.backgroundImage = os.path.realpath(dlg.backgroundImage, consts.ADDON_PATH + '/web/')
        saveSettings(
            {
                "cardsToPlay": dlg.txtCardsToPlay.text(),
                "backgroundImage": dlg.backgroundImage,
            }
        )


def saveSettings(settings):
    mw.addonManager.writeConfig(consts.ADDON_NAME, settings)
    consts.CONFIG = mw.addonManager.getConfig(consts.ADDON_NAME)

