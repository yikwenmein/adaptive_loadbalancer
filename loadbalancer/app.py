from flask import Flask, request
import sys
import os
import socket,requests,random
count =0
check =0
load1 =0
load2 =0
BACKENDS = ["20.107.205.190:8080","52.169.218.119:8080"]
app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def hello():
    global load1,load2
    global count
    global check
    if request.method =="GET":
        if load1 < 50 and load2 < 50:
            print("load1:",load1,flush =True)
            print("load2:",load2,flush=True)
            response = requests.get("http://{}".format(BACKENDS[count]))
            count = (count+1)%2
            return response.content, response.status_code
        if load1 > 50 or load2 > 50:
            print("load1:",load1,flush =True)
            print("load2:",load2,flush=True)
            if load1<load2:
                dif = round(load2-load1)
                ch1 = random.choices(BACKENDS,weights=(50+dif, 50-dif))
                response = requests.get("http://{}".format(ch1.pop()))
                return response.content, response.status_code
            if load2<load1:
                diff = round(load1-load2)
                ch2 = random.choices(BACKENDS,weights=(50-diff, 50+diff))
                response = requests.get("http://{}".format(ch2.pop()))
                return response.content, response.status_code
               

    if request.method =="POST":
         if request.form['load'] =='one':
             load1 = float(request.form['foo'])
             print("updated load1",load1,flush=True)
         elif request.form['load'] =='two':
             load2 = float(request.form['foo'])
             print("updated load2:",load2,flush=True)
         return 'Received !

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)

