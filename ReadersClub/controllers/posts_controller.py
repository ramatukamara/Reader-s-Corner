from flask import render_template, session, redirect, request
from ReadersClub import app
from ReadersClub.models.posts_model import Post

# ======================================== Fetch all posts from the database

@app.route('/homepage')
def homepage():
    if 'uid' not in session:
        return redirect('/')
    
    posts = Post.get_all()
    return render_template('homepage.html', posts=posts)

# ======================================== Fetch one post to view

@app.route('/post/<int:id>')
def view_post(id):
    if 'uid' not in session:
        return redirect('/')
    
    post = Post.get_by_id(id)
    return render_template('profile.html', post=post)

# ====================================== Create a new post

@app.route('/new_post')
def new_post():
    if 'uid' not in session:
        return redirect('/login')
    return render_template('create_post.html')

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'uid' not in session:
        return redirect('/login')
    
    data = {
        'comment': request.form['comment'],
        'book_club': request.form['book_club'],
        'date_of_post' : request.form['date_of_post'],
        'user_id': session['uid']
    }
    Post.create(data)
    return redirect('/homepage')

# ===================================Routes for editing

@app.route('/post/<int:id>/edit')
def edit_post(id):
    post = Post.get_by_id(id)
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:id>/update', methods=['POST'])
def update_post(id):

    data = {
        'id': id,
        'comment': request.form['comment'],
        'book_club': request.form['book_club']
    }
    Post.update(data)
    return redirect('/homepage')

# ================================== Route for deleting 

@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    Post.delete(id)
    return redirect('/homepage')