import os

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.moment import Moment
from flask.ext.script import Manager, Shell
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form

from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import Required

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjdskfr4k353fj943jf34jrkscf9r384'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username


class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/', methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)


# @app.route('/')
# def index():
# 	# REDIRECTS TO DIFFERENT PAGE
# 	return redirect('http://github.com')

# @app.route('/browser')
# def browser():
# 	# REQUEST BROWSER INFO
# 	user_agent = request.headers.get('User-Agent')
# 	return '<p>Your browser is %s</p>' % user_agent

# @app.route('/cookie')
# def cookie():
# 	# RESPONSE WITH COOKIE
# 	response = make_response('<h1>This document carries a cookie!</h1>')
# 	response.set_cookie('answer', '42')
# 	return response

# @app.route('/user/<name>')
# def user(name):
# 	return '<h1>Hello, %s</h1>' % name

# @app.route('/user/<id>')
# def get_user(id):
# 	user = load_user(id)
# 	if not user:
# 		abort(404)
# 	return '<h1>Hello, %s</h1>' % user.name


if __name__ == '__main__':
	manager.run()