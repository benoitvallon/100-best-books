from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
import wikipedia
from bs4 import BeautifulSoup

app = Flask(__name__)
assets = Environment(app)

# assets = flask.ext.assets.Environment()
assets.init_app(app)


assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('custom.scss', filters='pyscss', output='stylesheets.css')
assets.register('scss_all', scss)

js = Bundle('jquery.js', 'bootstrap.min.js', 'custom.js', filters='jsmin', output='javascripts.js')
assets.register('js_all', js)

@app.route('/')
def home():
  bok = wikipedia.page("Bokklubben_World_Library")
  htmlPage = BeautifulSoup(bok.html(), 'html.parser')
  table = htmlPage.select(".wikitable")[0]
  lines = table.select('tr')

  # we remove the first line of the table as it is the legend
  lines = lines[1:]
  titles = []
  for line in lines:
    cell = line.select('td')[0]
    titles.append(cell.get_text().strip())

  return render_template('home.html', titles= titles)

if __name__ == '__main__':
  app.run(debug=True)
