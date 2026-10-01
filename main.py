from flask import Flask, render_template, request, redirect, url_for, session

from data_base import get_login, get_profile, create_user, make_post, get_posts, get_post

app = Flask(__name__)
app.secret_key = "..."
users = [["rick astley","123"]]


@app.route('/',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_login(username)

        if user and password==user[2]:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for("home",username=username))
        else:
            error = "Username or password is incorrect"

    return render_template('login.html',error=error)


@app.route('/home')
def home():

    return render_template('home.html',posts=get_posts())


@app.route('/profile',methods=['GET','POST'])
def profile():
    if not session.get('username'):
        return redirect(url_for('login'))
    user = get_profile(username=session['username'])
    posts = get_post(user_id=session['user_id'])

    return render_template('profile.html',email=user[4],username=user[1],id=user[0],age=user[2],name=user[3],password=user[5],posts=posts)


@app.route('/post',methods=['GET','POST'])
def new_post():
    error = ''
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session['user_id']
        if title:
            make_post(title,content,user_id)
        else:
            error = 'Title cannot be blank'

    return render_template('post.html', error=error)


@app.route('/register',methods=['GET','POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if username in users:
            error = "This username is already taken"
        else:
            create_user(username,password,email)
            session['user_id'] = create_user(username,password,email)
            return redirect(url_for("home"))

    return render_template('register.html',error=error)


app.run(debug=True)
