from ReoMusic.core.bot import TGN
from ReoMusic.core.dir import dirr
from ReoMusic.core.git import git
from ReoMusic.core.userbot import Userbot
from ReoMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = TGN()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
