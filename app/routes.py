from app import app
from app.preprocess import preprocess

from flask.templating import render_template
from flask import request, jsonify

initial_list = preprocess('fast')
#initial_list = preprocess('slow')

@app.route("/", methods=["GET", "POST"])
def index():

    #workstream_name = request.args.get('workstream_name')

    return render_template("index.html", stewards=initial_list)