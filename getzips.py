
import requests
import sqlite3
from sqlite3 import Error
'''Documentation for url template 
https://developers.google.com/maps/documentation/geocoding/start'''

api_key = "AIzaSyAYJlZvWoBxEuFYcB_XiDdnHFPO3UEh0E4"
database = "../btplayersbyzip.db"
conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute("SELECT id, city || ' '|| location, zip FROM players") # where lat is null
rows = cur.fetchall()
# print(rows)

for row in rows:
    print(row)
    response_json = None
    # print(row)
    if row[2] != 'None' and len(str(row[2])) == 5:
        print('running query on zip')
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=".format(row[2]) + api_key
        response = requests.get(url)
        response_json = response.json()
        
        print(response_json['status'])
        if response_json['status'] =='OK':
            # print(response_json)
            if 'partial_match' not in response_json['results'][0].keys():
                print(row[2])
                print(response_json['results'][0]['geometry']['location']['lat'])
                newlat = response_json['results'][0]['geometry']['location']['lat']
                print(response_json['results'][0]['geometry']['location']['lng'])
                newlng = response_json['results'][0]['geometry']['location']['lng']
                query = "UPDATE players SET lat = '{}', lng = '{}' where id = {}".format(newlat,newlng,row[0])
                print(query)
                cur.execute(query)
                print("lastrowid " + str(cur.lastrowid))
                conn.commit()
            
            else:
                print('partial match wtf')
                print(response_json)
    elif row[1] != 'None':
        print('running query on city and place')
        print(row[1])
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=".format(row[1]) + api_key
        response = requests.get(url)
        response_json = response.json()
        if response_json['status'] =='OK':
            if 'partial_match' not in response_json['results'][0].keys():
                print(response_json['results'][0]['geometry']['location']['lat'])
                newlat = response_json['results'][0]['geometry']['location']['lat']
                print(response_json['results'][0]['geometry']['location']['lng'])
                newlng = response_json['results'][0]['geometry']['location']['lng']
                query = "UPDATE players SET lat = '{}', lng = '{}' where id = {}".format(newlat,newlng,row[0])
                print(query)
                cur.execute(query)
                print("lastrowid " + str(cur.lastrowid))
                conn.commit()

conn.commit()
conn.close()
    