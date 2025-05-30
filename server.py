from flask import Flask, render_template, request, flash, redirect, url_for, session, make_response, send_file, jsonify
from models import Property, PropertyImage, Users, Visitor, Agent, AgentImage
from db import db_init, db, login_manager
import secrets
import os  
from werkzeug.utils import secure_filename
import mimetypes
from flask_migrate import Migrate
from wtforms import StringField, IntegerField, FloatField, FileField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from datetime import datetime
import shutil
import qrcode
import io
import json
from PIL import Image
from apps.authentication.forms import CreateAccountForm, LoginForm
from apps.authentication.util import verify_pass
from flask_login import (
    login_required,
    current_user,
    login_user,
    logout_user
)
from jinja2 import TemplateNotFound
import logging
import hashlib
from sqlalchemy import func
import uuid



app = Flask(__name__, static_url_path='/static', static_folder='static')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test-16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(24)
app.config['UPLOAD_FOLDER'] = 'static/assets/uploads'
migrate = Migrate(app, db)
db_init(app)



@app.route("/")
def home():
    visitor_id = request.cookies.get("visitor_id")
    if visitor_id is None:
        visitor_id = str(uuid.uuid4())
        response = make_response(f"New visitor, your id is {visitor_id}")
        response.set_cookie("visitor_id", visitor_id, max_age=60*60*24*365*2)
        time_visited = datetime.now()
        new_visitor = Visitor(visitor_id=visitor_id, time_visited=time_visited)
        db.session.add(new_visitor)
        db.session.commit()
        print(f"DEBUGGGGG {visitor_id}")
    else:
        exisiting_visitor = Visitor.query.filter_by(visitor_id=visitor_id).first()
        print(f"Existing Visitor {exisiting_visitor}")
        if exisiting_visitor:
            exisiting_visitor.visit_count += 1
            exisiting_visitor.time_visited = datetime.now()
            db.session.commit()
        else:
            time_visited = datetime.now()
            new_visitor = Visitor(visitor_id=visitor_id, time_visited=time_visited)
            db.session.add(new_visitor)
            db.session.commit()




    properties_for_sale = Property.query.filter_by(property_status='For Sale').limit(3).all()
    latest_properties = Property.query.order_by(Property.upload_date.desc()).limit(10).all()
    
    print(f"LATEST PROPERTIES{latest_properties}")

    image_list = []
    for property in properties_for_sale:
        print(f'home Property ID{property.id}')
        images = PropertyImage.query.filter_by(property_id=property.id).all()
        if images:
            image_list.append(images[1])

    # image_list = image_list[1:]
    view_images = [first_item.image_path.split("static/", 1)[1] for first_item in image_list]
    print(f"IMAGE TO VIEW {view_images}")
     
    latest_item = {

    }
    new_property_image = {}
    for property in latest_properties:
        print(f'home Property ID{property.id}')
        images = PropertyImage.query.filter_by(property_id=property.id).all()
        if images:
            new_property_image[property] = images[1].image_path.split("static/", 1)[1]

    # view_latest_images = [first_item.image_path.split("static/", 1)[1] for first_item in new_property_image]
    print(f"Latest Images {new_property_image}")


    return render_template("index.html", properties_for_sale=properties_for_sale, latest_properties=new_property_image, images=view_images)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")




@app.route("/buy") 
def buy_property():
    properties = Property.query.filter_by(property_status="For Sale").all()
    image_list = []
    page = request.args.get('page', 1, type=int)
    per_page = 9
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(properties) + per_page - 1) // per_page

 
    property_on_page = properties[start:end]

    for property in property_on_page:
        print(f'Buy Property ID {property.id}')
        try:
            images = PropertyImage.query.filter_by(property_id=property.id).all()
        except Exception as e:
            print('Error occurred while querying image ')
        
        if images:
            image_list.append(images[1])
    print(f"IMAGE LISTTTTTT {image_list}")
    image_query = {}
    for element in image_list:
        property_id = element.property_id
        property_image_path = element.image_path.split("static/", 1)[1]
        print(f"PROPERTY_ID: {property_id}, PROPERTY_PATH: {property_image_path} ")
        image_query[property_id] = property_image_path
    print(f"DICTIONARYY: {image_query}")
    
    
    return render_template("property-grid.html", properties=property_on_page, images=image_query, total_pages=total_pages, page=page)

 
