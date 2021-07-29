from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import pandas as pd
import os
from pymongo import MongoClient
from guppy import hpy
from memory_profiler import profile
from flask import jsonify, json,make_response, current_app as app
import wtforms as wt
from wtforms import TextField, Form
app = Flask(__name__)


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res

if __name__=='__main__':
    app.run(debug=True, port=5000, threaded=True)