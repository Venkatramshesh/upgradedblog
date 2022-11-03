from flask import Flask, render_template, request
import requests
import smtplib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
import os
from form import CreatecommentForm
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor


app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = os.environ.get('api_key')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///C:/USers/venka/Python100days/Upgradedblog/comments.db")
db = SQLAlchemy(app)

my_email = "vramshesh@gmail.com"
passwd=os.getenv("passwd")

class comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    blogURL = "https://api.npoint.io/7a78376933651c927713"
    response = requests.get(blogURL)
    allposts = response.json()
    return render_template('index.html', posts=allposts)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post/<int:index>')
def post(index):
    blogURL = "https://api.npoint.io/7a78376933651c927713"
    response = requests.get(blogURL)
    allposts = response.json()
    return render_template('post.html', posts=allposts, num=index)

@app.route('/from_entry', methods=["POST"])
def from_entry():
    if request.method == 'POST':
        print(request.form["fname"])
        print(request.form["email"])
        print(request.form["phone"])
        print(request.form["message"])

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(my_email, passwd)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject:Hey\n\n Name: {request.form['fname']}\nE-mail: {request.form['email']}\nPhone:{request.form['phone']}\n{request.form['message']}")

    return render_template('from_entry.html')

@app.route('/comment',methods=["GET","POST"])
def comment():
    form = CreatecommentForm()
    if form.validate_on_submit():
       post = comments(text=form.body.data,name=form.name.data)
       db.session.add(post)
       db.session.commit()
       blogURL = "https://api.npoint.io/7a78376933651c927713"
       response = requests.get(blogURL)
       allposts = response.json()
       return render_template('index.html', posts=allposts)
    return render_template('comment.html', form=form)

if __name__=="__main__":
     app.run(debug=True)
     serve(app, host='0.0.0.0', port=80)