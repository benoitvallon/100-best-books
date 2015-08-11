from flask import Flask, render_template
import wikipedia
from bs4 import BeautifulSoup

app = Flask(__name__)

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
