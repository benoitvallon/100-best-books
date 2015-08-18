from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask.ext.assets import Environment, Bundle
import pudb
import json
from login import login_routes
from extractions import extractions_routes

app = Flask(__name__)
app.config.from_envvar('BOKKLUBBEN_SETTINGS', silent=True)

app.register_blueprint(login_routes)
app.register_blueprint(extractions_routes)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('custom.scss', filters='scss', output='stylesheets.css')
assets.register('scss_all', scss)

js = Bundle('lib/jquery/dist/jquery.js', 'lib/bootstrap-sass/assets/javascripts/bootstrap.min.js', 'custom.js', filters='jsmin', output='javascripts.js')
assets.register('js_all', js)


@app.route('/')
def home():
  # Open/close a file
  fileOpen = open("books.json", "r")
  fileData = fileOpen.read()
  fileOpen.close()

  books = json.loads(fileData)

  return render_template('home.html', books= books)

if __name__ == '__main__':
  app.run(debug=True)
