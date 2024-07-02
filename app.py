import json
import os
import secrets

from flask import Flask, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename

from database import db
from forms import UserForm, UploadFileForm
from models import User

app = Flask(__name__)

# Database Name
db_name = 'User.db'

# Configuring SQLite Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

# Suppresses warning while tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialising SQLAlchemy with Flask App
db.init_app(app)

SECRET_KEY = secrets.token_hex(16)
# print(SECRET_KEY, "\n\n")
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'static'


@app.route('/', methods=['GET', 'POST'])
def home():
    users = User.query.all()
    print(users, "\n\n")
    return render_template('home.html', users=users)


@app.route('/add-user', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        try:
            hobbies = form.hobbies.data.split(',')
            user = User(name=form.name.data, age=form.age.data, city=form.city.data, hobbies=hobbies)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()

            flash(f'Error: {str(e)}', 'danger')
    return render_template('form.html', form=form)


@app.route('/upload-user', methods=['GET', 'POST'])
def bulk_upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and file.filename.endswith('.json'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:

                with open(filepath, 'r') as f:
                    data = json.load(f)

                users = [
                    User(
                        name=item['name'],
                        age=item['age'],
                        city=item['city'],
                        hobbies=item['hobbies']
                    ) for item in data
                ]
                # Bulk insert
                db.session.bulk_save_objects(users)
                db.session.commit()
                flash('Users added successfully!', 'success')
            except Exception as err:
                flash(f'Error: {str(err)}', 'danger')
            os.remove(filepath)
            return redirect(url_for('bulk_upload'))
        else:
            flash(f'Expected a json file', 'danger')
    return render_template('bulk_upload.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
