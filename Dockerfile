FROM python:alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories 

RUN apk add --update tzdata dcron screen gcc linux-headers gcc g++ make libffi-dev openssl-dev libtool \
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 

# workdir
WORKDIR /app

COPY . .

RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -U pip \
    && pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r requirements.txt 

EXPOSE 3000

VOLUME [ "/app/ssl" ]

CMD [ "/usr/local/bin/python", "app.py" ]