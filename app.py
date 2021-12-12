from flask import Flask, request
from flask.json import jsonify
from rich.logging import RichHandler
import logging
from logging.handlers import RotatingFileHandler
import sqlite3

conn = sqlite3.connect("./db/data.db", check_same_thread=False)
hander = RotatingFileHandler(
    "./logs/server.log", encoding="UTF-8", maxBytes=1024 * 1024 * 10, backupCount=10
)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler(), hander],
)

log = logging.getLogger("ws_server")

app = Flask(__name__)
app.config["SECRET_KEY"] = "liona.fun"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=False,
        # TODO 根据个人情况修改
        ssl_context=(
            "./ssl/1_liona.fun_bundle.crt",
            "./ssl/2_liona.fun.key",
        ),
    )
