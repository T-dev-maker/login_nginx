from time import time
from flask import Flask,jsonify, redirect,request, session,render_template
from flask import redirect
from passlib.hash import pbkdf2_sha256
from app import r
from sqlalchemy import true
from app import db
import uuid
class User:

    def start_session(self,user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user),200

    def signup(self):
        print(request.form)
        # tao mot doi tuong nguoi dung:
        user = {
            "_id":uuid.uuid4().hex,
            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "password":request.form.get('password')
        }

        # ma hoa mat khau:
        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        #kiem tra email da ton tai hay chua:
        if db.users.find_one({"email":user['email']}):
            return jsonify({"error":"Email da ton tai"}),400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"dang nhap that bai"}),400
    def signout(self):
        session.clear()
        return redirect('/')
    # dang nhap
    def login(self):
        user = db.users.find_one({
            "email":request.form.get('email')
        })
        if user and pbkdf2_sha256.verify(request.form.get('password'),user['password']):
            id = str(request.remote_addr)
            if r.exists(id) and int(r.get(id))<=10:
                count = int(r.get(id))
                r.mset({id:count+1})
                return self.start_session(user)
            elif int(r.get(id))>10:
                return jsonify({"error":"qua so lan dang nhap trong 1 ngay"}),401
            else:
                r.setex(id,86400,0)
        return jsonify({"error":"thong tin dang nhap khong hop le"}),401

    #xoa nguoi dung/
    def delete():
        if request.method == "POST":    
            user_email = request.form["email"]
            if user_email:
                customer = {
                    "email":user_email,
                }
                db.users.delete_one(customer)
        return render_template("xoa.html")
