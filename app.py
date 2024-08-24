from flask import Flask, jsonify, flash, request, redirect, render_template, session
from models import connect_db, User, Book, Category_Book, Book_Author, db, Review
import requests, json
from events import socketio


app=Flask(__name__)
app.app_context().push() 

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://bookreads_database_owner:BrnwRdX8x1qZ@ep-noisy-water-a5s3a863.us-east-2.aws.neon.tech/bookreads_database?sslmode=require"
app.config['SECRET_KEY'] = "secret"
app.config["DEBUG"] = True

# app.register_blueprint(main)

socketio.init_app(app)

BASE_URL='https://www.googleapis.com/books/v1/volumes?q=a' # need to add '&key=' to use API KEY
API_KEY = 'AIzaSyDM7IREB5FJ2dom6ZIlXuW9rVxITR4qOyc'


# res = requests.get(url)
# print(json.loads(res.text))

connect_db(app)

# db.drop_all()
db.create_all()
        

@app.route('/')
def homepage():
    final_url = BASE_URL
    if 'title' in request.args and request.args['title']:
        final_title = request.args['title']
        if " " in final_title:
            title_list= request.args['title'].split()
            final_title= '+'.join(title_list)
        final_url += '+intitle=' + final_title+ '+'
    if 'author' in request.args and request.args['author']:
        final_author= request.args['author']
        if " " in final_author:
            author_list= request.args['author'].split()
            final_author= '+'.join(author_list)
        final_url += '+inauthor=' + final_author + '+'
    if 'category' in request.args and request.args['category']:
        final_category = request.args['category']
        if " " in final_category:
            category_list= request.args['category'].split()
            final_category= '+'.join(category_list)
        final_url += '+subject=' + final_category + '+'
    final_url += '&key=' + API_KEY
    
    res = json.loads(requests.get(final_url).text)
    books = res['items']
    for book in books:
        if not Book.query.filter_by(title=book['volumeInfo']['title']).one_or_none():
            description=""
            image=""
            if 'description' in book['volumeInfo']:
                description = book['volumeInfo']['description']
            if 'imageLinks' in book['volumeInfo']:
                image=book['volumeInfo']['imageLinks']['thumbnail'] 
            db_book = Book(
                isbn=book['volumeInfo']['industryIdentifiers'][0]['identifier'],
                title=book['volumeInfo']['title'],
                maturity_rating=book['volumeInfo']['maturityRating'],
                description=description,
                image=image  
            )
            db.session.add(db_book)
            db.session.commit()
        
    first_ten_books = res['items'][:10]
    favorites = []
    if 'username' in session:
        # cleaned up code by removing favorites and passed in user instead of User
        user = User.query.get(session['username'])
        return render_template('home.html', books=first_ten_books, user=user)

    return render_template('home.html', books=first_ten_books, user=None)

################################################### Register/Login/Logout ##############

@app.route('/register', methods=['GET','POST'])
def register(): 
    """ Register """
    if request.method=="GET":
        return render_template('register.html')
    elif request.method=="POST":
        username=request.form['username']
        existing_user = User.query.filter_by(username=username).one_or_none()
        if existing_user:
            flash("This username already exists.", "danger")
            return render_template('register.html')
        else:
            user = User(
                username=request.form['username'],
                password=request.form['password']
            )
            
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created.", "success")
            session['username'] = username
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login """

    if request.method =='GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username, password=password).one_or_none()
        if existing_user:
            flash('You are now logged in.', "success")
            session['username'] = username
            return redirect('/')
        else:
            flash('Sorry those login credentials do not work. Try again', "danger")
            return render_template('login.html')

@app.route('/logout')
def logout():
    """ Logout """

    if 'username' in session:
        session.pop('username')
        flash('You have successfully logged out', "success")
        return redirect('/')
    else:
        flash('You are not logged in', "danger")
        return redirect('/login')

@app.route('/books/<isbn>')
def book_detail(isbn):
    """ Shows Book Detail Page """

    if 'username' in session:
        book = Book.query.get(isbn)
        user = User.query.get(session['username'])
        print(Review.query.all())
        print(user.reviews, "reviews")
        if book:
            return render_template('book_detail.html', book=book, user=user)

        flash('This book does not exist.', "danger")
        return redirect('/')

    flash('Please login to use this feature.', "danger")
    return redirect('/login')

################################################### Favorite Books ##############

@app.route('/books/favorites')
def get_favorite_books():
    """ Get all your favorite books """
    # Note: you should add a link in the nav linking to this route
    user = User.query.get(session['username'])

    return render_template('favorites.html', user=user)


@app.route('/books/<isbn>/favorite', methods=['POST'])
def favorite_book(isbn):
    """ Favorite a book """

    book = Book.query.get(isbn)
    if 'username' in session:
        # not sure why it worked. Note: I simplified by using has_favorite method instead of for loop
        user = User.query.get(session['username'])
        if  user.has_favorite(isbn):
            user.favorites.remove(book)
            db.session.commit()
            print("hELLO")
            return jsonify({"unfavorited": isbn})       
        else:
            user = User.query.get(session['username'])
            user.favorites.append(book)
            db.session.add(user)
            db.session.commit()
            return jsonify({"favorited": isbn})

################################################### Books on Hold ##############

@app.route('/books/onhold')
def show_books():
    """ render books_on_hold.html with all variables needed. Read the html file for more details"""
    # Make sure to add a link in the nav to this route
    user = User.query.get(session['username'])

    return render_template("books_on_hold.html", user=user)

@app.route('/books/<isbn>/hold', methods=['POST'])
def make_hold(isbn):
    """ Put a book on hold or remove hold """
    # Note: 1) You should add someway to put a hold on books on the book previews on the homepage.
    # You can use a basic button, a fontawesome icon, or etc. Just make sure that it adds a hold 
    # or removes a hold based on whether or not the user already has it on hold.
    # 2) To do this you should make the appropiate table in the models.py file.
    book = Book.query.get(isbn)
    if 'username' in session:
        user = User.query.get(session['username'])
        if user.has_hold(isbn):
            user.holds.remove(book)
            db.session.commit()
            return jsonify({"Not On Hold": isbn})
        else:
            user = User.query.get(session['username'])
            user.holds.append(book)
            db.session.commit()
            return jsonify({"On Hold": isbn})



    return "dummy return"

################################################### Extra Implementations ##############

################################################### Messages ##############

# Use websockets to allow a real live chat between a librarian and a user
# Noah has never used websockets so this will be a learning experience

################################################### Book reviews ##############

# Would need to make appropiate table(s)
# make a route for making a review
# display averge rating on book previews
# display reviews on bottom of book detail page

@app.route('/books/<isbn>/review', methods=['GET','POST'])
def book_review(isbn):
    book = Book.query.get(isbn)
    user = User.query.get(session['username'])
   
    if user.has_review(isbn):
        #display the previous review
        flash("You have already reviewed this book.",'danger')
        return redirect('/')
    else:
        #make a review
        #ask user for number of stars
        #ask user for text review
        number_of_stars = 0
        review_text = ""
        if 'num-of-stars' in request.form:
            number_of_stars = request.form['num-of-stars']
        if 'review-text' in request.form:
            review_text = request.form['review-text']
        if number_of_stars and review_text:
            print("HELLO1")
            review = Review(text = review_text, number_of_stars = number_of_stars, username= session['username'], book_isbn=isbn)
            print(review)
            db.session.add(review)
            db.session.commit()
       
    return redirect('/')

################################################### Show nearby libraries ##############

# Would need to use google maps api
# and if possible we could link to their websites

if __name__ == '__main__':
    socketio.run(app)