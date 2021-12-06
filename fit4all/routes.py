from flask import render_template, url_for, flash, redirect, request, abort
from fit4all import app, db, bcrypt
from fit4all.forms import RegistrationForm, LoginForm, PostForm
from fit4all.models import User, Post, Note
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(user_id=current_user.id).all()
        notes = Note.query.filter_by(note_user_id=current_user.id).all()
        return render_template('home.html', posts = posts, notes = notes)
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title = 'about')

@app.route("/error404")
def error404():
    return render_template('error404.html', title = 'error404')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, athlete = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title = 'New Post', form = form,legend = 'Create Post')


@app.route("/post/<post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post = post)

@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.athlete != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='edit Post', form=form, legend='edit Post')

@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.athlete != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/account/<int:user_id>")
@login_required
def account(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('account.html',  user = user)

@app.route("/account/<int:user_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:
        abort(403)
    posts = Post.query.filter_by(user_id=current_user.id).all()
    for post in posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('login'))


@app.route("/not/<note_id>")
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note = note)


@app.route("/note/new", methods=['GET', 'POST'])
@login_required
def new_note():
    form = PostForm()
    if form.validate_on_submit():
        note = Note(content = form.content.data, note_user_id = current_user.id)
        db.session.add(note)
        db.session.commit()
        flash('note created', 'success')
        return redirect(url_for('home'))
    return render_template('create_note.html', title = 'New note', form = form,legend = 'Create note')