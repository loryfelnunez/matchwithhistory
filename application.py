from flask import Flask, render_template, request

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

import pymysql.cursors


# Connect to the database
SQLALCHEMY_DATABASE_URI = 'wmtechmakers18.cqf2qq23tddm.us-east-1.rds.amazonaws.com'

conn = pymysql.connect(host=SQLALCHEMY_DATABASE_URI,
                             port=3306,
                             user='wmtechmakers18',
                             password='wmtechmakers18',
                             db='wmtechmakers18',
                             cursorclass=pymysql.cursors.DictCursor)


@application.route('/')
@application.route('/index')
@application.route('/resto', methods=['GET'])
def history():
    cursor = conn.cursor()
    cursor.execute ("""
                SELECT * FROM `scores_1`  
                """)
    response = cursor.fetchall()
    all_names = []
    for r in response:
        all_names.append(r['Name'])
        print (r)
    jsonresults = [{"name":n}for n in all_names]
    return render_template("history.html", output=jsonresults)

if __name__ == '__main__':
    application.run(host='0.0.0.0')

# cursor = conn.cursor()
# cursor.execute('SELECT * FROM `scores_1` ')
# data = cursor.fetchone()
# print (data)