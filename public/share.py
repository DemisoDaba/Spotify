from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

posts = Blueprint("posts", __name__)


@posts.route("/post", methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form.get('title')
        article = request.form.get('article')

        if not article:
            flash('Post cannot be empty', category='error')
        elif not title:
            flash('Title cannot be empty', category='error')
        else:
            post = Post(title=title, article=article, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("editor.html", user=current_user)


@posts.route("/blog/<id>")
@login_required
def blog(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post Does Not Exist", category='error')
        return redirect(url_for('views.home'))
    comments = Comment.query.filter_by(post_id=id).all()
    return render_template("blog.html", user=current_user, post=post, comment=comments)
    

@posts.route("/delete/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post Does Not Exist", category='error')
    else:
        Comment.query.filter_by(post_id=id).delete()
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted!', category='success')
        return redirect(url_for('views.home'))
    return render_template("index.html", user=current_user)


@posts.route("/posts/<username>")
@login_required
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User Not Found!", category='error')
        return redirect(url_for('views.home'))
    user_posts = user.posts
    return render_template("posts.html", user=current_user, posts=user_posts, username=username)


@posts.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def comments(post_id):
    text = request.form.get('text')
    if not text:
        flash('Empty Comment!', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if not post:
            flash('Post does not exist', category='error')
        else:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
    return redirect(url_for('posts.blog', id=post_id))


@posts.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash("Comment Don\'t Exist", category='error')
    else:
        post_id = comment.post_id
        db.session.delete(comment)
        db.session.commit()
        flash("Comment Deleted", category='success')
    return redirect(url_for('posts.blog', id=post_id))