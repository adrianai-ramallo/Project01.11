from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity
from datetime import datetime
#from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql import func
#to upload files
#from werkzeug.utils import secure_filename
#import os
#to validate emails:
import re


app = Flask(__name__)


#for validating emails taken from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


#--------------------------Upload Images




#..........................Database 

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#..........................Table User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #firstname = db.Column(db.String(100), nullable=False)
    #lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
   # age = db.Column(db.Integer)
   # password=db.Column(db.Char(10),nullable = False)
    #landlord=db.Column(db.int, nullable = False)
    #created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.id}>'

#..........................Table Review

class Review(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #content = db.Column(db.String(), nullable=False)
    #completed= db.Column(db.Integer, default=0)
    #date_created = db.Column(db.DateTime, default= datetime.utcnow)

    review_id = db.Column(db.Integer, primary_key=True)
    review_text= db.Column(db.String(), nullable=False)
    review_time = db.Column(db.DateTime, default=datetime.utcnow)
    #user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=True)
       

    def __repr__(self):
        #return f'<Review {self.id}>'
        return f'<Review {self.review_id}>'

from app import Review
#from app import User, Review



       


@app.route('/', methods=['POST','GET'])
def index():

    if request.method == 'POST':
        review_text =request.form['review_text']
        new_review = Review(review_text= review_text)

        try: 
            db.session.add(new_review)
            db.session.commit()
            #return redirect('/')
            return 'added'

        except:
            return 'Error'
    
    else:
        reviews=Review.query.order_by(Review.review_time).all()
        return render_template('index.html', reviews = reviews)


@app.route('/login', methods=['POST','GET'])
def userlogin():
    return render_template('login.html')


@app.route('/modal', methods=['POST','GET'])
def modal():
    return render_template('modal.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email =request.form['email']
        new_email= User(email= email)

        if (re.fullmatch(regex,email)):
        
            try:
                db.session.add(new_email)
                db.session.commit()
                #return redirect('/')
                return 'added'
                
                
            except:
                return 'Error'
        else:
            return 'Make sure you are adding a valid email'
    else:
        return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)
    TEMPLATES_AUTO_RELOAD=True