from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from .import db

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    return render_template("login.html",boolean=True)

@auth.route('/logout')
def logout():
    return "<p>LOGOUT</p>"

@auth.route('/sign-up',methods=['GET','POST'])

def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        lastName=request.form.get('lastName')
        password=request.form.get('password')
        password2=request.form.get('password2')

        if len(email)<4:
            flash('Email entered should be more than 3 charaters',category = 'error')
        elif len(firstName)<2:
            flash('First name is too short',category='error')
        elif len(lastName)<2:
            flash('Last name is too short',category = 'error')
        elif password!=password2:
            flash('passwords do not match',category = 'error')
        elif len(password)<7:
            flash('passsword is too short',category = 'error')
        else:
            new_user=User(email=email,firstName=firstName,lastName=lastName,password=generate_password_hash(password,method = 'pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!',category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")