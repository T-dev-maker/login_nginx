from crypt import methods
from flask import Flask
from app import app
from user.models import User
@app.route('/user/signup',methods=['POST'])
def signup():
    return User().signup()
@app.route('/user/signout')
def signout():
    return User().signout()
@app.route('/user/login',methods=['POST'])
def login():
    return User().login()
# @app.route('/user/delete',methods=['POST'])
# def delete_User():
#     return User().delete()
@app.route('/user/update',methods=['POST'])
def update_User():
    return User().update()

