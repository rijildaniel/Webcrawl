# Webcrawl
Extracting contents

This project is about extracting contents from the commnunity sites and bring the contents into our system and stored them.
The full project is done in python using Flask framework for creating server and Beautiful Soup module in python for scraping contents from the web.

# Many other modules are used they are:
1) request - To establish connection to a website.
2) pymysql - to perform database operation.
3) multiprocessing - To enable multi-threading.
4) Flask
5) BeautifulSoup

# The flow of the project is as follows:
A user interface is provided to fire an query or question by the user, when query is fired the request goes to localserver created using flask framework.
The query is extracted and it is first google searched to get related links to query where we can find answer for the query. The links of Quora and Wikipedia is selected for extracting the contents. (search.py)
Firstly the contents from Quora links obtained from google search results is extratced using self desgined crawler and then from Wikipeda if available.
To execute the process of extracting contents faster,the program extracts the contents from different links simultaneously using multi threading where each thread handles each link. (To reduce waiting period.)
After extracting contents, the contents are stored in database in an MYSQL Database where questions and answers are stored.
Finally, the extracted contents are displayed to user .


# How to setup the project?
Directly download the zip folder and import it to Pycharm IDE

1) Install MYSQL in your computer.
2) Change if required in connect method of Database.py
3) Run the connect.py file (A localserver will be created at port no: 3000)
4) Open the link in your browser: http://localhost:3000
4) Ask a question.
5) See the result.
