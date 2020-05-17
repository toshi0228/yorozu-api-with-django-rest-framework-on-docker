FROM python:3.7-alpine

# requirements.txt
# # 環境変数
# ENV APP_PATH /opt/apps/django/

# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

# COPYコマンドは、左が自分のパソコンのフォルダー、右側がコンテナのディレクトリー
# linuxはルートディレクトリーが/から始まるるので/から始まる
COPY ./requirements.txt /requirements.txt

# pipの一括インストールオプション: -r
RUN pip install -r /requirements.txt

RUN mkdir /app

# WORKDIRコマンドは、RUN、CMD などの命令で相対パスを指定したときのディレクトリを変えることができる
WORKDIR /app
COPY ./app  /app
