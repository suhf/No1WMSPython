# -*- coding:utf-8 -*-

import configparser
import os
from flask import Flask
import pymysql

config = configparser.ConfigParser()

# DB 연결 설정 정보 세팅 ( db_config.ini에 정의 )
config.read(os.getcwd() + os.sep + 'db_config.ini', encoding='utf-8')

conn = pymysql.connect(
    host = config.get('DB_CONFIG', 'HOST'),
    port = int(config['DB_CONFIG']['PORT']),
    user= config['DB_CONFIG']['USER'],
    passwd= config.get('DB_CONFIG', 'PASSWD'),
    db= config['DB_CONFIG']['DBNAME'],
    charset="utf8")

# Tuple
cur = conn.cursor()

# DictCursor
cur = conn.cursor(pymysql.cursors.DictCursor)

sql = f"""SELECT * FROM authority
        """

# sql = f"""SELECT * FROM product
#         """
#cur.execute("set name utf8")

cur.execute(sql)

# 데이터 접근
result = cur.fetchall()

# 연결 종료
conn.close()

print(result)

app = Flask(__name__)

@app.route('/')
def hello():
    return result

if __name__ == '__main__':
    app.run()
