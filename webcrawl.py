"""
********* Scrape the contents the from the Quora site *************
"""


import requests
from bs4 import BeautifulSoup  # BeautifulSoup class for extracting contents from websites
from Database import Database


class WebscrapForQuora:  # To extract contents from quora site

        def __init__(self, link):  # Initialize the object with attribute url from where contents
            self.url = link  # will be extracted

        def Get_ques_ans(self):
            try:
                page = requests.get(self.url)  # Send request to site for getting source code of their webpage

                if page.status_code == 200:  # To check if it has successfully recieved the source
                    # code or particular webpage is present
                    content = BeautifulSoup(page.content, "html.parser")
                    # Question extraction...................................

                    question = []
                    for temp in content.find_all("div", class_="question_text_edit"):
                        temp = temp.get_text()
                        temp = str(temp)
                        temp = temp.lower()
                        question.append(temp)
                    # Answers extraction......................................

                    answers = []
                    for temp in content("span", class_="rendered_qtext"):  # extract the contents
                        temp = temp.get_text()
                        answers.append(temp)

                    for temp in content.find_all("div", class_="ui_qtext_expanded"):
                        temp = temp.get_text()
                        answers.append(temp)

                    db = Database()
                    db.StoreToDatabase(question, answers, self.url, 1)

                else:
                    print("Cannot connect to website due to " + str(page.status_code) + " error from Quora Site")
                    exit(-1)


            except Exception as error:
                print(error)
                print("Something went wrong try again later (Quora Site)")
                exit(-1)
