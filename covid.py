import requests
import json
import os
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)
@app.route('/', methods=['POST'])

def MainFunction():
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    answer_from_bot = generating_answer(question_from_dailogflow_raw) 
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json'
    return r

def generating_answer(question_from_dailogflow_dict):
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"]  
    if intent_group_question_str == 'Covid':
        answer_str = Covid_Report()
    else: answer_str = 'กรุณาพิมพ์คำว่า covid หรือ โควิด เพื่อใช้งาน'
    answer_from_bot = {"fulfillmentText": answer_str}  
    answer_from_bot = json.dumps(answer_from_bot, indent=4)  
    return answer_from_bot

def add(word):
    url = 'https://covid19.ddc.moph.go.th/api/Cases/today-cases-all'
    covid = requests.get(url,)
    j = covid.json()
    convert = json.dumps(j)
    cut = convert.strip("[]")
    final = json.loads(cut)
    answer = (format(int(final[word]), ',d'))
    answerr = str(answer)
    return answerr

def Covid_Report():
    url = 'https://covid19.ddc.moph.go.th/api/Cases/today-cases-all'
    covid = requests.get(url,)
    j = covid.json()
    convert = json.dumps(j)
    cut = convert.strip("[]")
    final = json.loads(cut)
    update_date = 'อัพเดทล่าสุด : ' + str(final['update_date']) + '\n'
    new_case = 'จำนวนผู้ติดเชื้อรายใหม่ : ' + add('new_case') + '\n'
    total_case = 'จำนวนผู้ติดเชื้อทั้งหมด : ' + add('total_case') + '\n'
    new_death = 'จำนวนผู้เสียชีวิตรายใหม่ : ' + add('new_death') + '\n'
    total_death = 'จำนวนผู้เสียชีวิตทั้งหมด : ' + add('total_death') + '\n'
    new_recovered = 'จำนวนผู้ที่รักษาหายรายใหม่ : ' + add('new_recovered') + '\n'
    total_recovered = 'จำนวนผู้ที่รักษาหายทั้งหมด : ' + add('total_recovered')
    answer_function = 'รายงานโควิด \n' + update_date + new_case + total_case + new_death + total_death + new_recovered + total_recovered
    return answer_function

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)