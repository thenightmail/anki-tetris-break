import os
from aqt.qt import (
    Qt,
    QVBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
    QFileDialog,
    QPushButton,
<<<<<<< HEAD
    QPixmap
=======
    QPixmap,
>>>>>>> a5b38c4 (Commit)
)
from aqt import mw

import shutil

from . import consts

class SettingsDialog(QDialog):
    hasBgImageToBeCopied = False
<<<<<<< HEAD
=======

>>>>>>> a5b38c4 (Commit)
    def __init__(self):
        super().__init__()

        self.setWindowTitle(consts.ADDON_TITLE + " Settings")

        self.layout = QVBoxLayout()

        # Cards to play
        self.lbCardsToPlay = QLabel("Number of cards needed to play the game")
        self.layout.addWidget(self.lbCardsToPlay)
        self.txtCardsToPlay = QLineEdit()
        self.layout.addWidget(self.txtCardsToPlay)

<<<<<<< HEAD
=======
        # Lines per play
        self.lbLinesPerPlay = QLabel("Number of lines to be cleared per play")
        self.layout.addWidget(self.lbLinesPerPlay)
        self.txtLinesPerPlay = QLineEdit()
        self.layout.addWidget(self.txtLinesPerPlay)

>>>>>>> a5b38c4 (Commit)
        # self.separator1 = QFrame()
        # self.separator1.setFrameShape(QFrame.HLine)
        # self.layout.addWidget(self.separator1)

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
        saveSettings(
            {
                "cardsToPlay": self.txtCardsToPlay.text(),
<<<<<<< HEAD
=======
                "linesPerPlay": self.txtLinesPerPlay.text(),
>>>>>>> a5b38c4 (Commit)
                "backgroundImage": self.backgroundImage,
            }
        )
        self.accept()

    def clearBgImg(self):
        self.hasBgImageToBeCopied = False
        self.backgroundImage = ""
        self.previewBgImg.setPixmap(QPixmap())

    def selectBgImg(self):
        bgImgFile, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*.*)"
        )
<<<<<<< HEAD
        
=======
>>>>>>> a5b38c4 (Commit)

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

dlg = SettingsDialog()

def openSettings():
    dlg.txtCardsToPlay.setText(str(consts.CONFIG["cardsToPlay"]))
<<<<<<< HEAD
    dlg.exec()

=======
    dlg.txtLinesPerPlay.setText(str(consts.CONFIG["linesPerPlay"]))
    dlg.exec()


>>>>>>> a5b38c4 (Commit)
def saveSettings(settings):
    if dlg.hasBgImageToBeCopied == True:
        shutil.copyfile(
            dlg.bgImageToBeCopied["source"], dlg.bgImageToBeCopied["destination"]
        )
        bgImg = os.path.relpath(
            dlg.bgImageToBeCopied["destination"], consts.ADDON_PATH + "/web/"
        )
        dlg.backgroundImage = bgImg
        settings["backgroundImage"] = bgImg
    mw.addonManager.writeConfig(consts.ADDON_NAME, settings)
<<<<<<< HEAD
    consts.CONFIG = mw.addonManager.getConfig(consts.ADDON_NAME)
=======
    consts.CONFIG = mw.addonManager.getConfig(consts.ADDON_NAME)
>>>>>>> a5b38c4 (Commit)