@app.route("/rent")
def rent_property():
    properties = Property.query.filter_by(property_status="For Rent").all()
    image_list = []
    page = request.args.get('page', 1, type=int)
    per_page = 9 
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(properties) + per_page - 1) // per_page

 
    property_on_page = properties[start:end]
    for property in property_on_page:
        print(f'Property ID{property.id}')
        images = PropertyImage.query.filter_by(property_id=property.id).all()
        if images:
            image_list.append(images[1])

    image_query = {}
    for element in image_list:
        property_id = element.property_id
        property_image_path = element.image_path.split("static/", 1)[1]
        # print(f"PROPERTY_ID: {property_id}, PROPERTY_PATH: {property_image_path} ")
        image_query[property_id] = property_image_path


    return render_template("rent-grid.html", properties=property_on_page, images=image_query, total_pages=total_pages, page=page)

wallet_addresses = {
    "btc": "bc1q46ajyqmnf785sz5zgylsxewlekdhjxk9w44cep",
    "eth": "0x3c4114773C0f06D28dca5E15bDFD91ea51440523",
    "ton": "UQBWo8co96EElybOJwYLcaiCmHA1T2BQEqDv7q0wlZ5PCQSg",
    "usdt(bep20/erc20)": "0x3c4114773C0f06D28dca5E15bDFD91ea51440523",
    "usdt(trc20)": "TQ2FByBbhbvraWzD96VkqK5AqdD8viUNAc",
    "sol": "5t8AZR3mBYgtTSM54weRonDx7LezzroULYVFBUeN4gW2", 
}



@app.route('/payment/<int:property_id>')
def make_payment(property_id):
    payment_types = [
        "Security Fee",
        "Agency Fee",
        "Legal Documentation Fee",
        "Down Payment",
        "Inspection Fee",
        "Reservation Fee",
        "Installment Payment"
    ]
    property_data = Property.query.get(property_id)
    return render_template('payment_bank.html', wallets=wallet_addresses, property_data=property_data, property_id=property_id, payment_types=payment_types)

@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    data = request.get_json()
    print("Payment data received:", data)

    # Create a directory for saving files if it doesn't exist
    save_dir = os.path.join(os.getcwd(), 'payment_logs')
    os.makedirs(save_dir, exist_ok=True)

    # Generate a unique filename (e.g., based on invoice_id or timestamp)
    invoice_id = data.get('invoice_id', 'no_invoice')
    filename = f"{invoice_id}.json"
    filepath = os.path.join(save_dir, filename)

    # Save the data to a JSON file
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


    # TODO: Save to database or process
    return jsonify({'status': 'success', 'message': 'Payment received'})



@app.route('/generate_qr')
def generate_qr():
    address = request.args.get("address")
    if not address:
        return "No address provided", 400

    # Generate QR code image in memory
    img = qrcode.make(address)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    data = request.get_json(force=True)

    # Ensure message directory exists
    messages_dir = os.path.join(os.getcwd(), 'user_messages')
    os.makedirs(messages_dir, exist_ok=True)

    # Generate unique filename based on timestamp
    timestamp = data.get("submitted_at", "").replace(":", "-").replace(".", "-")
    filename = f"message_{timestamp}.json"
    filepath = os.path.join(messages_dir, filename)

    # Save message to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"status": "success", "message": "Message saved successfully"})


