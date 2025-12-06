from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["users"]

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json()

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"message": "Missing fields"}), 400

    todo = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    collection.insert_one(todo)

    return jsonify({"message": "Todo item saved successfully"}), 201

@app.route('/api', methods=['GET'])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

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
