import urllib.parse
import re
import time
from dbConnetion import *
import io
import os
import sys
import urllib.parse
from selenium import webdriver
from flask_cors import CORS, cross_origin
from flask import Flask, request, send_file
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
#options.headless = True
options.headless = False

app = Flask(__name__)

cors = CORS(app)


@app.route('/staticF/<name>')
@cross_origin()
def pdfEm(name):
    result = send_file('static\\' + name)
    return result


# def chunks(l, n):
#     # Yield successive n-sized chunks from l
#     for i in range(0, len(l), n):
#         yield l[i:i + n]


# for x in chunks("ascasavasvasv",2):
#     print(x)

# google
googleD = webdriver.Chrome(options=options)
googleD.get(
    "https://translate.google.com/?hl=en&tab=rT1&sl=en&tl=fa&op=translate")
enTextBoxGoogle = googleD.find_element_by_css_selector('.er8xn')


@app.route('/translate/google', methods=['POST'])
@cross_origin()
def google():

    enTextBoxGoogle.send_keys(" ")

    enText = request.form.get('data')

    newenText = re.split("\.|\. ", enText)


    for count, value in enumerate(newenText):
        if (count % 2 != 0):
            newenText.insert(count, "\n-------------------\n")
   
    forPrint = "`"
    for x in newenText:
        forPrint += x
    forPrint += "`"


    googleD.execute_script(
        f"return document.querySelector('.er8xn').value={forPrint} ")

    enTextBoxGoogle.send_keys(" ")

    # for x in chunks(newenText,50):
    #     enTextBoxGoogle.send_keys(x)

    # enTextBoxGoogle.send_keys(newenText)

    
    elements = None


    if len(enText) >= 750:
        elements = WebDriverWait(googleD, 10000).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'span[jsname="W297wb"]'))
        )

        googleD.execute_script(
            "return document.querySelector('.er8xn').value=null ")

        temp11 = ''
        for x in elements:
            temp11 += x.get_attribute('innerHTML')


        temp = ''
        for x in re.split("---------", temp11):
            temp += x


        enTextBoxGoogle.send_keys(" ")

        return temp

    else:
        elements = WebDriverWait(googleD, 10000).until(
            EC.presence_of_all_elements_located(
                # انتخاب div هایی که ترججمه رو دارن
                (By.CSS_SELECTOR, 'div[jsname="FteS1d"]'))
                # (By.CSS_SELECTOR, 'div[jsname="coXp1b"]'))
        )

    enText = re.split("\.|\. ", enText)

    if len(enText[len(enText)-1]) <= 1:
        enText.pop()

    teran1 = []
    teran2 = []
    for count, value in enumerate(elements):
        if count % 2 == 0:
            teran1.append(value.get_attribute('innerHTML'))
        if count % 2 == 1:
            teran2.append(value.get_attribute('innerHTML'))

    newteran1 = []
    temppnewteran1 = ''
    for x in teran1:
        if x.find("------------") == -1:
            temppnewteran1 += x
        if x.find("------------") != -1:
            newteran1.append(temppnewteran1)
            temppnewteran1 = ''

    newteran2 = []
    temppnewteran2 = ''
    for x in teran2:
        if x.find("------------") == -1:
            temppnewteran2 += x
        if x.find("------------") != -1:
            newteran2.append(temppnewteran2)
            temppnewteran2 = ''

    str_temp = ""
    for count, value in enumerate(enText):
        str_temp += enText[count] + "\n" + str(
            int(count + 1)) + "-" + newteran1[count] + "\n" + str(
            int(count + 1)) + "-" + newteran2[count]
        # + "\n"

    googleD.execute_script(
        "return document.querySelector('.er8xn').value=null ")

    enTextBoxGoogle.send_keys(" ")

    return str_temp




# targoman
targomanD = webdriver.Chrome(options=options)
targomanD.get("https://targoman.ir/")
enTextBoxTargoman = targomanD.find_element_by_css_selector('.src .content')


@app.route('/translate/tarjome', methods=['POST'])
@cross_origin()
def tarjome():
    enText = request.form.get('data')

    enTextBoxTargoman.send_keys(enText)

    WebDriverWait(targomanD, 10000).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.tgt .content > span'))
    )

    test = targomanD.execute_script(
        "return document.querySelector('.tgt .content').textContent;")

    test = re.split("\.|\. ", test)

    temppp = ""
    for e in test:
        temppp += e  + "\n"

    clearr = WebDriverWait(targomanD, 10000).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.toolbar-button'))
    )

    clearr.click()

    return temppp


# mainF = webdriver.Chrome()
# mainF.get(
#     "file:///C:/Users/98/Desktop/project/python/PdfTranslate/index.html")



@app.route('/urlgoogleteanslate', methods=['POST'])
@cross_origin()
def url_google_teanslate():
    word = request.form.get('data')
    url = 'https://translate.google.com/?'
    params = {
        'hl': 'en',
        'tab': 'rT1',
        'sl': 'en',
        'tl': 'fa',
        'text': f'{word}',
        'op': 'translate'
    }
    return (url + urllib.parse.urlencode(params))



@app.route('/dictWord')
@cross_origin()
def dictWord():
    insert_word_from_csv_to_db()
    f = io.open("a.csv", mode="r", encoding="utf-8")

    words = f.read()

    modified_str = ''

    for char in range(0, len(words)):
        if(words[char] == '\n'):
            modified_str += ','
        else:
            modified_str += words[char]

    a = ""
    for count, value in enumerate(modified_str.split(",")):
        if count != 1:
            if len(value) >= 1:
                if count % 6 == 1:
                    a += value+"*%*"

    return a


@app.route('/wordsIKnow/read', methods=['POST'])
@cross_origin()
def read():
    word = request.form.get('data')
    return read_('en', word)






@app.route('/closeDrive')
@cross_origin()
def endddddd():
    googleD.quit()
    targomanD.quit()
    # mainF.quit()
    return "good by"
    sys.exit()





# @app.route('/wordsIKnow/update', methods=['POST'])
# @cross_origin()
# def update():
#     word = json.loads(request.form.get('data'))

#     # for item in word:
#     #     cca_retur = update_(word['index_'], item, word[item])
#     #     print("----------------------------")
#     #     print(item)
#     #     print(word[item])
#     #     print(cca_retur)
#     #     print("----------------------------")
#     #     if cca_retur != 'True':
#     #         return "erorr"

#     # print("----------------------------")
#     # print(word['index_'])
#     # print(read_('index_', word['index_']))
#     # print("----------------------------")

#     update_('410', 'description', 'asvasvasasvv')

#     return read_('index_', "410")

#     # return read_('index_', word['index_'])


# '''
# // "http://localhost:8000/wordsIKnow/readAll"
# // "http://localhost:8000/wordsIKnow/delete"
# // "http://localhost:8000/wordsIKnow/update"
# // "http://localhost:8000/wordsIKnow/create"
# '''





### to run this app
# set FLASK_APP=app.py
# set FLASK_RUN_PORT=8000
# flask run
