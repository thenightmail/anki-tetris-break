from aqt.qt import (
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
)
from aqt import mw

from . import consts


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(consts.ADDON_TITLE + " Settings")

        self.layout = QVBoxLayout()
        
        self.message = QLabel("Number of cards needed to play the game")
        self.layout.addWidget(self.message)
        
        self.txtCardsToPlay = QLineEdit()
        self.layout.addWidget(self.txtCardsToPlay)
        
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)
        
        self.setLayout(self.layout)

dlg = SettingsDialog()

def openSettings():
    dlg.txtCardsToPlay.setText(consts.CONFIG["cardsToPlay"])
    if dlg.exec():
        saveSettings({"cardsToPlay": dlg.txtCardsToPlay.text()})

def saveSettings(settings):
    mw.addonManager.writeConfig(consts.ADDON_NAME, settings)
    consts.CONFIG = mw.addonManager.getConfig(consts.ADDON_NAME)