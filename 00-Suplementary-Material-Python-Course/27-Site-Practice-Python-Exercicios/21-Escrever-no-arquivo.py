# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/11/30/21-write-to-a-file.html

import sys
print(sys.version)
##########################################################################
# Take the code from the How To Decode A Website exercise
# (if you didn’t do it or just want to play with some different code,
# use the code from the solution), and instead of printing the results to a
# screen, write the results to a txt file.
# In your code, just make up a name for the file you are saving to.
#
# Extras:
#     Ask the user to specify the name of the output file that will be saved.

import requests
from bs4 import BeautifulSoup


def decodifica_web_page():

    url = "http://www.vanityfair.com/society/2014/06/monica-lewinsky-humiliation-culture"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    # print(soup.prettify())

    texto_body = soup.select("div.parbase.cn_text > div.body > p")

    nome = input("Qual será o nome do arquivo? ")
    with open(nome, "w") as f:
        for elemento in texto_body[7:]:
            f.write(elemento.text.replace("\n", " ").strip())


# Resposta

import requests
from bs4 import BeautifulSoup

def resposta():

    base_url = 'http://www.nytimes.com'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, features="lxml")

    filename = input("File to save to: ")

    with open(filename, 'w') as f:
      for story_heading in soup.find_all(class_="story-heading"):
          if story_heading.a:
              f.write(story_heading.a.text.replace("\n", " ").strip())
          else:
              f.write(story_heading.contents[0].strip())

def main():
    decodifica_web_page()
    resposta()

if __name__ == '__main__':
    main()
