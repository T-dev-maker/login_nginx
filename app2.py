from crypt import methods
import json
from http import client
from flask import Flask, redirect,render_template,session,request
import pymongo
app=Flask(__name__)
app.secret_key = 'dinhtran'
#Creat Database
client = pymongo.MongoClient('localhost',27017)
db = client.user_login_system
@app.route('/',methods=["POST","GET"])
def delete():
    if request.method == "POST":    
        user_email = request.form["email"]
        if user_email:
            customer = {
                "email":user_email,
            }
            db.users.delete_one(customer)
    return render_template("delete.html")
@app.route('/update',methods=["POST","GET"])
def update():
    if request.method == "POST":    
        user_email = request.form["update_email"]
        user_name = request.form["update_name"]
        user_pass = request.form["update_password"]
        if user_email:
            user = db.users.find_one({
            "email":request.form.get('update_email'),
            })
            myquery = { "email": str(user_email) }
            newvalues = { "$set": { "name": str(user_name),"password":str(user_pass)} }
            db.users.update_one(myquery,newvalues)
    return render_template("xoa.html")
if __name__ =="__main__":
    app.run(debug=True,port=3000)
