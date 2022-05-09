from flask import Flask, redirect, render_template, request

import sys

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main_page():
    return render_template('main_page.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == "POST":
        v_1, v_2, v_3, v_4 = request.form['v_1'], request.form['v_2'], request.form['v_3'], request.form['v_4']
        x_1, x_2, x_3, x_4 = request.form['x_1'], request.form['x_2'], request.form['x_3'], request.form['x_4']

        return redirect('/')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
