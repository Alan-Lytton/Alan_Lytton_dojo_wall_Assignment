from flask import render_template, redirect, session, request
from flask_app.models.post import Post  #change this import line based on your extra .py file for generating OOP instances
from flask_app.models.comment import Comment
from flask_app import app



@app.route("/wall")     # lines 6 through 11 can be changed depending on what we need server.py to do.
def r_posts():
    if 'user_id' not in session:
        return redirect('/')
    posts = Post.get_all_posts_with_user()
    return render_template("wall.html", posts= posts)

@app.route('/destroy_session')
def destroy_session():
    session.clear()
    return redirect('/')

@app.route('/create_post', methods = ['POST'])
def f_create_posts():
    if 'user_id' not in session:
        return redirect('/')
    if not Post.validate_post(request.form):
        return redirect('/wall')
    else:
        Post.add_post(request.form)
    return redirect('/wall')

@app.route('/delete/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':id
    }
    Post.delete_post(data)
    return redirect('/wall')