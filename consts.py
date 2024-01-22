from aqt import mw
from aqt.theme import theme_manager
from pathlib import Path

global ADDON_NAME, ADDON_TITLE, ADDON_PATH, HOST, MEDIA_SERVER, DARK_MODE, PANEL_WIDTH, PATH_TO_HTML, PATH_TO_DATAFILE, CONFIG

ADDON_NAME = "1844476877"
ADDON_TITLE = mw.addonManager.addon_meta(ADDON_NAME).provided_name
ADDON_PATH = Path(__file__).parent.absolute().as_posix()

HOST = "localhost"
MEDIA_SERVER = mw.mediaServer

DARK_MODE = theme_manager.night_mode
PANEL_WIDTH = 600

PATH_TO_HTML = f"""web/index.html?dark={DARK_MODE}"""
PATH_TO_DATAFILE = f"""{ADDON_PATH}/data.json"""

CONFIG = mw.addonManager.getConfig(ADDON_NAME)
if(len(CONFIG) == 0):
    CONFIG = {
        "cardsToPlay": 1,
        "backgroundImage": ""
    }
    mw.addonManager.writeConfig(ADDON_NAME, CONFIG)