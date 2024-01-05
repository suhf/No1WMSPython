from flask import Flask, request, render_template, redirect, url_for
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

@app.route('/form')
def formhtml():
    return render_template("form.html")

@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        # args_dict = request.args.to_dict()
        # print(args_dict)
        num = request.args["num"]
        name = request.args.get("name")
        return "GET으로 전달된 데이터({}, {})".format(num, name)
    else:
        num = request.form["num"]
        name = request.form["name"]
        return "POST로 전달된 데이터({}, {})".format(num, name)

if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('daum'))
        app.run()