from ReadersClub import DATABASE
from ReadersClub.config.mysqlconnections import connectToMySQL
from flask import flash, session
from ReadersClub import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users(first_name, last_name, username, email, password) VALUES(%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s)"
        return connectToMySQL("readerscorner_db").query_db(query, data)
    
    @classmethod
    def get_users_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL('readerscorner_db').query_db(query, data)
        if not results:
            return False
        else:
            return cls(results[0])
        
# ================================== Validators 
    
    @staticmethod
    def confirm(user):
        is_valid = True
        if len(user['first_name']) == 0:
            flash('First Name is required.','err_users_first_name')
            is_valid = False
        if len(user['last_name']) == 0:
            flash('Last Name is required.','err_users_last_name')
            is_valid = False
        if len(user['email']) < 3:
            flash('Email is required.', 'err_users_email')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!",'err_users_email')
            is_valid = False
        if len(user['password']) == 0:
            flash('Password is required.','err_users_password')
            is_valid = False
        if user['password'] != user["confirm_password"]:
            flash('Password do not match','err_users_confirm_password')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['username']) == 0:
            flash('Username is required.')
            is_valid = False
        if len(user['password']) == 0:
            flash('Password is required.')
            is_valid = False
        if is_valid:
            potential_user = User.get_users_username({'username':user['username']})
            if not potential_user or not bcrypt.check_password_hash(potential_user.password, user['password']):
                flash('Incorrect Username or Password')
                is_valid = False
            else:
                session['uid'] = potential_user.id

            
        return is_valid