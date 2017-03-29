from app import db
import os
from flask import render_template,make_response,request,jsonify,url_for, flash,redirect
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
from flask_login import login_user, logout_user, UserMixin, LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from app.forms import MyForm, LoginForm, RegisterForm, CommentForm
from app.models import User, Post, Comment
from flask_wtf.csrf import CSRFProtect
from app import app
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
try:
    db.create_all()
except Exception as e:
    print(e)
else:
    """
    jwt authentication
    """
    class Info(object):
        def __init__(self, id, username, password):
            self.id = id
            self.username = username
            self.password = password

        def __str__(self):
            return "User(id='%s')" % self.id

    users = [
        Info(1, 'user1', 'abcxyz'),
        Info(2, 'user2', 'abcxyz'),
    ]

    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}

    def authenticate(username, password):
        user = username_table.get(username, None)
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            return (user)

    def identity(payload):
        user_id = payload['identity']
        return userid_table.get(user_id, None)

    app.config['SECRET_KEY'] = 'super-secret'
    jwt = JWT(app, authenticate, identity)


    """
    class based views
    """
    class HelloWorld(Resource):
        decorators = [jwt_required()]
        def get(self):
            queryset = models.Table3.query.all()
            return make_response(render_template('base.html', details = queryset),200)

    	
    api.add_resource(HelloWorld, '/hello')

    """
    method based views

    """
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/posts',methods=['GET','POST'])
    @login_required
    def posts():
        form = MyForm()
        data = request.data
        if request.method == 'POST':
            post = Post(title=form.title.data,
                        author=form.author.data,
                        content=form.content.data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts'))
        else:
            posts = Post.query.all()
            return render_template('post_list.html', posts=posts)

    @app.route('/post/<post_id>')
    def show_post(post_id):
        post = Post.query.get(post_id)
        comment_form = CommentForm()
        return render_template('show_post.html', form=comment_form, post=post)


    @app.route('/upload', methods=['GET', 'POST'])
    @login_required

    def upload_image():
        if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.picture = filename
            db.session.add(current_user)
            db.session.commit()

            flash('File Uploaded successfully')
            return redirect(url_for('posts'))
        else:
            return render_template('upload.html')

    @app.route('/post/new', methods=['POST','GET'])
    def new_post():
        form = MyForm()
        return render_template('post_form.html', form=form, url="/posts")


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/post/<post_id>/edit', methods=['GET'])
    @login_required
    def edit_post(post_id):
        post = Post.query.get(post_id)
        form = MyForm(obj=post)
        return render_template('post_form.html', form=form, url="/post/" + post_id + "/update")

    @app.route('/post/<post_id>/update', methods=['POST'])
    @login_required
    def update_post(post_id):

        post = Post.query.get(post_id)
        form = MyForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.author = form.author.data
            post.content = form.content.data
            post.user_id = current_user.id
            db.session.add(post)
            db.session.commit()
            flash('Post is updated!')
            return redirect(url_for('posts'))
        else:
            return redirect(url_for('posts'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        login_form = LoginForm()
        if request.method == 'GET':
            return render_template('login.html', form=login_form)
        if login_form.validate_on_submit():
            reg_user = User.query.filter_by(email=login_form.email.data,
                                            password=login_form.password.data).first()
            if reg_user is None:
                flash('Username or password is Invalid', 'error')
                return redirect(url_for('login'))
            login_user(reg_user)
            flash('Logged in successfully')
            return redirect(url_for('posts'))

    @app.route('/post/<post_id>/delete')
    @login_required
    def delete_post(post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post has been delete successfully!!')
        return redirect(url_for('posts'))

    @app.route('/post/<post_id>/comment', methods=['POST'])
    def add_comment(post_id):
        post = Post.query.get(post_id)
        comment_form = CommentForm()
        if comment_form.validate_on_submit():
            comment = Comment(content=comment_form.content.data,
                              user_id=current_user.id,
                              post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            url = url_for('show_post', post_id=post.id)
            return redirect(url)


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        register_form = RegisterForm()
        if request.method == 'GET':
            return render_template('register.html', form=register_form)
        if register_form.validate_on_submit():
            register = User(email=register_form.email.data,
                            password=register_form.password.data)
            db.session.add(register)
            db.session.commit()
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('new_post'))

    @app.route('/test')
    def index():
        return render_template('test.html')

