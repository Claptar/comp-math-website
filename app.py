from flask import Flask, render_template

import sys

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main_page():
    return render_template('main_page.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
