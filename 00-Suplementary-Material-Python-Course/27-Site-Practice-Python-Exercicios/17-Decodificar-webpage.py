# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/06/06/17-decode-a-web-page.html

import sys
print(sys.version)
##########################################################################
# Use the BeautifulSoup and requests Python packages to print out a list of all
# the article titles on the New York Times homepage.
import requests
url = "https://www.nytimes.com/"
pagina = requests.get(url)
# print(pagina.status_code)   # 200: significa "Pagina foi baixada com sucesso"
# print(pagina.content)
# pagina_html = pagina.text

import bs4
from bs4 import BeautifulSoup
# soup = BeautifulSoup(pagina.content, 'html.parser')
# print(soup.prettify())
# print(list(soup.children))
# html = list(soup.children)[2]
# print(html)
# body = list(html.children)[3]
# print(body)
# list(body.children)
# print(list(body.children))
# p = list(body.children)[1]
# print(p)

# soup = BeautifulSoup(pagina_html,'html.parser')
# titulo = soup.find('span').string
# print(titulo)

# Encontrando todas as instâncias de uma tag de uma vez
# soup.find_all('p')
# Para extrair o texto
# soup.find_all('p')[0].get_text()
# #####################################################################
# # Resposta
#
# # import the requests Python library for programmatically making HTTP requests
# # after installing it according to these instructions:
# # http://docs.python-requests.org/en/latest/user/install/#install
# import requests
#
# # import the BeautifulSoup Python library according to these instructions:
# # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
# # use this syntax as described on the documentation page:
# # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#making-the-soup
# from bs4 import BeautifulSoup
#
# # the URL of the NY Times website we want to parse
# base_url = 'http://www.nytimes.com'
#
# # the syntax (according to the documentation) for how to
# # "load" a webpage through Python
# r = requests.get(base_url)
#
# # how to decode the text of the HTML of the NY Times homepage
# # website. r comes from the requests request above
# soup = BeautifulSoup(r.text,'html.parser')
#
# # find and loop through all elements on the page with the
# # class name "story-heading"
# for story_heading in soup.find_all(class_="balancedHeadline"):
#     # for the story headings that are links, print out the text
#     # and format it nicely
#     # for the others, take the contents out and format it nicely
#     if story_heading.a:
#         print(story_heading.a.text.replace("\n", " ").strip())
#     else:
#         print(story_heading.contents[0].strip())
#
# #####################################################################

# OUtra Solucao
import requests
# import BeautifulSoup
from bs4 import BeautifulSoup

url = 'http://www.nytimes.com/'
ttl_lst = []

soup = bs4.BeautifulSoup(requests.get(url).text, features="lxml")
title = soup.findAll('h2', {'class': 'story-heading'})
for row in title:
     ttl_lst.append(row.text)

print(ttl_lst)
