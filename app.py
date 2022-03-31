from flask import Flask, request
from flask.json import jsonify
from rich.logging import RichHandler
import logging
from logging.handlers import RotatingFileHandler
import sqlite3
import json
from utils import re_write

conn = sqlite3.connect("./db/data.db", check_same_thread=False)
hander = RotatingFileHandler("./logs/server.log",
                             encoding="UTF-8",
                             maxBytes=1024 * 1024 * 10,
                             backupCount=10)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler(), hander],
)

log = logging.getLogger("server")

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

@app.route("/rewrite", methods=["POST"])
def rewrite():
    log.info(request.data)
    data = request.data.decode("utf-8")
    data = json.loads(data)
    log.info(data)
    origin_text = data["origin_text"]
    rewrite_text = re_write(origin_text)
    return jsonify({
        "origin_text": origin_text,
        "rewrite_text": rewrite_text
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True,
    )
