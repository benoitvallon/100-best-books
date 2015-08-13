from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask.ext.assets import Environment, Bundle
import wikipedia
import urllib2
import pudb
import re
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.from_envvar('BOKKLUBBEN_SETTINGS', silent=True)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('custom.scss', filters='pyscss', output='stylesheets.css')
assets.register('scss_all', scss)

js = Bundle('jquery.js', 'bootstrap.min.js', 'custom.js', filters='jsmin', output='javascripts.js')
assets.register('js_all', js)

def requestWikipedia(page):
  return wikipedia.page(page)

def requestIsbndb(book):
  pageName = book['title']
  pageName = pageName.replace("_", " ")

  if book['author'] != 'Unknow':
    pageName = pageName + " " + book['author']
  print book
  print pageName
  pageNameEncoded = urllib2.quote(pageName.encode('UTF-8'))
  print 'Request for: ' + pageNameEncoded
  isbndbXml = urllib2.urlopen("http://isbndb.com/api/v2/xml/" + app.config['ISBNDB_KEY'] + "/books?q=" + pageNameEncoded).read()

  bestResult = getIsbndbBestResult(isbndbXml)


  book['description'] = bestResult.find('physical_description_text').text
  isbn10 = bestResult.find('isbn10').text
  book['imageLink'] = "http://covers.openlibrary.org/b/isbn/" + isbn10 + ".jpg"

  return book

def getIsbndbBestResult(isbndbXml):
  root = ET.fromstring(isbndbXml)
  results = root.findall('data')

  for result in results:
    image = urllib2.urlopen("http://covers.openlibrary.org/b/isbn/" + result.find('isbn10').text + ".jpg")
    print "http://covers.openlibrary.org/b/isbn/" + result.find('isbn10').text + ".jpg"

    responseHeaders = image.info()
    # is the result of the image load request a real image
    if "content-type" in responseHeaders.keys():
      print "image found"
      # is there a description in the book
      physicalDescriptionText = result.find('physical_description_text').text
      print physicalDescriptionText
      if physicalDescriptionText is not None and physicalDescriptionText != "":
        print "description found"
        reMatch = re.search(r'([0-9]*)\s*pages', physicalDescriptionText)
        if reMatch:
          print "pages in description: " + reMatch.group(1)
          return result
        else:
          print "no pages description"
        # return result
      else:
        print "no description"
    else:
      print "no image"

  print 'All results processed'

  return results[0]

@app.route('/extract')
def extract():
  bok = requestWikipedia("Bokklubben_World_Library")
  htmlPage = BeautifulSoup(bok.html(), 'html.parser')
  table = htmlPage.select(".wikitable")[0]
  lines = table.select('tr')

  # we remove the first line of the table as it is the legend
  lines = lines[1:3]
  books = []
  for line in lines:
    cells = line.select('td')
    title = cells[0].get_text().strip()
    link = "https://en.wikipedia.org" + cells[0].find('a').get('href').strip() if cells[0].find('a') else ''
    author = cells[1].find('a').get_text().strip() if cells[1].find('a') else ''
    book = dict(title=title, author=author, link=link)
    book = requestIsbndb(book)
    books.append(book)

  formattedJson = json.dumps(books, sort_keys=True, indent=2, separators=(',', ': '))
  # Open/close a file
  fileOpen = open("books.json", "w")
  fileData = fileOpen.write(formattedJson)
  fileOpen.close()

  return render_template('home.html', books= books)

@app.route('/')
def home():
  # Open/close a file
  fileOpen = open("books.json", "r")
  fileData = fileOpen.read()
  fileOpen.close()

  books = json.loads(fileData)

  return render_template('home.html', books= books)

@app.route('/admin', methods=['GET', 'POST'])
def login():
  error = None
  print 'start'
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You are logged in')
      return redirect(url_for('home'))
  print 'end'
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You are logged out')
  return redirect(url_for('home'))

if __name__ == '__main__':
  app.run(debug=True)
