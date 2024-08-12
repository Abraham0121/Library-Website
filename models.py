from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    # id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(30), nullable = False)

    favorites = db.relationship('Book', secondary = 'favorites')
    holds =  db.relationship('Book', secondary = 'holds')

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

favorites = db.Table("favorites",
    db.Column("username", db.String, db.ForeignKey("users.username"), primary_key = True),
    db.Column("book_isbn", db.String, db.ForeignKey("books.isbn"), primary_key = True)
)#Used to be a class called User_Favorites changed in order to accomadate many to many relationship around ljne 40

# add holds table
holds = db.Table(
    "holds",
    db.Column("username", db.String, db.ForeignKey("users.username"), primary_key=True),
    db.Column("book_isbn", db.String, db.ForeignKey("books.isbn"), primary_key = True)
)


def connect_db(app):
    db.init_app(app)


