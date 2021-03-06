# cloud_project
공공 데이터 포털의 rest API를 사용하여 만든 웹 어플리케이션 입니다.
API를 이용하여 공공 데이터 포털에서 부동산 데이터를 받아와 기간과 검색을 통해 필터링 할 수 있고, 그래프를 통해 건물 종류 수와 건물 종류당 평균 거래 금액 추이를 볼 수 있습니다.

### 사용한 공공 데이터 API
1.  국토교통부_아파트매매 실거래자료 
(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058747)
2. 국토교통부_연립다세대 매매 실거래자료 
(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058038)
3. 국토교통부_단독/다가구 매매 실거래 자료 
(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058022)

### 동작 화면
![image](https://user-images.githubusercontent.com/31751481/102386552-88953180-4012-11eb-8c35-4483761f3480.png)
![image](https://user-images.githubusercontent.com/31751481/102386595-96e34d80-4012-11eb-8fd6-bfca4256d9e4.png)
![image](https://user-images.githubusercontent.com/31751481/102387001-31dc2780-4013-11eb-9b49-24485dae3c76.png)

### 실행
플라스크 폴더에서 serviceKey.txt에 서비스키 넣은 후
run.py 실행

### 배포하여 실행
루트폴더에서 
docker-compose up --build
명령어 실행 (docker, docker-compose가 설치되어 있어야함)



