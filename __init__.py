import json

from aqt.qt import (
    QSplitter,
    QUrl,
    Qt
)
from aqt import gui_hooks, mw
from aqt.webview import AnkiWebView

from .settings import openSettings
from . import consts

mw.addonManager.setWebExports(__name__, r"web/.*")

class tetrisWidget:
    webview = None
    ankiWebWidget = None
    splitter = None
    injected = False
    counter = 0
    threshold = 10
    
    def inject(self):
        if(self.injected == False):
            self.ankiWebWidget = mw.web
            
            self.splitter = QSplitter()
            self.splitter.setOrientation(Qt.Orientation.Horizontal)
            self.splitter.setHandleWidth(0)
            self.splitter.setStyleSheet("QSplitter::handle {  image: url('data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='); }")
            
            self.webview = AnkiWebView()
            self.webview.set_open_links_externally(False)
            
            centralWidget = mw.web
            
            # If no widgets are wrapping the main webview
            if(mw.web.parentWidget().objectName() != "centralwidget"):
                centralWidget = mw.web.parentWidget()
            
            mw.mainLayout.removeWidget(centralWidget)
            self.splitter.insertWidget(1, centralWidget)
            self.splitter.insertWidget(2, self.webview)
            mw.mainLayout.insertWidget(1, self.splitter)
            
            self.injected = True
            self.openSidebar()
            
            self.threshold = int(consts.CONFIG["cardsToPlay"])
            
    def navigate(self, path):
        url = f"""http://{consts.HOST}:{consts.MEDIA_SERVER.getPort()}/_addons/{consts.ADDON_NAME}/{path}"""
        self.webview.load(QUrl(url))
        
    def openSidebar(self):
        self.webview.setFixedWidth(consts.PANEL_WIDTH)
    def closeSidebar(self):
        self.webview.setFixedWidth(0)
        
    def saveData(self):
        js = f"""
            window.tetris.save()
        """
        self.webview.eval(js)
        
    def loadData(self):
        with open(consts.PATH_TO_DATAFILE) as f:
            data = f.read()
            js = f"""
            window.tetris.load({data})
            """
            self.webview.eval(js)
        

# Show Answer
def showAnswer(card) -> None:
    if(tetris.injected == False):
        tetris.inject()
        tetris.navigate(consts.PATH_TO_HTML)
    else:
        tetris.counter = tetris.counter + 1
        if(tetris.counter >= tetris.threshold):
            tetris.counter = 0
            tetris.openSidebar()

tetris = tetrisWidget()
gui_hooks.reviewer_did_show_answer.append(showAnswer)

# Close / Collapse
def collapseAddon():
    tetris.saveData()
    tetris.closeSidebar()

# Save before ending review
gui_hooks.reviewer_will_end.append(collapseAddon)
# Save before closing
gui_hooks.profile_will_close.append(collapseAddon)

# Handle move
def on_js_message(handled, msg, context):
    
    if msg.startswith("tetris::done"):
        tetris.closeSidebar()
        return True, None
    
    if msg.startswith("tetris::save"):
        data = json.loads(msg.replace("tetris::save::", ""))
        
        with open(consts.PATH_TO_DATAFILE, 'w') as f:
            json.dump(data, f)
        
    if msg.startswith("tetris::load"):
        tetris.loadData()
    return handled
    
gui_hooks.webview_did_receive_js_message.append(on_js_message)

mw.addonManager.setConfigAction(__name__, openSettings)