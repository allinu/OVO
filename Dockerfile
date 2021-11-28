FROM python:alpine

# change timezone and install packages
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories 

RUN apk add --update tzdata dcron nodejs npm screen \
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && npm i -g cea 

# workdir
WORKDIR /app

COPY . .

RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -U pip \
    && pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple rich flask flask_socketio toml

ENV NOTICE_KEY ""

RUN chmod +x scripts/start.sh && ./scripts/start.sh && crond

EXPOSE 3000

CMD [ "/usr/local/bin/python", "app.py" ]