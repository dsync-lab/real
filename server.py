from flask import Flask, render_template, request, flash
from models import Property, PropertyImage
from db import db_init, db
import secrets
import os
from werkzeug.utils import secure_filename
import mimetypes
from flask_migrate import Migrate
from wtforms import StringField, IntegerField, FloatField, FileField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from datetime import datetime


app = Flask(__name__, static_url_path='/static', static_folder='static')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test-4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(24)
app.config['UPLOAD_FOLDER'] = 'static/assets/uploads'
migrate = Migrate(app, db)
db_init(app)



properties = {
    1: {"id": 1, "name": "property-1", "price": "$340,000", "address": "Olive Road Two", "image": "property-1", "status": "Sale"},
    2: {"id": 2, "name": "property-3", "price": "$290,000", "address": "Pear Road Four", "image": "property-3", "status": "Sale"},
    3: {"id": 3, "name": "property-6", "price": "$420,000", "address": "Banana Road Eight", "image": "property-6", "status": "Sale"},
    4: {"id": 4, "name": "property-7", "price": "$270,000", "address": "Grape Road Nine", "image": "property-7", "status": "Sale"},
    5: {"id": 5, "name": "property-8", "price": "$460,000", "address": "Apple Road Eleven", "image": "property-8", "status": "Sale"},
    6: {"id": 6, "name": "property-8", "price": "$360,000", "address": "Apple Road Eleven", "image": "property-8", "status": "Sale"},
    
}

rent_properties = {
    1: {"id": 1, "name": "property-1", "price": "$6,000", "address": "Olive Road Two", "image": "property-1", "status": "Rent"},
    2: {"id": 2, "name": "property-3", "price": "$9,000", "address": "Pear Road Four", "image": "property-3", "status": "Rent"},
    3: {"id": 3, "name": "property-6", "price": "$8,500", "address": "Banana Road Eight", "image": "property-6", "status": "Rent"},
    4: {"id": 4, "name": "property-7", "price": "$4,600", "address": "Grape Road Nine", "image": "property-7", "status": "Rent"},
    5: {"id": 5, "name": "property-8", "price": "$5,000", "address": "Apple Road Eleven", "image": "property-8", "status": "Rent"},
    6: {"id": 6, "name": "property-8", "price": "$6,400", "address": "Apple Road Eleven", "image": "property-8", "status": "Rent"},
    
}

@app.route("/")
def home():
    return render_template("index.html", properties=rent_properties, buy_property=properties)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")




@app.route("/property") 
def property():
    return render_template("property-grid.html", properties=properties)
 
@app.route("/rent")
def rent():
    return render_template("rent-grid.html", properties=rent_properties)


@app.route("/rent-view/<int:rent_property_id>")
def view_rent_property(rent_property_id):
    property_data = rent_properties.get(rent_property_id)
    if property_data:
        return render_template("property-single.html", property_data=property_data, source="Rent", route="rent") 
    else:
        return "Property not found", 404

@app.route("/about", methods= ['GET', 'POST'])
def search_property():
    if request.method == 'POST':
        property_type = request.form.get('type')
        city = request.form.get('city')
        bedrooms = request.form.get('bedrooms')
        price = request.form.get('price')
        search_query = {
            'property_type': property_type,
            'city': city,
            'bedrooms': bedrooms,
            'price': price,
        }

        print(search_query)

    return render_template('index.html')




@app.route("/property-view/<int:property_id>")
def view_property(property_id):
    property_data = Property.query.get(property_id)
    images = PropertyImage.query.filter_by(property_id=property_id).all()
    for image in images:
        current_image_path = image.image_path
        formatted_path = current_image_path.split("static/", 1)[1]
        

    if property_data:
        return render_template("property-single.html", property_data=property_data, source="Buy", route="property", image=image, image_path=formatted_path) 
    else:
        return "Property not found", 404
        
@app.route("/agent")
def agent():
    return render_template("agents-grid.html")

@app.route("/view-agent")
def view_agent():
    return render_template("agent-single.html")

@app.route("/admin")
def admin():
    return "YOO fuck you ass hole"




@app.route("/property-upload", methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        address = request.form['address']
        property_status = request.form['status']
        area = request.form['area']
        bathroom = request.form['bathroom']
        garage = request.form['garage']
        property_type = request.form['property_type']

        upload_date = datetime.now()

        new_property = Property(
            name=name, 
            price=price, 
            address=address, 
            upload_date=upload_date,
            property_status=property_status,
            area=area,
            bathroom=bathroom,
            garage=garage,
            property_type=property_type,
            agent_id=1,
        )


        try: 
            db.session.add(new_property)
            db.session.commit()
           

            property_id = new_property.id
            # # handle image upload
            # image_data = request.files.get('image')
           
            files = request.files.getlist('files[]')
            #print(files)
             # Create a folder for each property to organize images
            property_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(property_id))
            for image_data in files:
                if image_data:
                    result = upload_image(property_id, image_data, property_folder)
                    print(result)
                
            flash('Property added successfully')
        except Exception as e:
            db.session.rollback()
            print(f"Error adding property: {str(e)}")
            flash('Error adding property. Please try again', 'error')
    return render_template('add_property.html') 

@app.route('/show_property/<int:property_id>')
def show_property(property_id):
    property_data = Property.query.get_or_404(property_id)
    images = PropertyImage.query.filter_by(property_id=property_id).all()
    for image in images:
        current_image_path = image.image_path
        formatted_path = current_image_path.split("static/", 1)[1]
        

    return render_template('view_property.html', property_data=property_data, image=image, image_path=formatted_path)


def get_mimetype(file_path):
    return mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

def upload_image(property_id, image_data, property_folder):
    try:
        if not image_data:
            return {"status": "error", "message": "No image data provided."}

        # Get the filename and check if it's allowed
        filename = secure_filename(image_data.filename)
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return {"status": "error", "message": "Invalid file type. Allowed types are png, jpg, jpeg, gif."}

       
        os.makedirs(property_folder, exist_ok=True)

        # Save the image file
        file_path = os.path.join(property_folder, filename)
        image_data.save(file_path)
        now = datetime.now()

        new_image = PropertyImage(
            name=filename,
            property_id=property_id,
            upload_date=now,
            image_path=file_path,
            mimetype=get_mimetype(file_path)
        )

        db.session.add(new_image)
        db.session.commit()
        print('=======File uploaded successfully=====')

    except Exception as e:
        app.logger.error(f"Error uploading image: {str(e)}")
        return {"status": "error", "message": "An unexpected error occurred during image upload."}



if __name__=="__main__":
    app.run(debug=True)
