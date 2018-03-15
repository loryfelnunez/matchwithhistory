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
cursor = conn.cursor()

@application.route('/')
@application.route('/index')
@application.route('/history', methods=['GET'])
def history():
    cursor.execute ("""
                SELECT distinct Main_Name FROM `scores_3` order by Main_Name 
                """)
    response = cursor.fetchall()
    all_names = []
    for r in response:
        all_names.append(r['Main_Name'])
        print (r)
    jsonresults = [{"name":n}for n in all_names]

    cursor.execute("""
                    SELECT distinct Main_Name FROM `scores_2` order by Main_Name 
                    """)
    response2 = cursor.fetchall()
    all_names2 = []
    for r in response2:
        all_names2.append(r['Main_Name'])
        print(r)
    jsonresults2 = [{"name": n} for n in all_names2]

    return render_template("history.html", output=jsonresults, outputv2=jsonresults2)


@application.route("/history_post", methods=['POST'])
def history_post():
    main_name = request.form["Main_Name"]
    print('here -----', main_name)
    sql = "SELECT Name, Score, URL  \
           FROM `scores_3` \
           WHERE Main_Name = \"" + main_name + "\"  \
           AND Name != \"" + main_name + "\"  \
           ORDER BY score DESC"
    cursor.execute (sql)
    response = cursor.fetchall()
    print (response)

    results = []
    for r in response:
        match_result = {}
        match_result['Name'] = r['Name']
        match_result['URL'] = r['URL']
        match_result['Score'] = r['Score']
        results.append(match_result)

    jsonresponse = {}
    jsonresponse['main_name'] = main_name
    jsonresponse['matches'] = results
    return render_template("history_post.html", output=jsonresponse)

@application.route("/history_post_v2", methods=['POST'])
def history_post_v2():
    main_name = request.form["Main_Name"]
    print('here -----', main_name)
    sql = "SELECT Name, Score, URL  \
           FROM `scores_2` \
           WHERE Main_Name = \"" + main_name + "\"  \
           AND Name != \"" + main_name + "\"  \
           ORDER BY score DESC"
    cursor.execute (sql)
    response = cursor.fetchall()
    print (response)

    results = []
    for r in response:
        match_result = {}
        match_result['Name'] = r['Name']
        match_result['URL'] = r['URL']
        match_result['Score'] = r['Score']
        results.append(match_result)

    jsonresponse = {}
    jsonresponse['main_name'] = main_name
    jsonresponse['matches'] = results
    return render_template("history_post.html", output=jsonresponse)


if __name__ == '__main__':
    application.run(host='0.0.0.0')

# cursor = conn.cursor()
# cursor.execute('SELECT * FROM `scores_1` ')
# data = cursor.fetchone()
# print (data)