from flask import Flask, render_template, request, redirect, url_for, session
from database.db import db
from database.application_model import Application
import os
from werkzeug.utils import secure_filename
import random
import json

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = "secret123"

db.init_app(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home
@app.route('/')
def home():
    return render_template('index.html')

# Step 1
@app.route('/apply', methods=['GET', 'POST'])
def apply_step1():
    if request.method == 'POST':
        session['step1'] = request.form.to_dict()
        return redirect(url_for('apply_step2'))
    return render_template('apply_step1.html', current_step=1)

# Step 2
@app.route('/apply/step2', methods=['GET', 'POST'])
def apply_step2():
    if request.method == 'POST':
        session['step2'] = request.form.to_dict()
        return redirect(url_for('apply_step3'))
    return render_template('apply_step2.html', current_step=2)

# Step 3
@app.route('/apply/step3', methods=['GET', 'POST'])
def apply_step3():
    if request.method == 'POST':
        session['step3'] = request.form.to_dict()
        return redirect(url_for('apply_step4'))
    return render_template('apply_step3.html', current_step=3)

# Step 4 (Upload)
@app.route('/apply/step4', methods=['GET', 'POST'])
def apply_step4():
    if request.method == 'POST':
        uploaded_files = {}
        fields = ['aadhaar_doc','pan_doc','college_id_doc','income_doc',
                  'marksheet_doc','passbook_doc','photo_doc','domicile_doc']

        for field in fields:
            file = request.files.get(field)
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files[field] = filename

        session['step4'] = uploaded_files
        return redirect(url_for('apply_step5'))

    return render_template('apply_step4.html', current_step=4)

# Step 5 (Review)
@app.route('/apply/step5')
def apply_step5():
    data = session
    return render_template('apply_step5.html', data=data, current_step=5)

# Final Submit (Database Saving)
@app.route('/apply/submit', methods=['POST'])
def submit():
    all_data = dict(session)

    app_no = "MU-" + str(random.randint(10000,99999))

    new_app = Application(
        application_no=app_no,
        full_name=all_data['step1']['full_name'],
        aadhaar_number=all_data['step1']['aadhaar_number'],
        pan_number=all_data['step1']['pan_number'],
        email=all_data['step1']['email'],
        mobile=all_data['step1']['mobile'],
        data_json=json.dumps(all_data)
    )

    db.session.add(new_app)
    db.session.commit()

    session.clear()

    return render_template('success.html', app_no=app_no)

# ✅ Check Status Route (ADDED)
@app.route('/status', methods=['GET', 'POST'])
def check_status():
    application = None
    searched = False

    if request.method == 'POST':
        app_no = request.form.get('app_no')
        application = Application.query.filter_by(application_no=app_no).first()
        searched = True

    return render_template('status.html', application=application, searched=searched)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)