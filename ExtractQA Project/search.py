"""
Search the input given by user on internet using Google Search API
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse


class SearchQues:

    @staticmethod
    def GetLinksForQuora(ques):
        try:
            query = urllib.parse.quote(ques)
            search = "https://www.google.com/search?q=" + query + "quora"

            page = requests.get(search)

            if page.status_code == 200:
                content = BeautifulSoup(page.content, "html.parser")

                links = []
                for url in content.find_all('a', href=True):
                    if url['href'].startswith("/url?q=https://www.quora.com"):
                        link = url['href']
                        link = link[link.find('https://'):]
                        link = link[:link.find('&sa=')]
                        links.append(link)
                return links

            else:
                print("Cannot connect to website due to " + str(page.status_code) + " error from Google Search")
                exit(-1)
        except Exception as error:
            print(error)
            print("(Google Search)")
            exit(-1)

    @staticmethod
    def GetLinksForWiki(ques):
        try:
            query = urllib.parse.quote(ques)
            search = "https://www.google.com/search?q=" + query + " wikipedia"

            page = requests.get(search)

            if page.status_code == 200:
                content = BeautifulSoup(page.content, "html.parser")

                temp = content.findAll('cite')
                links = [link.text for link in temp]
                temp = []
                for link in links:
                    if link.startswith("https://en.wikipedia.org/"):
                        temp.append(link)
                return temp

            else:
                print("Cannot connect to website due to " + str(page.status_code) + " error from Google Search")
                exit(-1)
        except Exception as error:
            print(error)
            print("(Google Search)")
            exit(-1)
