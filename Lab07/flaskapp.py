from flask import render_template, request, redirect, url_for, flash
from __init__ import app, db
from models import User

@app.route('/')
def index():
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address is already taken!', 'danger')
            return redirect(url_for('signup'))

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('thankyou'))
    
    return render_template('signup.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for('secretPage'))
        else:
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/secretPage')
def secretPage():
    return render_template('secretPage.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
