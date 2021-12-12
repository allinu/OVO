FROM python:alpine

# workdir
WORKDIR /app

COPY . .

RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -U pip \
    && pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r requirements.txt 

EXPOSE 3000

VOLUME [ "/app/ssl" ]

CMD [ "/usr/local/bin/python", "app.py" ]