from flask import Flask, request, render_template, redirect, url_for

# db연결 패키지 import
import configparser
import os
import pymysql
# ---

# DB 연결 설정 정보 세팅 ( db_config.ini에 정의 )
config = configparser.ConfigParser()
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

# sql = f"""SELECT * FROM wms.plan_In2
#         """

sql = f"""SELECT * FROM wms.plan_In2 where qr_hash=%s
        """

cur.execute(sql, 'testqr')

# 데이터 접근
# result = cur.fetchall()
rows = cur.fetchall()
# result = cur.fetchone()

# for record in result:
#     print(record)

# 연결 종료
conn.close()

for row in rows:
    # print(row)
    print(row['quantity'], row['qr_hash'], row['date'])

# rows = [list(rows[x]) for x in range(len(rows))]
#------------------------------------------------

app = Flask(__name__)

@app.route('/')
def hello():
    # return 'Hello, World!'
    return rows

@app.route('/hello')
def hellohtml():
    return render_template("hello.html")

@app.route('/hellos/<name>')
def hellos(name):
    return "hellos {}".format(name)

@app.route('/input/<int:num>')
def input(num):
    name = ''
    if num == 1:
        name = '도라에몽'
    elif num == 2:
        name = '진구'
    elif num == 3:
        name = '퉁퉁이'
    return "hello {}".format(name)

app.route('/test')
def test1():
    return 'test1'

@app.route('/test/')
def test2():
    return 'test2'

@app.route('/naver')
def naver():
    return render_template("naver.html")

@app.route('/kakao')
def daum():
    return redirect("https://www.daum.net/")

@app.route('/urltest')
def url_test():
    return redirect(url_for('daum'))

@app.route('/dora')
def myimage():
    return render_template("myimage.html")

@app.route('/form')
def formhtml():
    # return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], name = row['name'], quantity = row['quantity'])
    return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], quantity = row['quantity'])
    
@app.route('/method', methods=['GET', 'POST'])
def method():
    # if request.method == 'GET':
    #     # args_dict = request.args.to_dict()
    #     # print(args_dict)
    #     num = request.args["num"]
    #     name = request.args.get("name")
    #     return "GET으로 전달된 데이터({}, {})".format(num, name)
    # else:
    #     num = request.form["num"]
    #     name = request.form["name"]
    #     return "POST로 전달된 데이터({}, {})".format(num, name)
    if request.method == 'GET':
        # args_dict = request.args.to_dict()
        # print(args_dict)
        date = request.args.get["date"]
        warehouse_id = request.args.get("warehouse_id")
        # name = request.args.get("name")
        # return "GET으로 전달된 데이터({}, {})".format(date, warehouse_id, quantity, name)
        return "GET으로 전달된 데이터({}, {}, {})".format(date, warehouse_id, quantity)
    else:
        date = request.form["date"]
        warehouse_id = request.form["warehouse_id"]
        quantity = request.form["quantity"]
        return "POST로 전달된 데이터({}, {}, {})".format(date, warehouse_id, quantity)

if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('daum'))
        app.run()