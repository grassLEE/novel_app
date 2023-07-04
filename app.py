import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sometext'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir,  'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(800), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    pages = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Book {self.title}>'
    

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/<int:book_id>/')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)


@app.route('/addBook/', methods=('GET', 'POST'))
def addBook():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        genre = request.form['genre']
        book = Book(author=author,
                    title=title,
                    pages=pages,
                    genre=genre)
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('addBook.html')


@app.route('/<int:book_id>/edit/', methods=('GET', 'POST'))
def edit(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = int(request.form['pages'])
        genre = request.form['genre']

        book.title = title
        book.author = author
        book.pages = pages
        book.genre = genre

        db.session.add(book)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('edit.html', book=book)


@app.post('/<int:book_id>/delete/')
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/landing')
def landing():
    flash("What's your favorite genre?")
    return render_template('landing.html')

@app.route('/greet', methods=['POST', 'GET'])
def greet():
    flash("Fantastic! " + str(request.form['name_input']) + " is one of my favorites, too!")
    return render_template("landing.html")
