import os
from flask import render_template, url_for, flash, redirect, request, abort
from coffeeCalc import application, db, bcrypt
from coffeeCalc.forms import SignUpForm, LoginForm, PostForm, NoteForm, QuickCalcForm
from coffeeCalc.models import User, Post, Note, Country
from flask_login import login_user, current_user, logout_user, login_required

from coffeeCalc.calculator import *

# home page
@application.route("/")
def home():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(user_id=current_user.id).all()
        posts.reverse()
        notes = Note.query.filter_by(note_user_id=current_user.id).all()
        profile_image = url_for('static', filename='profile_images/' + current_user.image_file)
        return render_template('home.html', posts = posts, notes = notes, profile_image=profile_image)
    
    return sign_up()

# about page
@application.route("/about")
def about():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(note_user_id=current_user.id).all()
        return render_template('about.html', title = 'about', notes = notes)
    return render_template('about.html', title = 'about')

# new user page
@application.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign Up', form=form)

# login user page
@application.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            application.logger.info('Log in attempt for user:' + user.username)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# logout user page
@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# calculator page for guest users
@application.route("/calculation", methods=['GET', 'POST'])
def calculation():
    form = QuickCalcForm()
    form.start_country.choices = [(country.title) for country in Country.query.all()]
    if form.validate_on_submit():
        carbon_cost = co2_cost(form.weight.data, form.origin_to_port_distance.data, form.start_country.data, form.port_to_client_distance.data)
        print("This is the carbon cost: " + str(carbon_cost))
        return render_template('calculation.html', title = 'calculation', form = form, co2 = carbon_cost)    
    return render_template('calculation.html', title = 'calculation', form = form,  co2 = "0")

# new calculation for logged in users
@application.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    notes = Note.query.filter_by(note_user_id=current_user.id).all()
    form = PostForm()
    form.start_country.choices = [(country.title) for country in Country.query.all()]
    if form.validate_on_submit():
        print("test1")
        post = Post(title = form.title.data, start_country = form.start_country.data, origin_to_port_distance = str(form.origin_to_port_distance.data),end_location = form.end_location.data, port_to_client_distance=str(form.port_to_client_distance.data), weight = str(form.weight.data), carbon_cost = co2_cost(form.weight.data, form.origin_to_port_distance.data, form.start_country.data, form.port_to_client_distance.data), client = current_user)
        print("test2")
        db.session.add(post)
        db.session.commit()
        flash('Post created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title = 'New Post', form = form,legend = 'Create Post', notes = notes)

# view calculation for logged in users
@application.route("/post/<post_id>")
def post(post_id):
    notes = Note.query.filter_by(note_user_id=current_user.id).all()
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    profile_image = url_for('static', filename='profile_images/' + user.image_file)
    return render_template('post.html', title = post.title, post = post, notes = notes, profile_image=profile_image)

# edit calculation for logged in users
@application.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    notes = Note.query.filter_by(note_user_id=current_user.id).all()
    post = Post.query.get_or_404(post_id)
    if post.client != current_user:
        abort(403)
    form = PostForm()
    form.start_country.choices = [(country.title) for country in Country.query.all()]
    if form.validate_on_submit():
        post.title = form.title.data
        post.start_country = form.start_country.data
        post.origin_to_port_distance = str(form.origin_to_port_distance.data) 
        post.end_location = form.end_location.data
        post.port_to_client_distance = str(form.port_to_client_distance.data)
        post.weight = str(form.weight.data)
        post.carbon_cost = co2_cost(form.weight.data, form.origin_to_port_distance.data, form.start_country.data, form.port_to_client_distance.data)

        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.start_country.data = post.start_country
        form.origin_to_port_distance.data = float(post.origin_to_port_distance)
        form.end_location.data = post.end_location
        form.port_to_client_distance.data = float(post.port_to_client_distance)
        form.weight.data = float(post.weight)

    return render_template('create_post.html', title='edit Post', form=form, legend='edit Post', notes = notes)

# delete calculation for logged in users
@application.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.client != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# user account page
@application.route("/account/<int:user_id>")
@login_required
def account(user_id):
    notes = Note.query.filter_by(note_user_id=current_user.id).all()
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    posts.reverse()

    userPostsNum = len(posts)
    totalCarbon = 0

    if userPostsNum < 1:
        userPostsNum = 0
    else:
        i = 0
        while (i < userPostsNum):
            totalCarbon += co2_cost(posts[i].weight, posts[i].origin_to_port_distance, posts[i].start_country, posts[i].port_to_client_distance)
            i = i+1
        
    profile_image = url_for('static', filename='profile_images/' + user.image_file)
    return render_template('account.html',  user = user, notes = notes, profile_image = profile_image, userPostsnum = userPostsNum, posts = posts, totalCarbon = totalCarbon)

# delete user account
@application.route("/account/<int:user_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:
        abort(403)
    posts = Post.query.filter_by(user_id=current_user.id).all()
    notes= Note.query.filter_by(note_user_id=current_user.id).all()
    for post in posts:
        db.session.delete(post)
    for note in notes:
        db.session.delete(note)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('login'))

# view note for user account
@application.route("/note/<note_id>")
def note(note_id):
    notes = Note.query.filter_by(note_user_id=current_user.id).all()
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note = note, notes = notes)

# create new note for user account
@application.route("/note/new", methods=['GET', 'POST'])
@login_required
def new_note():
    notes = Note.query.filter_by(note_user_id=current_user.id).all()
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(content = form.content.data, note_user_id = current_user.id)
        db.session.add(note)
        db.session.commit()
        flash('note created', 'success')
        return redirect(url_for('home'))
    return render_template('create_note.html', title = 'New note', form = form, legend = 'Create note', notes = notes)

# edit note for user account
@application.route("/note/<int:note_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    notes = Note.query.filter_by(note_user_id=current_user.id).all()
    note = Note.query.get_or_404(note_id)
    if note.note_user_id != current_user.id:
        abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.content = form.content.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('note', note_id=note.id))
    elif request.method == 'GET':
        form.content.data = note.content
    return render_template('create_note.html', title='edit note', form=form, legend='edit note', notes = notes)

# delete note for user account
@application.route("/note/<int:note_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.note_user_id != current_user.id:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('home'))

# see other user accounts
@application.route("/exploreUsers")
def explore_users():
    if current_user.is_authenticated:
        users = User.query.all()
        users.reverse()
        notes = Note.query.filter_by(note_user_id=current_user.id).all()

        return render_template('explore_users.html', users = users, notes = notes)
    
    return sign_up()

# upload new user profile avatar
@application.route("/upload_file", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            image.save(os.path.join(application.config["IMAGE_UPLOADS"], image.filename))
            current_user.image_file=image.filename
            db.session.commit()

            print("Image saved")
            return render_template("home.html")
    return render_template("update_profile_pic.html")

# error 404 page
@application.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html', title = error)
