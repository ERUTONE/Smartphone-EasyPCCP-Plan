# ベースイメージとしてPython公式イメージを使用します 
FROM python:3.9-slim 

# 必要なパッケージをインストールします 
RUN apt-get update && apt-get install -y gcc 

# Pythonの依存パッケージをコピーしてインストールします 
COPY requirements.txt /app/ RUN pip install --no-cache-dir -r requirements.txt 

# カレントディレクトリのコードをコンテナ内の/appにコピーします 
COPY . /app/ 

# Flaskアプリを起動するコマンドを指定します 
CMD [ "python", "app.py" ] 