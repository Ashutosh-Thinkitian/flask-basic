from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello..welcome to flask application"

@app.route('/new')
def query_string():
    query_val = request.args.get('greetings', 'hello')
    return '<h1> The Greeting is : {0} </h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>')
def no_query_string(name='patil'):
    return '<h2> Hello there Power = {} </h2>'.format(name)

# pass string in query string
@app.route('/text')
@app.route('/text/<string:name>')   # this variable and function variable must be same
def working_with_string(name='Mavala'):
    return '<h2> You passed this string = '+name+ '</h2>'.format(name)

# pass integer in url means query string(may be)
@app.route('/add/<int:num1>/<int:num2>')
def addition(num1, num2):
    return '<h1> Addition ={} </h2>'.format(num1+num2)

# one more example with integer
@app.route('/integer/<int:num>')
def working_with_integer(num):
    return '<h1> You passed this integer '+str(num)+ '</h1>'    # without using format

# pass floating point numbers
@app.route('/product/float/<float:num1>/<float:num2>')
def working_with_float(num1, num2):
    return '<h1> Product of '+ str(num1) + ' X ' +str(num2) +' = {} </h1>'.format(num1*num2)

#    rendering html -> the folder name must be templates
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

#   introduced jinja template
@app.route('/watch')
def top_movies():
    movie_list = [
        '3 idiots',
        'Kai po chee',
        'Ranzanaa',
        'Bahubali',
        'Sketch',
        'Family man'
    ]
    return render_template('movie.html', movies=movie_list, name='Ashutosh Patil')

# if else in jinja2
@app.route('/tables')
def movies_plus():
    movies_dict ={
        '3 idiots': 300,
        'Kai po chee': 50,
        'Ranzanaa': 80,
        'Bahubali': 900,
        'Sketch': 35,
        'Family man': 350
    }
    return render_template('tables.html', movies_di=movies_dict, name='Box office collection')

# learning jinja filter
@app.route('/filter')
def filter_data():
    movies_dict = {
        '3 idiots': 300.80,
        'kai po chee': 50.23,
        'ranzanaa': 80.40,
        'bahubali': 900.57,
        'sketch': 35.12,
        'family man': 350.67
    }
    return render_template('filter_data.html', movies=movies_dict, name=None, film='Zindagi na milegi dobara')

@app.route('/macros')
def jinja_macros():
    movies_dict ={
        '3 idiots': 300,
        'Kai po chee': 50,
        'Ranzanaa': 80,
        'Bahubali': 900,
        'Sketch': 35,
        'Family man': 350
    }
    return render_template('using_macros.html', movies_di=movies_dict)

# for database connection
app.config.update(

    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:root@localhost/flask',
    # database://user_id:password@server/database_name
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)    # create db database instance and pass flask instance

#   create database table
# Inheritance with db.Model - SQLAlchemy
class Publication(db.Model):
    __tablename__ ='publication'    # this is table name must be same with class name..but not capitalize

    # create columns
    id = db.Column(db.Integer, primary_key=True)  # --> remove  in  __init__() (Later changes)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The Publisher name is {}'.format(self.name)

# create class for another table
class Book(db.Model):
    __tablename__ ='book'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    #   one to many relationship because each publication have more than one book
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))  # create foreign key with id from publication table

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        # self.id =id --> did not need because SQLAlchemy automatically fill this
        self.title =title
        self.author =author
        self.avg_rating=avg_rating
        self.format = book_format
        self.image = image
        self.num_pages =num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {} '.format(self.title, self.author)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)