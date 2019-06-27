"""
Database connectivity to perform various operation- Inserting records,Get the records,etc
"""

import pymysql


class Database:
    @staticmethod
    def StoreToDatabase(ques, ans, url, id):
        try:
            con = pymysql.connect(host='localhost', user='root', password='', db='Extract_QA')

            handle = con.cursor()
            for temp in ques:
                query = 'INSERT INTO Question(SiteID,Question) VALUES(' + str(id) + ',"' + str(temp) + '");'
                handle.execute(query)
                con.commit()
            for temp in ans:
                temp = str(temp)
                temp = temp.replace("\u2019", "")
                temp = temp.replace("\u201c", "")
                temp = temp.replace("\u201d", "")
                temp = temp.replace("\u2018", "")
                temp = temp.replace("\u2013", "")
                temp = temp.replace("\u2026", "")
                temp = temp.replace("\u2122", "")
                temp = temp.replace('"', "")
                check = temp.strip()
                if not check:
                    continue

                query = 'INSERT INTO answers(Ans_id,Answer) VALUES((SELECT MAX(Q_ID) FROM question),"' + temp + '");'
                handle.execute(query)
                con.commit()

            query = 'INSERT INTO links(QID,Links) VALUES((SELECT MAX(Q_ID) FROM question),"' + url + '");'
            handle.execute(query)

            con.commit()
            con.close()
        except Exception as error:
            print(error)
            print("Issue in Database operation- (Database.py)")

