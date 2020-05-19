FROM python:3.7-alpine
# FROM python:3.7.5-slim

# requirements.txt
# # 環境変数
# ENV APP_PATH /opt/apps/django/

# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

RUN apk update  \ 
    && apk add gcc musl-dev jpeg-dev zlib-dev

# RUN apk update \
#     && apk add  gcc  musl-dev jpeg-dev zlib-dev 

# COPYコマンドは、左が自分のパソコンのフォルダー、右側がコンテナのディレクトリー
# linuxはルートディレクトリーが/から始まるるので/から始まる
COPY ./requirements.txt /requirements.txt

# pipの一括インストールオプション: -r
RUN pip install -r /requirements.txt

RUN mkdir /app

# WORKDIRコマンドは、RUN、CMD などの命令で相対パスを指定したときのディレクトリを変えることができる
WORKDIR /app
COPY ./app  /app


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# alpineという軽量なLinuxに様々なパッケージやアプリケーションをインストールするためには、
# apkというパッケージマネージャを使う

# apk updateを行わないと、addできないので、まず初めにやること
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# Pillowをインストールするために
# pillowをinstallするために必要なライブラリーものを読み込む

# RUN apk update  \ 
#     && apk add gcc musl-dev jpeg-dev zlib-dev

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
