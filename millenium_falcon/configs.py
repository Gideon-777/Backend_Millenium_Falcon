import os

from dotenv import load_dotenv

from millenium_falcon.utils import set_loglevel

load_dotenv(".env")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").strip()
set_loglevel(LOG_LEVEL)
PORT = os.environ.get("PORT").strip()
