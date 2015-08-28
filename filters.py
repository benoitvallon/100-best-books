from operator import itemgetter

def orderByMostAuthors(books):
  isolatedAuthors = {}
  for book in books:
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

  return authors

def orderByMostLanguages(books):
  isolatedLanguages = {}
  for book in books:
    if book['language'] in isolatedLanguages.keys():
      isolatedLanguages[book['language']] += 1
    else:
      isolatedLanguages[book['language']] = 1

  # clean unknow languages
  unknowLanguageString = "Unknown"
  if unknowLanguageString in isolatedLanguages:
    del isolatedLanguages[unknowLanguageString]

  languages = []
  for key, value in isolatedLanguages.items():
    language = { "name": key, "numberOfBooks": value }
    languages.append(language)

  languages = sorted(languages, key=itemgetter('numberOfBooks'), reverse=True)

  return languages
