from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask.ext.assets import Environment, Bundle
import pudb
import urllib2
import json
from operator import itemgetter
from datetime import datetime, date, time, timedelta
from login import login_routes
from extractions import extractions_routes

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('HUNDREDBESTBOOKS_SETTINGS', silent=True)

app.register_blueprint(login_routes)
app.register_blueprint(extractions_routes)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('custom.scss', filters='scss', output='stylesheets.css')
assets.register('scss_all', scss)

js = Bundle('lib/jquery/dist/jquery.js', 'lib/bootstrap-sass/assets/javascripts/bootstrap.min.js', 'custom.js', filters='jsmin', output='javascripts.js')
assets.register('js_all', js)


@app.route('/', methods=['GET', 'POST'])
def home():
  home = True

  if request.method == 'GET':
    number_of_days_to_end = request.args.get('days')

    return render_template('home.html', home= home,
        number_of_days_to_end= number_of_days_to_end)
  else:
    # Open/close a file
    fileOpen = open("books.json", "r")
    fileData = fileOpen.read()
    fileOpen.close()

    books = json.loads(fileData)

    if not request.form['number-of-pages'].isdigit():
      flash('Please enter a real number ;)', 'danger')
      return redirect(url_for('home'))

    pages_read_per_day = int(request.form['number-of-pages'])

    total_number_of_pages = 0
    for book in books:
      total_number_of_pages = total_number_of_pages + int(book['pages'])

    number_of_days_to_end = int(total_number_of_pages / pages_read_per_day) + 1
    today = datetime.now()
    finished_date = today + timedelta(days=number_of_days_to_end)

    tweeter_message = urllib2.quote('It would take me ' + str(number_of_days_to_end) + ' days to read the 100 Best Books of all time. Wanna know how long it would take for you too!' .encode('UTF-8'))

    return render_template('home-result.html', home= home,
        pages_read_per_day= pages_read_per_day, tweeter_message= tweeter_message,
        number_of_days_to_end= number_of_days_to_end, finished_date= finished_date)

@app.route('/list')
def list():
  # Open/close a file
  fileOpen = open("books.json", "r")
  fileData = fileOpen.read()
  fileOpen.close()

  books = json.loads(fileData)

  isReversedOrder = False;
  orderBy = request.args.get('order')

  if orderBy:
    isReversedOrder = orderBy[0] == "-"
    if isReversedOrder:
      orderBy = orderBy[1:]

    books = sorted(books, key=itemgetter(orderBy), reverse=isReversedOrder)

  print(isReversedOrder)

  return render_template('list.html', books= books, isReversedOrder=isReversedOrder)

@app.route('/whatisit')
def whatisit():
  return render_template('whatisit.html')

@app.route('/funstats')
def funstats():

  # Open/close a file
  fileOpen = open("books.json", "r")
  fileData = fileOpen.read()
  fileOpen.close()

  books = json.loads(fileData)

  isolatedAuthors = {}
  for book in books:
    print(book['author'])
    if book['author'] in isolatedAuthors.keys():
      isolatedAuthors[book['author']] += 1
    else:
      isolatedAuthors[book['author']] = 1

  # clean unknow authors
  unknowAuthorString = "Unknown"
  if unknowAuthorString in isolatedAuthors:
    del isolatedAuthors[unknowAuthorString]

  authors = []
  for key, value in isolatedAuthors.items():
    author = { "name": key, "numberOfBooks": value }
    authors.append(author)

  authors = sorted(authors, key=itemgetter('numberOfBooks'), reverse=True)
  print authors

  return render_template('funstats.html', authors=authors)

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=True)
