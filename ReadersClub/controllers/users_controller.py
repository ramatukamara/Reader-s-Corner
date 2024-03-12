from ReadersClub import app, bcrypt
from flask import render_template, redirect, request, session
from ReadersClub.models.users_model import User


# =================================================================== Login Form Submission Route

@app.route('/')
def first_page():
    return render_template('index.html') 

@app.route('/login', methods=['POST'])
def login():
    if 'uid' in session:
        return redirect ('/homepage')
    if not User.validate_login(request.form):
        return redirect('/')
    
    user = User.get_users_username(request.form['username'])
    session['uid'] = user.id

    return redirect('/homepage')

# ===================================================================== Register Route

# Register Page Route
@app.route('/registration', methods=['GET'])
def register_page():
    return render_template('register.html')

# Register Form Submission Route
@app.route('/register', methods=['POST'])
def register():
    # if not User.get_users_username(request.form):
    #     return redirect('/registration')
    
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': hashed_password
    }
    session['uid'] = User.create(user_data)

    return redirect('/')

# ===========================================================Logout Route

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')