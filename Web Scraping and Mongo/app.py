from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html", 
      four_pics=[mars for mars in mongo.db.four_pics.find()])

@app.route("/scrape")
def scrape():
    mongo.db.four_pics.drop()
    four_pics = mongo.db.four_pics  
    four_pics_data = mission_to_mars.scrape_url()
    for mars in four_pics_data:
        four_pics.insert_one(mars)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=False)
