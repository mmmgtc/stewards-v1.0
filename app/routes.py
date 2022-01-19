from app import app
from app.preprocess import preprocess

from flask.templating import render_template
from flask import request, jsonify

initial_list = preprocess()

@app.route("/", methods=["GET", "POST"])
def index():

    #Workstream_name = request.args.get('name')

    return render_template("index.html", stewards=initial_list)
