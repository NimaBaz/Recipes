from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

#! CREATE AKA REGISTER

@app.route("/register", methods = ['post'])
def register():
    print(request.form)

    # TODO validate our user
    if not User.validate_user(request.form):
        return redirect('/')

    # TODO hash the password
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)

    # TODO save the user to the database
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
    }
    user_id = User.save(data)

    # TODO log in the user
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']

    # TODO redirect user to app
    return redirect('/recipes')


#! READ and VERIFY AKA LOGIN

@app.route('/login', methods=['post'])
def login():
    # TODO see of the email is in our DB
    if not User.get_by_email(request.form):
        flash("Invalid Email/Password")
        return redirect('/')

    # TODO check to see of the password provided matches the password in our DB
    data = {
        "email": request.form['email']
    }
    user_in_db = User.get_by_email(data)
    password_valid = bcrypt.check_password_hash(user_in_db.password, request.form['password'])

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    
    if not password_valid:
        flash("Invalid Email/Password")
        return redirect('/')

    # TODO log in the user
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    
    # TODO redirect user to app
    return redirect('/recipes')


#! LOGOUT

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')