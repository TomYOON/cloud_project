from flask import Flask, render_template, request
from DataProcess import ApiCaller, RegCodeLDataProcessor
import json

app = Flask(__name__)
api = ApiCaller()
api.load_service_key("./serviceKey.txt")
rdp = RegCodeLDataProcessor()
rdp.read_file("dong_code.txt")

@app.route("/")
def getMain():
    return render_template("root.html")

@app.route("/selectSiDo",  methods=['GET', 'POST'])
def getSiDo():
    # print(request.form)
    sido = request.form["sido"]
    gu = request.form["gu"]
    start_date = int(request.form["start"].replace("-", ""))
    end_date = int(request.form["end"].replace("-", ""))

    if end_date < start_date: #start가 더 뒤의 날짜로 왔을 경우 스왑
        end_date, start_date = start_date, end_date
    date_list = [start_date]
    while start_date != end_date:
        start_date +=1
        if start_date % 100 == 13: #12월 넘어갔을 때
            start_date += 100 #년도 추가
            start_date -= 12
        date_list.append(start_date)
    searched_list = rdp.search(sido, gu)
    
    data_list = []
    count_dic = {"category":"per count"}
    line_data = []
    for date in date_list:
        for do_gu in searched_list: 
            called_data = api.call_all(int(do_gu.code), date)
            mapped_data, avg_apart, avg_dasaedae, avg_dagagu, avg_dandok = rdp.mapping_trade_data(called_data, do_gu)
            data_list += mapped_data
        line_data.append([str(date), avg_apart, avg_dasaedae, avg_dagagu, avg_dandok])
    # print(data_list)
    for data in data_list:
        if data.category not in count_dic:
            count_dic[data.category] = 1
        else:
            count_dic[data.category] += 1
    # print(line_data)
    return render_template("body.html", data_list=data_list, count_data=count_dic, line_data=line_data)

@app.route("/test")
def test():
    data = {'Task' : 'Hours per Day', 'Work' : 11, 'Eat' : 2, 'Commute' : 2, 'Watching TV' : 2, 'Sleeping' : 7}
    return render_template("graph.html",data=data)
if __name__ == '__main__':

	app.run(debug=True)