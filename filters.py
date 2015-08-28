from operator import itemgetter

def orderByMost(filterString, books):
  isolatedElements = {}
  for book in books:
    if book[filterString] in isolatedElements.keys():
      isolatedElements[book[filterString]] += 1
    else:
      isolatedElements[book[filterString]] = 1

  # clean unknow elements
  unknowElementString = "Unknown"
  if unknowElementString in isolatedElements:
    del isolatedElements[unknowElementString]

  elements = []
  for key, value in isolatedElements.items():
    element = { "name": key, "numberOfBooks": value }
    elements.append(element)

  elements = sorted(elements, key=itemgetter('numberOfBooks'), reverse=True)

  return elements
