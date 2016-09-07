from flask import Flask
from flask import abort
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request

from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager


app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

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