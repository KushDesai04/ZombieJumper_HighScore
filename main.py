from flask import Flask, request
import sqlite3
from config import Config
import datetime

app = Flask('app')
app.config.from_object(Config)


## Connect to DATABASE ##
def connect(q, val=tuple(''), single=False):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    if val:
        cur.execute(q, val)
    else:
        cur.execute(q)
    result = cur.fetchone() if single else cur.fetchall()
    conn.close()
    return result


## Insert into DATABASE ##
def insert(val):
  conn = sqlite3.connect(app.config['DATABASE'])
  cur = conn.cursor()
  cur.execute("INSERT INTO Score (name,time,kills) VALUES(?,?,?)", val)
  conn.commit()
  conn.close()


## Show top 25 scores ##
@app.route('/', methods = ["GET", "POST"])
def home():
  scores = connect("SELECT name,time FROM Score ORDER BY time desc LIMIT 25")

  string = ""
  for i in scores:
    string += (i[0] + " - " + i[1] + "\n")
  print(string)
  return string


## Show top 25 kills ##
@app.route('/kills', methods = ["GET", "POST"])
def kills():
  kills = connect("SELECT name,kills FROM Score ORDER BY kills desc LIMIT 25")  
  print("KIllSS", kills)
  string = ""
  for i in kills:
    string += (i[0] + " - " + str(i[1]) + "\n")
  return string


## Add high scores ##
@app.route('/submit/<data>', methods = ["GET", "POST"])
def sumbit(data):
  player_time = ""
  name = ""
  kills = ""
  key = ""
  if request.method == "POST":
    print("POST REQUEST RECIEVED")
    name = request.form["username"]
    player_time = request.form["score"]
    kills = request.form["kills"]
    key = request.form["key"]



    print(name, player_time, kills)

    #Convert time to readable format
    player_time = int(player_time)
    player_time = str(datetime.timedelta(seconds = player_time))[2:]
    print(type(kills))
    #Insert into database

    if key == app.config["SECRETKEY"]:
      insert((name,player_time,kills))

    all = connect("SELECT * FROM Score")
    print(all)
  return str(data)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=8080, host='0.0.0.0')