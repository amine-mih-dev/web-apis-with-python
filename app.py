from flask import Flask, jsonify, request, url_for, render_template
from markupsafe import escape
# Intitialise the app
app = Flask(__name__)

# Define what the app does
@app.get("/groot")
def index():
    """
    TODO:
    1. Capture first name & last name
    2. If either is not provided: respond with an error
    3. If first name is not provided and second name is provided: respond with "Hello Mr <second-name>!"
    4. If first name is provided byt second name is not provided: respond with "Hello, <first-name>!"
    5. If both names are provided: respond with a question, "Is your name <fist-name> <second-name>
    """

    name = escape(request.args.get( "name" ))
    last_name = escape(request.args.get( "last_name"))
    if (not name) and (not last_name):
        return jsonify({ "status" : "error" })
    elif (not name) and last_name:
        return jsonify({ "data" : "Hello, Mr {}!".format(last_name.capitalize()) })
    elif name and (not last_name):
        return jsonify({ "data" : "Hello, {}!".format(name.capitalize()) })
    else:
        return jsonify({ "data" : "Is your name {} {}?".format(name.capitalize(), last_name.capitalize()) })

@app.get("/")
def home():
    name = request.args.get( "name" )
    last_name = request.args.get( "last_name")
    if (not name) and (not last_name):
        color = "#e44100;"
        response = { "data" : "error" , "color" : color }
    elif (not name) and last_name:
        color = "#00a0bd;"
        response = { "data" : "Hello, Mr {}!".format(last_name.capitalize()), "color" : color }
    elif name and (not last_name):
        color = "#00e457;"
        response = { "data" : "Hello, {}!".format(name.capitalize()), "color" : color }
    else:
        color = "#e4af00;"
        response = { "data" : "Is your name {} {}?".format(name.capitalize(), last_name.capitalize()), "color" : color }
        print(response['data'])
    return render_template("index.html",response=response)

if __name__ == "__main__":
    app.run(debug=True)