from flask import Blueprint, render_template
from flask_login import current_user
from .models import Post

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", user=current_user, posts=posts)
