import requests
import os
import datetime

# 보안 설정값
API_KEY = os.environ.get('DATA_API_KEY')
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = "8470635650" # 아까 성공하신 본인의 숫자 ID로 꼭 확인해 주세요!

def get_hospital_update():
    # 1. 공공데이터 API 주소 (병원 목록)
    url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'
    
    # 2. 청주시 4개 구 코드 (상당, 서원, 흥덕, 청원)
    sggu_codes = ['330401', '330402', '330403', '330404']
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    report = f"🏥 [청주시 병원 동향 리포트]\n날짜: {today}\n"
    report += "----------------------------\n"
    
    found_count = 0
    
    for code in sggu_codes:
        params = {
            'serviceKey': requests.utils.unquote(API_KEY),
            'sgguCd': code,
            'numOfRows': '10',
            '_type': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            items = data['response']['body']['items']
            
            if items:
                item_list = items['item']
                if isinstance(item_list, dict): item_list = [item_list]
                
                for item in item_list:
                    name = item.get('yadmNm')      # 병원명
                    category = item.get('clCdNm')  # 의원/병원 구분
                    addr = item.get('addr')        # 주소
                    tel = item.get('telno', '-')   # 전화번호
                    
                    report += f"📍 {name} ({category})\n🏢 {addr}\n📞 {tel}\n\n"
                    found_count += 1
        except Exception as e:
            continue

    if found_count == 0:
        report += "현재 새로 업데이트된 병원이 없습니다."
    else:
        report += f"총 {found_count}개의 병원 정보를 확인했습니다."
        
    return report

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

if __name__ == "__main__":
    content = get_hospital_update()
    send_telegram(content)
