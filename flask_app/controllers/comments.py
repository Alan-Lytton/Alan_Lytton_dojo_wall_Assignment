from flask import redirect, request, session
from flask_app.models.comment import Comment  #change this import line based on your extra .py file for generating OOP instances
from flask_app import app


@app.route('/add/comment', methods = ['POST'])
def f_add_comment():
    if 'user_id' not in session:
        return redirect('/')
    if not Comment.validate_comment(request.form):
        return redirect('/wall')
    else:
        Comment.add_comment(request.form)
    return redirect('/wall')