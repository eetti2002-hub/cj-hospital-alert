import requests
import os
import datetime

# 1. 설정값 (본인의 정보로 업데이트됨)
API_KEY = os.environ.get('DATA_API_KEY')
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = "8470635650"  # 알려주신 ID로 고정했습니다!

def get_hospital_update():
    # 개폐업 현황을 포함한 병원 기본정보 API
    url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'
    sggu_codes = ['330401', '330402', '330403', '330404'] # 청주시 4개 구
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    report = f"🏥 [청주시 병원 개/폐업 동향]\n기준일: {today}\n"
    report += "----------------------------\n"
    
    found_count = 0
    
    for code in sggu_codes:
        params = {
            'serviceKey': requests.utils.unquote(API_KEY),
            'sgguCd': code,
            'numOfRows': '20',
            '_type': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # 데이터 추출
            items = data.get('response', {}).get('body', {}).get('items', {})
            if items:
                item_list = items.get('item', [])
                if isinstance(item_list, dict): item_list = [item_list]
                
                for item in item_list:
                    name = item.get('yadmNm')      # 병원명
                    category = item.get('clCdNm')  # 의원/병원 구분
                    addr = item.get('addr')        # 주소
                    tel = item.get('telno', '-')   # 전화번호
                    
                    # 리스트에 추가
                    report += f"📍 {name} ({category})\n🏢 {addr}\n📞 {tel}\n\n"
                    found_count += 1
        except Exception as e:
            continue

    if found_count == 0:
        report += "🔔 현재 새롭게 업데이트된 개/폐업 정보가 없습니다."
    else:
        report += f"✅ 총 {found_count}건의 최근 변동 사항을 확인했습니다."
        
    return report

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

if __name__ == "__main__":
    content = get_hospital_update()
    send_telegram(content)
