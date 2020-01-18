import requests,webbrowser
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect
from selenium import webdriver
#import urllib.request


app = Flask(__name__)
bar=''

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def foo():
    bar = request.form['vehnum']
    r = requests.post("http://www.rtovehicleinformation.com/rto-vehicle-information-karnataka", data=dict(
        vehicle_shrt_name= bar
        ))
    if r.status_code == 500:
        return render_template('error.html')
    soup = BeautifulSoup(r.text, "html.parser")
    tabdata = soup.find_all("td")[3]
    vehicle_name = tabdata.text.split('/')[1]
    vehicle_name = vehicle_name.split(' ')[0:3]
    query = ' '.join(map(str, vehicle_name))
    print(query)

    r1 = requests.get("https://www.google.com/search?q="+query)

    soup1 = BeautifulSoup(r1.text, 'html.parser')

    res = soup1.select('.kCrYT a')

    for i in res[1:2]:
        actual_link = i.get('href')
        #urllib.request.urlopen('https://google.com/'+actual_link)
        webbrowser.open('https://google.com/'+actual_link)
    return redirect('https://google.com/'+actual_link)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80)