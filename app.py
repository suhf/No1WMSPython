from flask import Flask, request, render_template, redirect, url_for

# db연결 패키지 import
import configparser
import os
import pymysql
# ---
import datetime
# import uuid

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

def insert_data(group_number, product_id, quantity, warehouse_id, manager_id):
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
        c.execute("UPDATE wms.plan_In SET clear = TRUE, activation = false WHERE url=%s", setdata)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()

def update_stock(warehouse_id, product_id, quantity): 
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (warehouse_id, product_id,warehouse_id,product_id, warehouse_id, product_id, quantity, warehouse_id,product_id,quantity)
        c.execute("INSERT INTO wms.stock(id, warehouse_id, product_id, quantity, activation)VALUES(CASE WHEN( SELECT inner_stock.id from stock inner_stock where inner_stock.warehouse_id  = %s and inner_stock.product_id = %s) is null THEN UUID() ELSE (SELECT inner_stock2.id from stock inner_stock2 where inner_stock2.warehouse_id  = %s and inner_stock2.product_id = %s) END, %s, %s, %s, TRUE) ON DUPLICATE KEY UPDATE quantity = (SELECT quantity from stock s where s.warehouse_id = %s and s.product_id = %s) + %s", setdata)
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

def wh_select_all():
    ret = list()
    try:
        db = dbcon()
        # c = db.cursor()
        c = db.cursor(pymysql.cursors.DictCursor)
        #c.execute('SELECT * FROM wms.plan_In')
        c.execute('SELECT * FROM wms.warehouse WHERE activation=1')
        ret = c.fetchall()
        # for row in c.execute('SELECT * FROM student'):
        #     ret.append(row)
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
        return ret

def select_num(url):
    ret = list()
    try:
        db = dbcon()
        # c = db.cursor()
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

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
    
#@app.route('/form')
@app.route('/qr/<string:str>')
#def formhtml():
def formhtml(str):
    d = select_num(str)
    row = d[0]
    ret2 = wh_select_all()

    # print(group_number, product_id, warehouse_id, manager_id)
    # if str == 'f90aef8a-aecd-11ee-935d-0242ac110006':
    #     return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], quantity = row['quantity'])
    # return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], name = row['name'], quantity = row['quantity'])
    return render_template("form.html", date = row['date'], wh_name = row['wh_name'], 
                           quantity = row['quantity'], pd_name = row['pd_name'], group_number = row['group_number'], 
                           product_id = row['product_id'], warehouse_id = row['warehouse_id'], manager_id = row['manager_id'], 
                           url = row['url'], server_list = ret2)
    
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
    date = request.form["date"]
    wh_name = request.form["wh_name"]
    warehouse_id = wh_name
    quantity = request.form["quantity"]
    pd_name = request.form["pd_name"]
    group_number = request.form["group_number"]
    product_id = request.form["product_id"]
    manager_id = request.form["manager_id"]
    url = request.form["url"]
    
    insert_data(group_number, product_id, quantity, warehouse_id, manager_id)
    update_data(url)
    update_stock(warehouse_id, product_id, quantity)
    
    return "POST로 전달된 데이터({}, {}, {}, {})".format(date, wh_name, quantity, pd_name)
    # return render_template("form.html", date = row['date'], warehouse_id = row['warehouse_id'], quantity = row['quantity'])

if __name__ == '__main__':
    with app.test_request_context():
        app.run()