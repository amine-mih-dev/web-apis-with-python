from flask import Flask, request, render_template, redirect
from markupsafe import escape
app = Flask(__name__)

@app.get("/")
def index():
    """
    TODO: Render the home page provided under templates/index.html in the repository
    """
    return render_template("index.html")

@app.get("/search")
def search():
    q = escape(request.args.get("q"))
    """
    TODO:
    1. Capture the word that is being searched
    2. Seach for the word on Google and display results
    """
    print(request.form)
    return redirect("https://www.google.com/search?q=" + q)

@app.get("/lucky")
def lucky():
    q = escape(request.args.get("q"))
    print(q)
    return redirect("https://www.google.com/search?btnI=1&q={}".format(q))


if __name__ == "__main__":
    app.run(debug = True)