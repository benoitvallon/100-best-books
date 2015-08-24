from flask import Blueprint, render_template, flash, current_app
import wikipedia
import urllib2
import re
import json

from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

extractions_routes = Blueprint('extractions_routes', __name__)

@extractions_routes.route('/extract-from-csv')
def extractFromCsv():
  # Open/close a file
  fileOpen = open("books.csv", "r")
  fileData = fileOpen.readlines()
  fileOpen.close()

  books = []
  for line in fileData:
    line = line.split(';')
    book = {
      'title': line[0].decode('utf8'),
      'author': line[1].decode('utf8'),
      'link': '',
      'pages': int(line[6].decode('utf8')),
      'year': int(line[3].decode('utf8')),
      'country': line[4].decode('utf8'),
      'language': line[5].decode('utf8'),
      'imageLink': 'images/' + line[7].decode('utf8')
    }
    if line[7]:
      book['link'] = line[8].decode('utf8')

    books.append(book)

  flash('%d book(s) have been extracted from the .csv file' % len(books), 'success')

  formattedJson = json.dumps(books, sort_keys=True, indent=2, separators=(',', ': '))
  # Open/close a file
  fileOpen = open("books.json", "w")
  fileData = fileOpen.write(formattedJson)
  fileOpen.close()

  return render_template('list.html', books= books)


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
  isbndbXml = urllib2.urlopen("http://isbndb.com/api/v2/xml/" + current_app.config['ISBNDB_KEY'] + "/books?q=" + pageNameEncoded).read()

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

@extractions_routes.route('/extract-from-apis')
def extractFromApis():
  request = requestWikipedia("Bokklubben_World_Library")
  htmlPage = BeautifulSoup(request.html(), 'html.parser')
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

  flash('%d book(s) have been extracted from wikipedia and other APIs' % len(books))

  formattedJson = json.dumps(books, sort_keys=True, indent=2, separators=(',', ': '))
  # # Open/close a file
  # fileOpen = open("books.json", "w")
  # fileData = fileOpen.write(formattedJson)
  # fileOpen.close()

  return render_template('list.html', books= books)
