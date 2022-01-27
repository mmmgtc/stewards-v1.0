from app import app
from app.preprocess import preprocess
from app.helpers.helpers import get_proposals

from flask.templating import render_template

initial_list = preprocess()

@app.route("/", methods=["GET", "POST"])
def index():
    #proposals_data = get_proposals()
    #proposal_number = len(proposals_data)
    #print(number_prop.number)
    #if proposal_number != number_prop.number:
    #    initial_list, number_prop = preprocess()
    

    return render_template("index.html", stewards=initial_list)
