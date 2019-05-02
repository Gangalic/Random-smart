#!/usr/bin/env python
import os
import mysql.connector
import pymysql
from mysql.connector import Error
from mysql.connector import errorcode
from hashlib import md5
from flask import Flask, abort, request, jsonify, g, url_for


# initialization
app = Flask(__name__)
##-----------------------------------------------------------------------
dbconx = None

db = [
    {
        'email' : 'suka@gmail.com',
        'username' : 'suka',
        'password_hash' : '1937f167ce4a58749368ca8e815336da' #suka
    },
    {
        'email' : 'puta@gmail.com', 
        'username' : 'puta',
        'password_hash' : '2309f522cab926b42f4463fc656bd87f' #madre
    }
]

##------------------------------------------------------------------------

class User:

    def __init__(self, email, username, password_hash = ''):
        self.email = email
        self.username = username
        self.password_hash = password_hash

    def hash_password(self, password):
        self.password_hash = md5(password).hexdigest()

    def verify_password(self, password):
        return md5(password).hexdigest() == self.password_hash
    
    @staticmethod
    def search_user(email):
        #DB QUERY ---------------------------------------------------------------
        cursor = dbconx.cursor()
        cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
        records = cursor.fetchall()
        cursor.close()
        #DB QUERY END ------------------------------------------------------------
        for user in records:
            if user[0] == email:
                return User(email = email,username = user[1], password_hash = user[2])
        return None
    @staticmethod
    def add_user(user):
        #DB QUERY ---------------------------------------------------------------
        cursor = dbconx.cursor()
        query = "INSERT INTO users (email, username, pass_hash)\
            VALUES(\
                '" + user.email + "','" + user.username + "','" + user.password_hash +"'\
            )"
        cursor.execute(query)
        dbconx.commit()
        cursor.close()
        #DB QUERY END ------------------------------------------------------------


@app.route('/lyon_quest/users/login/', methods=['POST'])
def verify_login():
    user = User.search_user(request.json['email'])
    if not user or not user.verify_password(request.json['password']):
        return jsonify({'status' : 'failure', 'error' : 'You have entered an invalid email or password'})
    return jsonify({'status' : 'success'})


@app.route('/lyon_quest/users/register/', methods=['POST'])
def new_user():
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    if User.search_user(email) is not None:
       return jsonify({'status' : 'failure', 'error' : 'This email is already used'})
    user = User(email = email, username = username)
    user.hash_password(password)
    User.add_user(user)
    return jsonify({'status' : 'success'})

@app.route('/lyon_quest/resource/', methods = ['GET'])
def get_resource():
    return jsonify({'data': 'Hello there!'})


if __name__ == '__main__':
    try:
        print("hui")
        # The SQLAlchemy engine will help manage interactions, including automatically
        # managing a pool of connections to your database
        dbconx = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername='mysql+pymysql',
                username='root',
                password='smartroot',
                database='smart',
                query={
                    'unix_socket': '/cloudsql/{}'.format('lyon-quest:europe-west1:lyon-quest-db')
                }
            )
        )
        print("dupa")
        print(dbconx)
    except mysql.connector.Error as error :
        print("Failed inserting record into python_users table {}".format(error))

    app.run(host = '127.0.0.1', port = 5000)

