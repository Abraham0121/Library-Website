from flask import Flask, flash, request, redirect, render_template
from models import connect_db, User, Book, Category_Book, Book_Author, db
import requests, json


app=Flask(__name__)
app.app_context().push() 
# url='https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=AIzaSyDM7IREB5FJ2dom6ZIlXuW9rVxITR4qOyc'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///bookreads_database"
app.config['SECRET_KEY'] = "secret"


"""'https://www.googleapis.com/books/v1/volumes?key=AIzaSyDM7IREB5FJ2dom6ZIlXuW9rVxITR4qOyc'
does not work because it doesn't specify a book(?)"""

# res = requests.get(url)
# print(json.loads(res.text))

connect_db(app)

db.create_all()
"""@app.route('/login', methods=["POST"])
def login():
    pass"""
@app.route('/')
def hello_world():
    return render_template("home.html")

# @app.route('/1')
# def number_one():
#     return "<p> 1 </p>"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template('register.html')
    elif request.method=="POST":
        username=request.form['username']
        existing_user = User.query.filter_by(username=username).one_or_none()
        if existing_user:
            flash("This username already exists.")
            return render_template('register.html')
        else:
            user = (User(username=request.form['username'],
                        password=request.form['password']))
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created.")
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username, password=password).one_or_none()
        if existing_user:
            flash('You are now logged in.')
            return redirect('/')
        else:
            flash('Sorry those login credentials do not work. Try again')
            return render_template('login.html')


