from flask import Flask, request, render_template, redirect, url_for

# db연결 패키지 import
import configparser
import os
import pymysql
# ---
import datetime
# import uuid

# 전역함수
global url
global group_number
global product_id
global warehouse_id
global manager_id

# DB 연결 설정 정보 세팅 ( db_config.ini에 정의 )
config = configparser.ConfigParser()
config.read(os.getcwd() + os.sep + 'db_config.ini', encoding='utf-8')

# db 연결
def dbcon():
    return pymysql.connect(
    host = config.get('DB_CONFIG', 'HOST'),
    port = int(config['DB_CONFIG']['PORT']),
    user= config['DB_CONFIG']['USER'],
    passwd= config.get('DB_CONFIG', 'PASSWD'),
    db= config['DB_CONFIG']['DBNAME'],
    charset="utf8")

def insert_data(quantity):
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (group_number, product_id, datetime.datetime.now(), quantity, warehouse_id, manager_id, 'a', True)
        # setdata = (uuid.uuid1(), uuid.uuid1(), uuid.uuid1(), datetime.datetime.now(), quantity, uuid.uuid1(), uuid.uuid1(), 'test', True)
        # c.execute("INSERT INTO wms.product_in2 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", setdata)
        c.execute("INSERT INTO wms.product_in(id, group_number, product_id, in_date, quantity, warehouse_id, manager_id, note, activation) VALUES(UUID(), %s, %s, %s, %s, %s, %s, %s, %s)", setdata)
        db.commit()
    except Exception as e:
        print('db error:', e)
        print(group_number)
    finally:
        db.close()

def update_data(url):
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (url)
        c.execute("UPDATE wms.plan_In SET clear = TRUE WHERE url=%s", setdata)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()

def select_all():
    ret = list()
    try:
        db = dbcon()
        c = db.cursor()
        #c.execute('SELECT * FROM wms.plan_In')
        c.execute('SELECT * FROM wms.plan_In WHERE clear=0')
        ret = c.fetchall()
        # for row in c.execute('SELECT * FROM student'):
        #     ret.append(row)
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
        return ret

# def select_num(url):
#     ret = ()
#     try:
#         db = dbcon()
#         #c = db.cursor()
#         c = db.cursor(pymysql.cursors.DictCursor)
#         setdata = (url)
#         # c.execute('SELECT * FROM wms.plan_In WHERE url=%s', setdata)
#         c.execute('SELECT * FROM wms.plan_In WHERE url=%s AND clear=0', setdata)
#         ret = c.fetchall()
#     except Exception as e:
#         print('db error:', e)
#     finally:
#         db.close()
#         return ret

def select_num(url):
    ret = ()
    try:
        db = dbcon()
        #c = db.cursor()
        c = db.cursor(pymysql.cursors.DictCursor)
        setdata = (url)
        # c.execute('SELECT * FROM wms.plan_In WHERE url=%s', setdata)
        c.execute('SELECT wms.plan_In.url url, wms.plan_In.group_number group_number, wms.plan_In.product_id product_id, wms.plan_In.warehouse_id warehouse_id, wms.plan_In.manager_id manager_id, wms.plan_In.quantity quantity, wms.product.name pd_name, wms.warehouse.name wh_name, wms.plan_In.`date` FROM wms.plan_In left join wms.product on wms.product.id = wms.plan_In.product_id left join wms.warehouse on wms.warehouse.id = wms.plan_In.warehouse_id WHERE url=%s AND clear=0', setdata)
        ret = c.fetchall()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
        return ret

# # # DB 연결
# # db = dbcon()

# # Tuple
# cur = conn.cursor()

# # DictCursor
# cur = conn.cursor(pymysql.cursors.DictCursor)

# # sql = f"""SELECT * FROM wms.plan_In2
# #         """

# sql = f"""SELECT * FROM wms.plan_In2 where qr_hash=%s
#         """

# cur.execute(sql, 'testqr')

# 데이터 접근
# result = cur.fetchall()
# rows = cur.fetchall()
# result = cur.fetchone()

# for record in result:
#     print(record)

# 연결 종료
#conn.close()

# ret = select_num('485b02c0-b05e-11ee-935d-0242ac110006')

# for row in ret:
#     # print(row)
#     print(row['wh_name'], row['pd_name'])
# rows = [list(rows[x]) for x in range(len(rows))]
#------------------------------------------------

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

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
    
#@app.route('/form')
@app.route('/form/<string:str>')
#def formhtml():
def formhtml(str):
    ret = select_num(str)
    for row in ret:
        print()

    global group_number
    global product_id
    global warehouse_id
    global manager_id
    global url
    group_number = row['group_number']
    product_id = row['product_id']
    warehouse_id = row['warehouse_id']
    manager_id = row['manager_id']
    url = row['url']
    # print(group_number, product_id, warehouse_id, manager_id)
    # if str == 'f90aef8a-aecd-11ee-935d-0242ac110006':
    #     return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], quantity = row['quantity'])
    # return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], name = row['name'], quantity = row['quantity'])
    return render_template("form.html", date = row['date'], wh_name = row['wh_name'], quantity = row['quantity'], pd_name = row['pd_name'])
    
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
        warehouse_id = request.args.get("wh_name")
        # name = request.args.get("name")
        # return "GET으로 전달된 데이터({}, {})".format(date, warehouse_id, quantity, name)
        return "GET으로 전달된 데이터({}, {}, {})".format(date, wh_name, quantity)
    else:
        date = request.form["date"]
        wh_name = request.form["wh_name"]
        quantity = request.form["quantity"]
        pd_name = request.form["pd_name"]
        insert_data(quantity)
        update_data(url)
        return "POST로 전달된 데이터({}, {}, {}, {})".format(date, wh_name, quantity, pd_name)
        # return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], quantity = row['quantity'])

if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('daum'))
        app.run()