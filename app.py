from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymoclarngo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["users"]

@app.route('/api', methods=['GET'])
def get_data():
    data = list(collection.find({}, {"_id": 0})) 
    return jsonify(data)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    try:
        collection.insert_one({"name": name, "email": email})
        return redirect(url_for("success"))

    except Exception as e:
        return render_template("form.html", error=str(e))

@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
