from flask import Flask, render_template, request
import requests
import smtplib
from waitress import serve
import os


app = Flask(__name__)

my_email = "vramshesh@gmail.com"
passwd=os.getenv("passwd")


# @app.route('/')
# def logout():
#     session.clear()
#     return

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

if __name__=="__main__":
     app.run(debug=True)
     serve(app, host='0.0.0.0', port=80)