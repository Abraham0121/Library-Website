from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique=True, nullable = False)
    password = db.Column(db.String(30), nullable = False)

    favorites = db.relationship('Book', secondary = 'favorites')

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key = True)
    kind = db.Column(db.String)
    publish_date = db.Column(db.String)
    publisher = db.Column(db.String)
    page_count = db.Column(db.String)
    maturity_rating = db.Column(db.String)
    average_rating = db.Column(db.String)
    image = db.Column(db.String)

class Book_Author(db.Model):
    __tablename__ = "book_authors"

    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    author = db.Column(db.String)

class Category_Book(db.Model):
    __tablename__ = "category_books"

    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    category = db.Column(db.String)

favorites = db.Table("favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key = True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key = True)
)#Used to be a class called User_Favorites changed in order to accomadate many to many relationship around ljne 40


def connect_db(app):
    db.init_app(app)


