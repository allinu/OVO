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
app.config["SECRET_KEY"] = "secret!"

NOTICE_KEY = os.environ.get("NOTICE_KEY")


def write_to_file():
    cursor = conn.cursor()
    ans = cursor.execute("SELECT * FROM tasks")
    if NOTICE_KEY:
        tmp = {
            "notifier": ["0", NOTICE_KEY, "AUTO_SIGN"],
            "users": [],
        }
    else:
        tmp = {"users": []}
    for row in ans:
        tmp["users"].append(
            {
                "username": row[0],
                "password": row[1],
                "school": row[2],
                "addr": [row[3].split(",")[0], row[3].split(",")[1], row[4]],
                "alias": row[5],
            }
        )

    with open("./conf.toml", "w", encoding="utf-8") as f:
        f.write(toml.dumps(tmp))


@app.route("/tasks", methods=["POST"])
def post_form():
    cursor = conn.cursor()
    if request.method == "POST":
        try:
            data = request.data.decode("utf-8")
            data = json.loads(data)
            log.info(data)
            for value in data.values():
                if len(str(value)) == 0:
                    return jsonify({"status": "error", "msg": "请填写完整信息"})
            username = data["username"]
            password = data["password"]
            school = data["school"]
            gps = data["gps"]
            gps_loc_name = data["gps_loc_name"]
            alias = data["alias"]
            res_data = {
                "username": username,
                "password": password,
                "school": school,
                "gps": gps,
                "gps_loc_name": gps_loc_name,
                "alias": alias,
            }
            log.info(res_data)
            sql = (
                """INSERT INTO tasks (username, password, school, gps, gps_loc_name, alias) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"""
                % (username, password, school, gps, gps_loc_name, alias)
            )
            log.info(sql)
            cursor.execute(sql)
            conn.commit()
            write_to_file()
            return jsonify({"status": "success", "data": res_data})
        except Exception as e:
            log.error(e)
            return jsonify(
                {
                    "status": "error",
                    "info": "昵称重复，或者用户名存在",
                }
            )


@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor = conn.cursor()
    if request.method == "GET":
        try:
            data = []
            ans = cursor.execute(
                "select username, school, gps_loc_name, alias from tasks"
            )
            for row in ans:
                data.append(
                    {
                        "username": row[0][:3] + 4 * "_" + row[0][-4:],
                        "school": row[1],
                        "gps_loc_name": row[2],
                        "alias": row[3],
                    }
                )
            log.info(data)
            return jsonify({"status": "success", "data": data})
        except Exception as e:
            return jsonify({"status": "error", "info": "Something wrong."})


@app.route("/tasks/<alias>", methods=["DELETE"])
def delete_tasks(alias):
    cursor = conn.cursor()
    if request.method == "DELETE":
        try:
            sql = "DELETE FROM tasks WHERE alias = '%s'" % (alias)
            log.info(sql)
            cursor.execute(sql)
            conn.commit()
            write_to_file()
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "info": "Something wrong."})


@app.route("/tasks/<username>", methods=["PUT"])
def update_tasks(username):
    cursor = conn.cursor()
    if request.method == "PUT":
        try:
            data = request.form
            log.info(data)
            password = data["password"]
            school = data["school"]
            gps = data["gps"]
            gps_loc_name = data["gps_loc_name"]
            alias = data["alias"]
            res_data = {
                "username": username,
                "password": password,
                "school": school,
                "gps": gps,
                "gps_loc_name": gps_loc_name,
                "alias": alias,
            }
            log.info(res_data)
            sql = (
                """UPDATE tasks SET password = '%s', school = '%s', gps = '%s', gps_loc_name = '%s', alias = '%s' WHERE username = '%s'"""
                % (password, school, gps, gps_loc_name, alias, username)
            )
            log.info(sql)
            cursor.execute(sql)
            conn.commit()
            write_to_file()
            return jsonify({"status": "success", "data": res_data})
        except Exception as e:
            return jsonify({"status": "error", "info": "Incomplete data"})


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
