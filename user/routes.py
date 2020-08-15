from flask import Flask, request, jsonify, make_response, session, app, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
import json
from user import app, db
from .models import User
from flask import render_template, redirect, url_for, flash
import datetime

@app.route('/register', methods=['POST'])
def register():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(username=post_data.get('username')).first()
    if not user:
        user = User(
            username=post_data.get('username'),
            useremail=post_data.get('useremail'),
            password=post_data.get('password')
        )
        # insert the user data
        db.session.add(user)
        db.session.commit()
        responseObject = {
            'Message': 'Registration successful'
        }
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'Message': 'Check the fields entered',
        }
    return make_response(jsonify(responseObject)), 400


@app.route('/login', methods=['POST'])
def login():
    # get the post data from authorization 
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    #decode base64 data received
    import base64
    message_bytes = base64.b64decode(auth_token)
    message = message_bytes.decode('ascii')
    if message:
        # fetch the user data
        user = User.query.filter_by(
            username=message.strip().split(":")[0],password=message.strip().split(":")[1]).first()
        if user:
            responseObject = {
                'Message': 'Login success'
            }
            resp = make_response(jsonify(responseObject))
            #creating and storing session details
            session['username'] = user.username
            session['password'] = user.password
            return resp, 200
        else:
            responseObject = {
            'Message': 'Could not verify'
        }
            resp = make_response(jsonify(responseObject))
            return resp, 400
    else:
        responseObject = {
            'Message': 'Could not verify'
        }
        resp = make_response(jsonify(responseObject))
        return resp, 400

@app.route('/logout', methods=['POST'])
def logout():
  try:
    #during logout, if session exists then remove the session
    if session['username']:
        session.pop('username', None)
        responseObject = {
            'Message': 'Logout successful'
        }
        resp = make_response(jsonify(responseObject))
        return resp, 200
    else:
        responseObject = {
            'Message': 'Already logged out'
        }
        resp = make_response(jsonify(responseObject))
        return resp, 400
  except:
    responseObject = {
            'Message': 'Already logged out'
        }
    resp = make_response(jsonify(responseObject))
    return resp, 400