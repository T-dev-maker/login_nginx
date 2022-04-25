from flask import Flask, redirect,render_template,session,jsonify,request
import pymongo
import redis
from functools import wraps
app=Flask(__name__)
app.secret_key = 'dinhtran'
# Creat Database
r = redis.Redis(host="localhost",port=6379,)
client = pymongo.MongoClient('localhost',27017)
db = client.user_login_system
#Decorator
def login_required(f):
  @wraps(f)
  def wrap(*arg,**kwargs):
    if 'logged_in' in session:
      return f(*arg, **kwargs)
    else:
      return redirect('/')
  return wrap

# Routes(duong dan toi models)
from user import routes
@app.route('/')
def home():
  return render_template("home.html")

# @app.route('/delete')
# def xoa():
#   return render_template("delete.html")

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template("dashboard.html")

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200