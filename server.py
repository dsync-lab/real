from flask import Flask, render_template, request


app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


properties = {
    1: {"id": 1, "name": "property-1", "price": "$340,000", "address": "Olive Road Two", "image": "property-1"},
    2: {"id": 2, "name": "property-3", "price": "$290,000", "address": "Pear Road Four", "image": "property-3"},
    3: {"id": 3, "name": "property-6", "price": "$420,000", "address": "Banana Road Eight", "image": "property-6"},
    4: {"id": 4, "name": "property-7", "price": "$270,000", "address": "Grape Road Nine", "image": "property-7"},
    5: {"id": 5, "name": "property-8", "price": "$460,000", "address": "Apple Road Eleven", "image": "property-8"},
    6: {"id": 6, "name": "property-8", "price": "$360,000", "address": "Apple Road Eleven", "image": "property-8"},
    
}

rent_properties = {
    1: {"id": 1, "name": "property-1", "price": "$6,000", "address": "Olive Road Two", "image": "property-1"},
    2: {"id": 2, "name": "property-3", "price": "$9,000", "address": "Pear Road Four", "image": "property-3"},
    3: {"id": 3, "name": "property-6", "price": "$8,500", "address": "Banana Road Eight", "image": "property-6"},
    4: {"id": 4, "name": "property-7", "price": "$4,600", "address": "Grape Road Nine", "image": "property-7"},
    5: {"id": 5, "name": "property-8", "price": "$5,000", "address": "Apple Road Eleven", "image": "property-8"},
    6: {"id": 6, "name": "property-8", "price": "$6,400", "address": "Apple Road Eleven", "image": "property-8"},
    
}

@app.route("/property") 
def property():
    return render_template("property-grid.html", properties=properties)
 
@app.route("/rent")
def rent():
    return render_template("rent-grid.html", properties=rent_properties)

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

# @app.route("/view/<int:num>")
# def debug_page(num):
    #     return render_template("property-single.html", number=num)



@app.route("/property-view/<int:property_id>")
def view_property(property_id):
    print(f"========{property_id}=========")
    property_data = properties.get(property_id)
    if property_data:
        print(f"========{property_data}=========")
        return render_template("property-single.html", property_data=property_data) 
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


if __name__=="__main__":
    app.run(debug=True, host="192.168.74.157")



