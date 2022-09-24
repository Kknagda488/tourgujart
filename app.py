from flask import Flask, render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_mail import Mail
from flask_login import LoginManager,login_user,UserMixin,logout_user

with open('config.json', 'r') as C:
    params = json.load(C) ["params"]
local_server = True
app =Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'],
)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-Krishna'],
    MAIL_PASSWORD = params['krishna-password']
)
mail = Mail(app)
if(local_server):
    app.config[ 'SQLALCHEMY_DATABASE_URI' ] = params['local_uri']

else:
    app.config[ 'SQLALCHEMY_DATABASE_URI' ] = params['prod_uri']

app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False
app.config['SECRET_KEY'] = params['secret_key']
db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=False)
    user_email = db.Column(db.String(20), nullable=False, unique=False)
    user_num = db.Column(db.String(12),  nullable=False, unique=False)
    password = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=True)
    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
    

@app.route('/')
def home():
    return render_template('index.html', params=params)
@app.route('/ahmedabad')
def ahmedabad():
    return render_template('ahmedabad.html', params=params)

@app.route('/dwarka')
def dwarka():
    return render_template('dwarka.html', params=params)

@app.route('/kutch')
def kutch():
    return render_template('kutch.html', params=params)
@app.route('/mehsana')
def mehsana():
    return render_template('mehsana.html', params=params)

@app.route('/statueOfUnity')
def statueOfUnity():
    return render_template('statueOfUnity.html', params=params)
@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route("/contact", methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num=phone, msg=message, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + email,
                          sender = email,
                          recipients = [params['gmail-user']],
                          body = name + "\n" + message + "\n" + phone
                          )
        mail.send_message('New message from ' + email,
                          sender = email,
                          recipients = [params['gmail-Krishna']],
                          body = name + "\n" + message + "\n" + phone
                          )
        if len(message) > 1:
            flash('Sent Sucessfully','success')
            # return redirect('/contact')
    return render_template('contact.html', params=params)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user and password==user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid Credentials','warning')
            return redirect('/login')




    return render_template('login.html', params=params)







@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        username = request.form.get('username')
        user_email = request.form.get('user_email')
        user_num = request.form.get('user_num')
        password = request.form.get('password')
        entry = Users(user_name=user_name, user_num=user_num,username=username, password=password, user_email=user_email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash('user has been register successfuly','success')
        return redirect('/login')
    return render_template('signup.html',params=params)
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)

