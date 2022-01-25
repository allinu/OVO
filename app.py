from flask import Flask, request
from flask.json import jsonify
from rich.logging import RichHandler
import logging
from logging.handlers import RotatingFileHandler
import sqlite3
import toml
import os
import json

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

NOTICE_KEY = os.environ.get("NOTICE_KEY")


def write_to_file():
    cursor = conn.cursor()
    ans = cursor.execute("SELECT * FROM sign_task")
    log.info(ans)
    if NOTICE_KEY:
        tmp = {
            "notifier": ["0", NOTICE_KEY, "AUTO_SIGN"],
            "users": [],
        }
    else:
        tmp = {"users": []}
        for row in ans:
            log.info(row)
            tmp_addr = []
            if row[4] == "" and row[5] == "":
                tmp_addr = [""]
            else:
                tmp_addr = [row[4], row[5], row[6]]
            tmp["users"].append({
                "alias": row[0],
                "school": row[1],
                "username": row[2],
                "password": row[3],
                "addr": tmp_addr,
                "signedDataMonth": row[7],
            })

    with open("./config/conf.toml", "w", encoding="utf-8") as f:
        f.write(toml.dumps(tmp))

@app.route("/tasks", methods=["POST"])
def post_form():
    cursor = conn.cursor()
    try:
        data = request.data.decode("utf-8")
        data = json.loads(data)

        log.info(data)

        if data["alias"] == "" or data['username'] == "" or data['password'] == "" or data['school_id'] == "":
            return jsonify({"code": 1, "info": "必要数据不完整", "status": "error"})
        else:
            sql = "INSERT INTO sign_task (alias,school_id,username,password,location_lon,location_lat,location_name,signedDataMonth) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                data["alias"], data["school_id"], data["username"], data["password"], data["location_lon"], data["location_lat"], data["location_name"], data["signedDataMonth"])
            cursor.execute(sql)
            log.info(sql)
            conn.commit()
            write_to_file()
            return jsonify({
                "status": "success",
                "info": "保存成功",
                "code": 0
            })
    except Exception as e:
        log.error(e)
        return jsonify({
            "status": "error",
            "info": "数据填写不完全，昵称重复，或者用户名存在",
            "code": 1
        })

@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor = conn.cursor()
    if request.method == "GET":
        try:
            data = []
            ans = cursor.execute(
                "select alias,school_id,location_name from sign_task")
            for row in ans:
                data.append({
                    "alias": row[0],
                    "school_id": row[1],
                    "location_name": row[2],
                })
            log.info(data)
            return jsonify({"status": "success", "data": data, "code": 0, "info": "获取成功"})
        except Exception as e:
            return jsonify({"status": "error", "info": "获取失败", "code": 1})

@app.route("/tasks/<username>",methods=["GET"])
def get_info(username):
    cursor = conn.cursor()
    if request.method == "GET":
        try:
            data = []
            ans = cursor.execute(
                "select alias,school_id,location_name from sign_task where username = '%s'"%username)
            for row in ans:
                data.append({
                    "alias": row[0],
                    "school_id": row[1],
                    "location_name": row[2],
                })
            log.info(data)
            if len(data) == 0:
                return jsonify({"status": "error", "info": "用户不存在", "code": 1})
            else:
                return jsonify({"status": "success", "data": data, "code": 0, "info": "用户存在"})
        except Exception as e:
            return jsonify({"status": "error", "info": "获取失败", "code": 1})

@app.route("/tasks/<username>", methods=["DELETE"])
def delete_tasks(username):
    cursor = conn.cursor()
    if request.method == "DELETE":
        try:
            sql = "DELETE FROM sign_task WHERE username = '%s'" % (username)
            log.info(sql)
            cursor.execute(sql)
            conn.commit()
            write_to_file()
            return jsonify({
                "code": 0,
                "info": "删除成功",
                "status": "success"
            })
        except Exception as e:
            return jsonify({"status": "error", "info": "Something wrong.", "code": 1})


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        log.info(request)
    else:
        log.info(request)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True,
    )