@app.route("/property-view/<int:property_id>")
def view_property(property_id):
    property_data = Property.query.get_or_404(property_id)
    print(f'Queried property {property_data}')
    

    images = PropertyImage.query.filter_by(property_id=property_id).all()
    agent_data = Agent.query.get_or_404(property_id)
    print(f'agent data: {agent_data}')

    
    # images = images[1:]
    if images:
        

        

        # try:
        #     images = PropertyImage.query.filter_by(property_id=property.id).all()
        # except Exception as e:
        #     print('Error occurred while querying image ')
        print(f'Queried images {images}')
        formatted_image_path = []
        

        print(f'&&&&&& {property_data}')
        for image in images:
            current_image_path = image.image_path
            formatted_path = current_image_path.split("static/", 1)[1]
            formatted_image_path.append(formatted_path)
            
            

        if property_data:
            agent_image = formatted_image_path[0]
            the_image_path= formatted_image_path[1:]
            print(f'this is IMAGES {agent_image}')

            _price = property_data.price.replace(',', '')

            daily_price = int(_price)
            print(f'FUCKKKKKKKK£R£******* {daily_price}')
            weekly_price = daily_price * 7
            monthly_price = daily_price * 30
            yearly_price = daily_price * 365
            full_price = {
                'daily': daily_price,
                'weekly': weekly_price,
                'monthly': monthly_price,
                'yearly': yearly_price
            }

            return render_template("property-single.html", property_data=property_data, full_price = full_price, agent_data=agent_data,source="Buy", route="buy_property", image=image, agent_image=agent_image,image_path=the_image_path) 
        else:
            return "Property not found", 404
    else:
        print("Error occurred while quering image")
        return render_template("property-single.html", property_data=property_data, source="Buy", route="buy_property", agent_image=None,image=None, image_path=None) 


@app.route("/rent-view/<int:rent_property_id>")
def view_rent_property(rent_property_id):
    property_data = Property.query.get_or_404(property_id)
    try:
        images = PropertyImage.query.filter_by(property_id=property_id).all()
        formatted_image_path = []
        
        if images:
            print(f'view {images}')
            for image in images:
                current_image_path = image.image_path
                formatted_path = current_image_path.split("static/", 1)[1]
                formatted_image_path.append(formatted_path)
                

            if property_data:
                daily_price = property_data.get('price', '0')  # Get the string price
                property_data['daily_price'] = daily_price
                print(f'FUCKING CUNT {property_data['daily_price']}')
                property_data['weekly_price'] = daily_price * 7
                property_data['monthly_price'] = daily_price * 30
                property_data['yearly_price'] = daily_price * 365
                return render_template("property-single.html", property_data=property_data, source="Rent", route="rent_property", image=image, image_path=formatted_image_path) 
            else:
                return "Property not found", 404
        else:
            return render_template("property-single.html")
    except UnboundLocalError as e:
        # print("Property not found", e)
        return f"Property not found {e}", 404

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



        
@app.route("/agent")
def agent():
    return render_template("agents-grid.html")

@app.route("/view-agent")
def view_agent():
    return render_template("agent-single.html")

@app.route("/admin")
def admin():
    return "YOO fuck you ass hole"



#====================ADMIN FUNCTIONALITIES====================#





# Login & Registration

@app.route("/admin-home")
@login_required
def admin_home():
    new_visitors = db.session.query(func.count(func.distinct(Visitor.visitor_id))).scalar()
    print(f"ALL VISITOR COUNT {new_visitors}")
    traffic = Visitor.query.all()
    total_traffic = [ num.visit_count for num in traffic]
    traffic = 0
    for i in total_traffic:
        traffic += i
    print(f"TOTAL TRAFFIC{total_traffic}")
    print(f"TOTAL USERS {new_visitors}")
    print(f"CURRENT USERRR{current_user}")
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        return "Unathorized Access"

    if current_user.is_authenticated:

        return render_template("home/index.html", segment="index", users_visited=new_visitors, traffic=traffic)
    elif not current_user.is_admin:
        logging.warning(f"Unauthorized access to admin panel by user: {current_user.username}")
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('admin_home'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('admin_home'))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)
        user = Users.query.all()
        if len(user) == 0:
            is_admin = True
        else:
            is_admin = False

        # else we can create the user
        user_data = dict(request.form)
        user_data['is_admin'] = is_admin
        user = Users(**user_data)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


@app.route("/profile")
@login_required
def admin_profile():
    if current_user.is_authenticated:
    
        return render_template("home/profile.html", segment="profile", current_user=current_user)
    else:
        return redirect(url_for("login"))



