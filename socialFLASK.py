from flask import Flask, render_template, jsonify, request
import numpy as np
import pandas as  pd
import sklearn 
import json
import pickle as p 
import requests 


app  = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/socialprediction", methods = ['POST'])
def predictheart():
    data = request.get_json()
    prediction = np.array2string(model.predict(data))
    return jsonify(prediction)

@app.route("/socialbuy", methods = ['POST'])
def heartcondition():
    url = "http://localhost:5000/socialprediction"


    User_id = request.form["User_id"]
    Gender = request.form["Gender"]
    Age  = int(request.form["Age"])
    EstimatedSalary = float(request.form["EstimatedSalary"])

    
    data = {'Gender':[Gender],'Age':[Age],'EstimatedSalary':[EstimatedSalary]}

    data = pd.DataFrame(data)
    
    social = pd.read_csv('Social_Network_Ads.csv')
    x = social.iloc[:,1:4]


    x = pd.concat([x,data],axis = 0)
    x = x.reset_index(drop = True) 
    for i in range(len(x["Gender"])):
        if x.iloc[i,0] == 'Male':
            x.iloc[i,0] = 1
        else:
            x.iloc[i,0] = 0 

    #scaling

    x_new = x
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    scale_col = ['Age','EstimatedSalary']
    x_new[scale_col] = scaler.fit_transform(x[scale_col]) 


    a = x_new.iloc[-1,:]
    new_data = []
     
    for i in range(len(a.index)):
        new_data.append(a[i])

    new_data = [new_data]
    j_data = json.dumps(new_data)

    headers = {'content-type':'application/json','Accept-Charset':'UTF-8'}
    r = requests.post(url, data = j_data, headers = headers)
    r1 = list(r.text)
    stat = ""

    if r1[2] == str(0):
        stat = "Ad will not be purchased"
    elif r1[2] == str(1):
        stat = "Ad will be purchased"
    else:
        stat = "Error"
        
    return render_template("result.html", result = stat)

if __name__ == '__main__':

    model_file='social.pickle'
    model=p.load(open(model_file,'rb'))
    app.run(debug = True, host = '0.0.0.0')

    