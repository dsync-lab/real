from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/property")
def property():
    return render_template("property-grid.html")
 
@app.route("/blog")
def blog():
    return render_template("blog-grid.html")

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


@app.route("/view-property")
def view_property():
    return render_template("property-single.html")

@app.route("/agent")
def agent():
    return render_template("agents-grid.html")

@app.route("/view-agent")
def view_agent():
    return render_template("agent-single.html")

@app.route("/admin")
def admin():
    return render_template("admin_templates/templates/index.html")


if __name__=="__main__":
    app.run(debug=True, host='192.168.74.157')