@app.route('/admin/messages')
@login_required
def view_messages():
    messages_dir = 'user_messages'
    messages = []

    if os.path.exists(messages_dir):
        for file_name in sorted(os.listdir(messages_dir), reverse=True):
            if file_name.endswith('.json'):
                with open(os.path.join(messages_dir, file_name), 'r') as f:
                    try:
                        msg = json.load(f)
                        msg['filename'] = file_name
                        messages.append(msg)
                    except Exception as e:
                        print(f"Failed to load {file_name}: {e}")

    return render_template('admin_messages.html', messages=messages)


@app.route('/payment_logs')
@login_required
def payment_logs():
    logs = []
    logs_dir = os.path.join(os.getcwd(), 'payment_logs')

    if os.path.exists(logs_dir):
        for filename in os.listdir(logs_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(logs_dir, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)

                        # Ensure proper types for template
                        try:
                            data['amount'] = float(data.get('amount', 0))
                        except (ValueError, TypeError):
                            data['amount'] = None

                        data['filename'] = filename
                        logs.append(data)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    return render_template('payment_logs.html', logs=logs)


@app.route("/property-upload", methods=['GET', 'POST'])
@login_required
def add_property():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        property_description = request.form['property_description']
        address = request.form['address']
        map_view = request.form['map_view']
        property_status = request.form['status']
        area = request.form['area']
        bathroom = request.form['bathroom']
        garage = request.form['garage']
        property_type = request.form['property_type']

        upload_date = datetime.now()
        

        property_exists = Property.query.filter_by(name=name).first()

        if property_exists:
            flash('Property Already Exists')
            return redirect(url_for('add_property'))
        else:

            new_property = Property(
                name=name, 
                price=price, 
                property_description=property_description,
                address=address, 
                map_view=map_view,
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
            print(f'PROPERTY ADDED NOW {new_property}')
            print(f'Property ID ADDED NOW {new_property.id}')
           
            files = request.files.getlist('files[]')
            

            # Create a folder for each property to organize images
            property_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(property_id))
            for image_data in files:
                if image_data:
                    result = upload_image(property_id, image_data, property_folder)
                    print(result)
            if result:
                
                flash('Property added successfully')
            else:
                flash("Image dimensions are too Small/Large")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding property: {str(e)}")
            flash('Error adding property. Please try again', 'error')
    return render_template('add_property.html', segment="add_property") 


@app.route("/agent-upload", methods=['GET', 'POST'])
@login_required
def add_agent():
    if request.method == 'POST':
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        description = request.form['description']
        instagram = request.form['instagram']
        linkedin = request.form['linkedin']
        facebook = request.form['facebook']

     
        


        new_agent = Agent(
            name=name,
            email=email,
            phone=phone,
            description=description,
            instagram=instagram,
            linkedin=linkedin,
            facebook=facebook,
            image='nil'
        )


        try: 
            db.session.add(new_agent)
            db.session.commit()
           
            agent_id = new_agent.id

           
            files = request.files.getlist('files[]')
            

            # Create a folder for each property to organize images
            agent_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(agent_id))
            for image_data in files:
                if image_data:
                    result = upload_image(agent_id, image_data, agent_folder)
                    print(result)
            if result:
                
                flash('Agent added successfully')
            else:
                flash("Image dimensions are too Small/Large")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding agent: {str(e)}")
            flash('Error adding agent. Please try again', 'error')
    return render_template('add_agent.html', segment="add_agent") 


def is_image_valid(image_path, image_min_size, image_max_size, min_width, min_height, max_width, max_height):
    # Getting the image size
    image_size = os.path.getsize(image_path)
    if image_size < image_min_size or image_size > image_max_size:
        return False
    img = Image.open(image_path)
    width, height = img.size

    return width >= min_width and height >= min_height or width <= max_width and height <= max_height

def get_mimetype(file_path):
    return mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

