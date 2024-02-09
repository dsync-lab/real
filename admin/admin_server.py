from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError
from db import db_init, db
from werkzeug.utils import secure_filename
from models import Img
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_uploads.db'
app.config['UPLOAD_FOLDER'] = 'static/assets/uploads'
db_init(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/carousel")
def carousel_upload():
    return render_template("components-carousel.html")



@app.route('/upload', methods=['POST'])
def upload_pic():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded', 400


    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    try:
        pic_path = os.path.join(app.config['UPLOAD_FOLDER'], pic.filename)
        pic.save(pic_path)

        img = Img(section=request.form.get('section'), mimetype=mimetype, name=filename)
        db.session.add(img)
        db.session.commit()
        upload_status = True
        return render_template('components-carousel.html', upload_status=upload_status)
        # return redirect(url_for('carousel_upload'))
    except IntegrityError as e:
        db.session.rollback()
        return 'Error: Duplicate image data. Image not uploaded', 400
    
    except Exception as e:
        db.session.rollback()
        return f'Error: {str(e)}', 500



if __name__=="__main__":
    app.run(debug=True, host="192.168.74.157")


