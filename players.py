from flask import Flask, render_template
import os
import sqlite3

# print(os.environ['googlemapsapikey'])

apikey = 'AIzaSyAYJlZvWoBxEuFYcB_XiDdnHFPO3UEh0E4'

app = Flask(__name__)

database = "../btplayersbyzip.db"
conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute("SELECT name, city, location, other, zip, CAST(lat AS REAL), CAST(lng AS REAL) FROM players WHERE lat is not null and lng is not null")

rows = cur.fetchall()
# print(rows)
points = []
for row in rows:
    # print(row)
    if row[3] != None:
        print(row[3])
        info = str(row[0]) + ' ' + str(row[3])
    else:
        info = row[0]
    
    # print(info)

    points.append([row[-1], row[-2], info])
# print(points)


@app.route('/')
def hello_world():
    print('ass')
    return render_template('map.html', points=points)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)