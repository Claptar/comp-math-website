from flask import Flask, redirect, render_template, request
from data_handling import db, Launches, upload_file
from computations.pendulum import solve_celluloid_problem

import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
form_params = {
    "Masses": [
        {"placeholder": "mass of the ball", "name": "m1"},
        {"placeholder": "mass of the ball", "name": "m2"}
    ],
    "Lengths": [
        {"placeholder": "length of the thread", "name": "l1"},
        {"placeholder": "length of the thread", "name": "l2"}
    ]
}
folder_id = "1aV0F7HXookLXrnoyl3cXGmRCRFqhYAmu"

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
# db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def main_page():
    img_path = "/static/img/cat.webp"
    return render_template('main_page.html', form_params=form_params, img_path=img_path)


@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == "POST":
        m1, m2 = float(request.form['m1']), float(request.form['m2'])
        l1, l2 = float(request.form['l1']), float(request.form['l2'])
        initials = {"m1": m1, "m2": m2, "l1": l1, "l2": l2}

        pendulum_data = Launches.check_launch(initials)

        if pendulum_data:  # if there is image on the google drive
            drive_id = pendulum_data[-1].drive_id()
            img_path = f"https://drive.google.com/drive/folders/{folder_id}?{drive_id}"
            return render_template('main_page.html', form_params=form_params, img_path=img_path)
        else:
            solve_celluloid_problem([m1, m2], [l1, l2])

            file_name = f"pendulum{str(m1)}{str(m2)}{str(l1)}{str(l2)}"
            file_path = "/computations/celluloid.gif"
            drive_id = upload_file(folder_id, file_name, file_path)

            pendulum_data = Launches(m1, m2, l1, l2, drive_id)
            pendulum_data.save_to_db()
            img_path = f"https://drive.google.com/drive/folders/{folder_id}?{drive_id}"

        return render_template('main_page.html', form_params=form_params, img_path=img_path)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
