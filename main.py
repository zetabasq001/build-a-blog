from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://build-a-blog:3k9$JD%m@localhost:3306/build-a-blog"
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(228))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    @app.route("/")
    def index():
        return redirect("/blog")

    @app.route("/blog")
    def main_blog():
        blog_id = request.args.get("id")
        if blog_id:
            blog = Blog.query.get(blog_id)
            return render_template("blogpage.html", blog_title=blog.title, 
                blog_body=blog.body)
        
        blogs = Blog.query.all()
        return render_template("blog.html", tab_title="Build a Blog", blogs=blogs)

    @app.route("/newpost", methods = ["POST", "GET"])
    def new_post():
        if request.method == "POST":
            title_error = ""
            body_error = ""

            blog_title = request.form["blog_title"]
            blog_body = request.form["blog_body"]

            if blog_title == "":
                title_error = "Please fill in the title"
            if blog_body == "":
                body_error = "Please fill in the body"

            if title_error or body_error:
                return render_template("newpost.html", title_error=title_error,
                    body_error=body_error, blog_title=blog_title, blog_body=blog_body)

            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            return redirect("/blog?id={0}".format(new_blog.id))
        else:
            return render_template("newpost.html", tab_title="Add a Blog Entry")
  
if __name__ == '__main__':
    app.run()