from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    # id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(30), nullable = False)
    is_librarian = db.Column(db.Boolean, default=False)

    favorites = db.relationship('Book', secondary = 'favorites')
    holds =  db.relationship('Book', secondary = 'holds')
    messages = db.relationship('Message', lazy='dynamic',foreign_keys='Message.to_username')
    reviews = db.relationship('Review')

    def has_favorite(self, isbn):
        for favorite in self.favorites:
            if favorite.isbn==isbn:
                return True
        return False
    
    def has_hold(self, isbn):
        for hold in self.holds:
            if hold.isbn ==isbn:
                return True
        return False
    
    def has_review(self, isbn):
        for review in self.reviews:
            if isbn == review.book_isbn:
                return True
        return False
        

class Book(db.Model):
    __tablename__ = "books"

    isbn = db.Column(db.String, primary_key = True)
    kind = db.Column(db.String)
    title = db.Column(db.String) #FORGOT TO ADD BEFORE?
    publish_date = db.Column(db.String)
    publisher = db.Column(db.String)
    page_count = db.Column(db.String)
    maturity_rating = db.Column(db.String)
    average_rating = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.String)

    categories = db.relationship('Category_Book')
    authors = db.relationship('Book_Author')
    reviews = db.relationship('Review')

    def __eq__(self, other):
        return self.isbn == other.isbn

class Book_Author(db.Model):
    __tablename__ = "book_authors"

    id = db.Column(db.Integer, primary_key = True)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"))
    author = db.Column(db.String)

class Category_Book(db.Model):
    __tablename__ = "category_books"

    id = db.Column(db.Integer, primary_key = True)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"))
    category = db.Column(db.String)

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String, nullable= False)
    from_username = db.Column(db.String, db.ForeignKey("users.username"))
    to_username = db.Column(db.String, db.ForeignKey("users.username"))

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String, nullable= False)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"))
    username = db.Column(db.String, db.ForeignKey("users.username"))
    number_of_stars = db.Column(db.Integer, nullable=False)

    def is_ok(self):
        return (self.number_of_stars >= 1 and self.number_of_stars <= 5)

favorites = db.Table("favorites",
    db.Column("username", db.String, db.ForeignKey("users.username"), primary_key = True),
    db.Column("book_isbn", db.String, db.ForeignKey("books.isbn"), primary_key = True)
)

# add holds table
holds = db.Table(
    "holds",
    db.Column("username", db.String, db.ForeignKey("users.username"), primary_key=True),
    db.Column("book_isbn", db.String, db.ForeignKey("books.isbn"), primary_key = True)
)
 


def connect_db(app):
    db.init_app(app)


