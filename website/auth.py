from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from .import db
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')


        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully ',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect!Please try again!',category='error')
        else:
            flash('Email doesnot exist',category='error')
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])

def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        lastName=request.form.get('lastName')
        password=request.form.get('password')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.',category='error')
        elif len(email)<4:
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
            login_user(user,remember=True)
            flash('Account created!',category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html",user=current_user)