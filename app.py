from flask import Flask, redirect, render_template, request
from data_handling import db, Init_values, upload_file
from computations.pendulum import solve_celluloid_problem

import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
FOLDER_ID = os.environ.get('FOLDER_ID')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/', methods=['POST', 'GET'])
def main_page():
    img_path = "/static/img/cat.webp"
    return render_template('index.html', img_path=img_path)


@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == "POST":
        m1, m2 = float(request.form['m1']), float(request.form['m2'])
        l1, l2 = float(request.form['l1']), float(request.form['l2'])
        a1, a2 = float(request.form['a1']), float(request.form['a2'])

        initials = {"m1": m1, "m2": m2, "l1": l1, "l2": l2, "alpha1": a1, "alpha2": a2}

        print(initials)

        pendulum_data = Init_values.check_launch(initials)

        if pendulum_data:  # if there is image on the google drive
            drive_id = pendulum_data[-1].drive_id
            img_path = f"https://drive.google.com/uc?export=view&id={drive_id}"
            return render_template('index.html', img_path=img_path)
        else:
            solve_celluloid_problem([m1, m2], [l1, l2], [a1, a2])

            file_name = f"pendulum{str(m1)}{str(m2)}{str(l1)}{str(l2)}{str(a1)}{str(a2)}"
            file_path = 'celluloid.gif' #  os.path.join(os.path.abspath('computations'), 'celluloid.gif')
            drive_id = upload_file(FOLDER_ID, file_name, file_path)
            print("DRIVE_ID:", drive_id)

            pendulum_data = Init_values(m1, m2, l1, l2, a1, a2, drive_id['id'])
            pendulum_data.save_to_db()
            img_path = f"https://drive.google.com/uc?export=view&id={drive_id['id']}"
            print("IMAGE_PATH:", img_path)

        return render_template('index.html', img_path=img_path)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