def upload_image(property_id, image_data, property_folder):
     # Get the filename and check if it's allowed
    filename = secure_filename(image_data.filename)
    image_min_size = 1000
    image_max_size = 10 * 1024 * 1024
    min_width = 600
    min_height = 500

    max_width = 900
    max_height = 900

    target_size = (800, 600)
    temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_data.save(temp_file_path)

    if is_image_valid(temp_file_path, image_min_size, image_max_size, min_width, min_height, max_width, max_height):
    
        try:    
            
            if not image_data:
                return {"status": "error", "message": "No image data provided."}  

            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return {"status": "error", "message": "Invalid file type. Allowed types are png, jpg, jpeg, gif."}

        
            os.makedirs(property_folder, exist_ok=True)
 
            img = Image.open(temp_file_path)

            img_resized = img.resize(target_size, resample=Image.LANCZOS)

            # Create a new image with the target size and paste the resized image onto it
            padded_img = Image.new('RGB', target_size, (255, 255, 255))  # Create a white background
            left = (target_size[0] - img_resized.width) // 2
            top = (target_size[1] - img_resized.height) // 2
            padded_img.paste(img_resized, (left, top))
            
            

            # Save the image file
            
            file_path = os.path.join(property_folder, filename)
            print(f"File patH {file_path}")

            padded_img.save(file_path, quality=95)
            os.remove(temp_file_path)
            print("Image processing completed successfully. ")

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
            
            return True

        except Exception as e:
            app.logger.error(f"Error uploading image: {str(e)}")
            return {"status": "error", "message": "An unexpected error occurred during image upload."}
    else:
        return False


@app.route('/all-properties')
@login_required
def all_properties():
    properties = Property.query.all()
    image_dict = {}
    page = request.args.get('page', 1, type=int)
    per_page = 9
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(properties) + per_page - 1) // per_page

 
    property_on_page = properties[start:end]


    for property in properties:
        print(f'admin Property ID{property.id}')
        images = PropertyImage.query.filter_by(property_id=property.id).all()
        if images:
            image_dict[property.id] = images[0].image_path.split("static/", 1)[1]
    
    # view_images = [first_item.image_path.split("static/", 1)[1] for first_item in image_list]
    return render_template('home/tables.html', properties=property_on_page, images=image_dict, segment="all_properties", total_pages=total_pages, page=page)




@app.route('/edit-property/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_property(id):
    print(f"PROPERTY ID____ {id}")
    property = Property.query.get_or_404(id)
    images = PropertyImage.query.filter_by(property_id=id).all()
    image_list = []
    for image in images:
        image_list.append(image.image_path.split("static/", 1)[1])
    print(image_list)
    if request.method == 'POST':
        property.name = request.form.get('name')
        property.price = request.form.get('price')
        property.property_description = request.form.get('property_description')
        property.address = request.form.get('address')
        property.map_view = request.form.get('map_view')
        property.property_status = request.form.get('status')
        property.area = request.form.get('area')
        property.bathroom = request.form.get('bathroom')
        property.garage = request.form.get('garage')
        property.property_type = request.form.get('property_type')

        # Debugging: Print form data
        print("Form data received:", request.form)

        try:
            db.session.add(property) 
            db.session.commit()
            
            files = request.files.getlist('files[]')
            print("FILES RECEIVED: ", files)

            if files:
                property_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(property.id))
                os.makedirs(property_folder, exist_ok=True)

                for image_data in files:
                    if image_data and image_data.filename != '':
                        result = upload_image(property.id, image_data, property_folder)
                        print("UPLOAD RESULT:", result)
                        
                        

            flash("Your changes has been successfully applied")
        except Exception as e:
            db.session.rollback()
            flash('Error updating property')
            print(f'error updating property: {e}')
        return redirect(url_for('all_properties'))
    return render_template('home/edit_property.html', segment='edit_property', property=property, images=image_list, id=id)    

@app.route('/all-properties/delete/<int:id>')
@login_required
def delete_property(id):
    try:
        property = Property.query.get_or_404(id)
        upload_folder = app.config['UPLOAD_FOLDER']
        folder_id = os.path.join(upload_folder, str(id))
        shutil.rmtree(folder_id) # deletes the property image folder using the folder id
       
        print(f"Folder with ID {folder_id} deleted successfully.")


        if property:
            db.session.delete(property)
            db.session.commit()
            flash('Property deleted successfully')
        else:
            flash('Property not found')
    except Exception as e:
        flash('An error occurred while deleting the property')
        print(e)  
    return redirect(url_for('all_properties'))

    
# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@app.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500



if __name__=="__main__": 
    app.run(debug=True)


# jason2 dingidhgiW£$$  dingidhgiW£$

#  jefnu%£##S434



# upload agent photo then a single property img before adding more images