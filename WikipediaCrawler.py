"""
*********** Scrape the contents from Wikipedia site ******************
"""

import requests
from bs4 import BeautifulSoup  # BeautifulSoup class for extracting contents from websites

from Database import Database


class WebscrapForWikipedia:  # To extract contents from quora site

    def __init__(self, link):  # Initialize the object with attribute url from where contents
        self.url = link  # will be extracted

    def Get_ques_ans(self):
        try:
            response = requests.get(self.url)  # Send request to site for getting source code of their webpage

            if response.status_code == 200:  # To check if it has successfully recieved the source

                # code or particular webpage is present
                content = BeautifulSoup(response.content, "html.parser")
                title = content.find("h1", class_="firstHeading")

                # ...................... Answers extraction....................
                title = title.get_text()
                answers = []
                content = content.find("div", class_="mw-parser-output")
                for temp in content.find_all("p"):  # extract the contents
                    temp = temp.get_text()
                    answers.append(temp)

                heading = [title]
                db = Database()
                db.StoreToDatabase(heading, answers, self.url, 2)

            else:
                print("Cannot connect to website due to " + str(response.status_code) + " error from Wikipedia Site")
                exit(-1)


        except Exception as error:
            print(error)
            print("Something went wrong try again later (Wikipedia site)")
            exit(-1)
