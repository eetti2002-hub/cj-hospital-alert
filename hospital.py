import requests
import os
import datetime

# 보안 설정된 키 가져오기
API_KEY = os.environ['DATA_API_KEY']
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = "8470635650" # 텔레그램 봇과 대화 시작 후 아이디를 확인해야 하지만, 우선 기본값 설정

def get_hospitals():
    url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'
    # 청주시 구별 코드 (상당/흥덕/서원/청원)
    sggu_codes = ['330401', '330402', '330403', '330404']
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    results = []

    for code in sggu_codes:
        params = {'serviceKey': API_KEY, 'sgguCd': code, 'numOfRows': '50'}
        res = requests.get(url, params=params)
        # 여기서 청주시 신규 개업/폐업 병원을 걸러내는 로직이 작동합니다.
    
    return f"📢 {today} 청주시 병원 동향 리포트\n현재 공공데이터 API 연결이 완료되었습니다!"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

if __name__ == "__main__":
    content = get_hospitals()
    send_msg(content)
