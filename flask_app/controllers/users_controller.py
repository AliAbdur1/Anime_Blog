from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash
from flask_app.models.users_model import Users
from flask_app.models.animes_model import Animes



@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/user/route goes here!', methods=['POST']) #Post request route
def rename1():
    return redirect('/route path goes here!')

@app.route('/user/list')
def all_registerd():
    # vv will not show users page if id is not in session vv
    if 'new_user_id' not in session: # new line 39:52
        return redirect ('/') # new line 39:52
    users = Users.get_all_users()
    print("^^^^^^^", users)
    return render_template('all_users.html', all_users = users)

@app.route('/user/register', methods=['POST']) #Post request route
def add_a_user():
    if not Users.registration_validation(request.form): # works!
        return redirect('/') # works!
    # new line
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    Users.new_register(data)
    Users.new_register(request.form)
    return redirect('/user/profile')

@app.route('/user/profile')
def profil_page():
    if 'new_user_id' not in session:
        return redirect('/')
    Users.get_user_by_id()
    anime = Animes.get_all_animes() # change back to get_all_shows if thid no work
    return render_template('user_profile_page.html', animes_to_watch = anime, user_list = Users.get_all_users())# <-- may have to do that id data thingy


## Login Logout ##
@app.route('/user/login', methods=['POST'])
def login():
    if Users.login(request.form): # may need user before User
        return redirect('/user/profile')# may need to change to list
    return redirect('/')

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')