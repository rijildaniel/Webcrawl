"""
To Create a localserver using a flask on port 3000
"""

from flask import Flask, render_template, request  # to create a localserver
from search import SearchQues  # search a query over internet get links of community site for scraping
from webcrawl import WebscrapForQuora  # Scrape the content from quora site
import pymysql  # to connect to database and perform various operation
import multiprocessing
from WikipediaCrawler import WebscrapForWikipedia


def CheckForLinks(linksS, listOfQids):
    con = pymysql.connect(host='localhost', user='root', password='', db='Extract_QA')
    handle = con.cursor()
    query = "SELECT Links FROM Links;"
    handle.execute(query)
    ls = handle.fetchall()
    links = []
    for l1 in ls:
        links.append(l1[0])
    linksCopy = linksS.copy()
    for link in linksCopy:
        if links.count(link) >= 0:
            query = "SELECT QID FROM Links WHERE Links=\'{0}\';".format(str(link))
            handle.execute(query)
            id = handle.fetchone()
            if id is not None:
                listOfQids.append(id[0])
                linksS.remove(link)


def CreateProcess1(links):
    processes = [multiprocessing.Process(target=GetAnswersFromQuora, args=(link,)) for link in links]
    for p in processes:
        p.start()
    for p in processes:
        p.join()


def CreateProcess2(links):
    processes = [multiprocessing.Process(target=GetAnswersFromWiki, args=(link,)) for link in links]
    for p in processes:
        p.start()
    for p in processes:
        p.join()


class Database:
    @staticmethod
    def FetchAnswers(qids):
        con = pymysql.connect(host='localhost', user='root', password='', db='Extract_QA')
        handle = con.cursor()
        data = []
        for i in qids:
            query = 'SELECT Answer FROM Answers WHERE Ans_id=' + str(i) + ';'
            handle.execute(query)
            data.append(handle.fetchall())
            con.commit()
        con.close()
        return data


app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/answers', methods=['POST'])
def GetResults():
    ques = request.form['ques']
    listOfQids = []
    Link = SearchQues()
    linksQuora = Link.GetLinksForQuora(ques)
    CheckForLinks(linksQuora, listOfQids)
    flag = 0
    con = None
    handle = None
    start = None
    end = None
    if not listOfQids:
        con = pymysql.connect(host='localhost', user='root', password='', db='Extract_QA')
        handle = con.cursor()
        query = "SELECT MAX(Q_ID) FROM question;"
        handle.execute(query)
        num = handle.fetchone()
        start = int(num[0])
        start += 1
        end = start + (len(linksQuora) - 1)
        for i in range(start, end + 1):
            listOfQids.append(i)
        flag = 1

    if len(linksQuora) != 0:
        CreateProcess1(linksQuora)

    linksWiki = Link.GetLinksForWiki(ques)
    CheckForLinks(linksWiki, listOfQids)
    if len(linksWiki) != 0:
        CreateProcess2(linksWiki)

    if flag == 1:
        end += len(linksWiki) - 1
        query = 'INSERT INTO answer_index(Question,Start_ID,End_ID) VALUES(\'' + ques + "'," + str(start) + "," + str(
            end) + ");"
        handle.execute(query)
        con.commit()

    db = Database()
    answers = db.FetchAnswers(listOfQids)
    ans = []
    for ans1 in answers:
        for ans2 in ans1:
            for ans3 in ans2:
                ans.append(ans3)

    return render_template('answers/answers.html', ques=ques, answers=ans)


def GetAnswersFromQuora(url):
    crawl = WebscrapForQuora(url)
    crawl.Get_ques_ans()


def GetAnswersFromWiki(url):
    crawl = WebscrapForWikipedia(url)
    crawl.Get_ques_ans()


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)




"""
  To run the File: Server will be created at http://localhost:3000
  Windows:-  python connect.py
  Linux:-    python3 connect.py
"""
