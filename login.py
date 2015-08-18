from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/admin', methods=['GET', 'POST'])
def login():
  error = None

  if request.method == 'POST':
    if request.form['username'] != current_app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != current_app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You are logged in', 'success')
      return redirect(url_for('home'))

  return render_template('login.html', error=error)

@login_routes.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You are logged out', 'success')
  return redirect(url_for('home'))
