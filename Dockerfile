FROM python:3.7-alpine

# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

RUN apk update  \ 
    && apk add gcc musl-dev jpeg-dev zlib-dev postgresql-dev

# COPYコマンドは、左が自分のパソコンのフォルダー、右側がコンテナのディレクトリー
# linuxはルートディレクトリーが/から始まるるので/から始まる
COPY ./requirements.txt /requirements.txt

# pipの一括インストールオプション: -r
RUN pip install -r /requirements.txt

RUN mkdir /app
# WORKDIRコマンドは、RUN、CMD などの命令で相対パスを指定したときのディレクトリを変えることができる
WORKDIR /app

# pipfileに関しては、ホスト側でappのディレクトリーに言って、pipenv installを行う
# この二つが実行できない
# RUN pip install pipenv 
# RUN pipenv install --system --skip-lock --dev

# ホストのapp以下のフォルダをコピーするだが、ymlでvolumeで同期しているので必要ない
# COPY ./app  /app


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

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# psycopg2-binaryをインストールするために

# postgresql-devで、postgresqlの実行環境を整えてくれる

# RUN apk update  \ 
#     && apk add postgresql-dev
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# pipenvに関して
# pipenv install
# と打つとカレントディレクトリにあるPipfile・Pipfile.lockを探して
# 自動でインストールしてくれる

# --system : 仮想環境ではなくデフォルトのPythonにインストール
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# pipenv続き
# 全部のパッケージを更新したい? それなら $ pipenv update とするだけです
# ipenv install を実行したときに requirements.txt ファイルしか無い場合は、
# Pipenvは自動でそのファイルの内容をインポートし Pipfile を作成します
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
