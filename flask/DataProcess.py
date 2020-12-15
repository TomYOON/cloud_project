import requests 
import xmltodict, json
import urllib
import time

class ApiCaller:
    """
    for api call
    """
    
    def __init__(self):
        self.service_key = ""
    
    def load_service_key(self, key_path):
        f = open(key_path, 'r')
        self.service_key = f.readline()
        f.close()
    
    def call_apart_data(self, lawd_cd, deal_ymd):
        url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade"
        return self.call_api(url, lawd_cd, deal_ymd)
    
    def call_dasaedae_data(self, lawd_cd, deal_ymd):
        url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade"
        return self.call_api(url, lawd_cd, deal_ymd)
    
    def call_dagagu_data(self,lawd_cd, deal_ymd):
        url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcSHTrade"
        return self.call_api(url, lawd_cd, deal_ymd)
    
    def call_all(self, lawd_cd, deal_ymd):
        return self.call_apart_data(lawd_cd, deal_ymd) + self.call_dagagu_data(lawd_cd, deal_ymd) + self.call_dasaedae_data(lawd_cd, deal_ymd)
    
    def call_api(self, url, lawd_cd, deal_ymd):
        if type(deal_ymd) == str:
            deal_ymd = int(deal_ymd)
        params = {'serviceKey': self.service_key,
                  'LAWD_CD': lawd_cd,
                  "DEAL_YMD": deal_ymd
                 }
        request_url = self.create_request_url(url, params)
        res = requests.get(request_url)
        temp = xmltodict.parse(res.text)
        json_res = json.dumps(temp, ensure_ascii = False)
        json_res = json.loads(json_res) #str to dict
        time.sleep(0.002)
        # print(json_res)
        if json_res["response"]["body"]["items"] == None:
            return [dict()]
        return json_res["response"]["body"]["items"]["item"]    
    
    def create_request_url(self, end_point, params):
        items = list(params.items())
        param_str = ""
        for key, value in items:
            param_str += "{}={}&".format(key,value)
        return end_point + "?" + param_str[:-1]

# 거래날짜, 전용면적, 거래금액, 법정동, 주택유형, 건물이름(아파트, 다세대) 전용면적 대비 거래금액
class TradeData:
    def __init__(self, do, gu, dong, year, month, day, price, area, category, name = ""):
        self.addr = "{} {} {}".format(do, gu, dong)
        self.date = "{}/{}/{}".format(year, month, day)
        self.price = price
        self.area = area
        self.price_per_area = round(price/area, 2)
        self.category = category
        self.name = name
        
    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.addr, self.date, self.price, self.area, self.price_per_area, self.category, self.name)
    
    def __repr__(self):
        return "{} {} {} {} {} {} {}".format(self.addr, self.date, self.price, self.area, self.price_per_area, self.category, self.name)

class RegCodeL():
    
    def __init__(self, do, gu, code):
        self.do = do
        self.gu = gu
        if type(code) == str:
            code = int(code)
        self.code = code
        
    def is_same_do(self, do):
        if self.do == do:
            return True
        return False
    
    def is_same_dogu(self, do, gu):
        if self.do == do and self.gu == gu:
            return True
        return False
    
    def __str__(self):
        return "{} {} {}".format(self.do, self.gu, self.code)
    def __repr__(self):
        return "{} {} {}".format(self.do, self.gu, self.code)

class RegCodeLDataProcessor:   
    def __init__(self):
        self.do_gu_list = []
    
    def read_file(self, file_path):
        f = open(file_path, 'r', encoding='euc-kr')
        while True:
            line = f.readline()
            if not line: 
                break
            split_line = line.split()
            if len(split_line) == 4:
                code, do, gu, posi = split_line
                if posi == "존재":
                    self.do_gu_list.append(RegCodeL(do, gu, code[:5])) 
        f.close()
        
    def get_do_list(self):
        do_list = []
        for do_gu in self.do_gu_list:
            if do_gu.do not in do_list:
                do_list.append(do_gu.do)
        return do_list
    
    def get_gu_list(self, do):
        gu_list = []
        for do_gu in self.do_gu_list:
            if do_gu.do == do:
                gu_list.append(do_gu.gu)
        return gu_list
    
    def search(self, do, gu):
        rtn_list = []

        for do_gu in self.do_gu_list:
            if gu == "전체":
                if do_gu.is_same_do(do):
                    rtn_list.append(do_gu)
            else:
                if do_gu.is_same_dogu(do, gu):
                    rtn_list.append(do_gu)
                    return rtn_list
        return rtn_list

    # self, do, gu, dong, year, month, day, price, area, category, name = ""
    def mapping_trade_data(self, called_data, do_gu):
        """
        called_data: api로 공공데이터 포털에서 가져온 데이터 리스트
        do_gu: RegCodeL 데이터 타입(도, 구, 법정동 코드가 들어간 데이터 타입)
        """
        APART = "아파트"
        DASAEDAE = "연립다세대"
        DAGAGU = "주택유형"
        mapped_data_list = []

        apart_count = 0
        dandok_count = 0
        dagagu_count = 0
        dasaedae_count = 0
        apart_sum = 0
        dandok_sum = 0
        dagagu_sum = 0
        dasaedae_sum = 0

        for data in called_data:
            category = ""
            name = "정보 없음(단독 주택 혹은 다가구)"
            area = 0
            if len(data) == 0:
                continue
            if APART in data:
                category = APART
                name = data[APART]
                area = data["전용면적"]
                apart_count += 1
                apart_sum += int(data["거래금액"].replace(",","")) / float(area)
            elif DASAEDAE in data:
                category = DASAEDAE
                name = data[DASAEDAE]
                area = data["대지권면적"]
                dasaedae_count += 1
                dasaedae_sum += int(data["거래금액"].replace(",","")) / float(area)
            elif DAGAGU in data:
                category = data[DAGAGU]
                area = data["대지면적"]
                if category == "단독":
                    dandok_count += 1
                    dandok_sum += int(data["거래금액"].replace(",","")) / float(area)
                else:
                    dagagu_count += 1
                    dagagu_sum += int(data["거래금액"].replace(",","")) / float(area)

            mapped_data_list.append(TradeData(do_gu.do, do_gu.gu, data["법정동"], data["년"], data["월"], data["일"], int(data["거래금액"].replace(",","")), float(area), category, name))
        avg_apart = 0
        avg_dasaedae = 0
        avg_dagagu = 0
        avg_dandok = 0
        if apart_count != 0:
            avg_apart = round(apart_sum/apart_count, 2)
        if dasaedae_count != 0:
            avg_dasaedae = round(dasaedae_sum/dasaedae_count, 2)
        if dagagu_count != 0:
            avg_dagagu = round(dagagu_sum/dagagu_count, 2)
        if dandok_count != 0:
            avg_dandok = round(dandok_sum/dandok_count, 2)

        return mapped_data_list, avg_apart, avg_dasaedae, avg_dagagu, avg_dandok