import requests

def get_location(zip_code):
    # ジオコーディングAPIを使用して郵便番号から位置情報を取得
    geocode_url = f"http://zipcloud.ibsnet.co.jp/api/search?zipcode={zip_code}"
    response = requests.get(geocode_url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]
            address = f"{location['address1']} {location['address2']} {location['address3']}"
            return address
        else:
            print("Invalid zip code or no results found.")
            return None
    else:
        print(f"Failed to retrieve location data. Status code: {response.status_code}")
        return None

def get_weather(zip_code):
    # 郵便番号から位置情報を取得
    location = get_location(zip_code)
    if location is None:
        return
    
    # 気象庁APIのエンドポイントとパラメータ
    base_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/'
    params = {
        'q': location,
        'format': 'json'
    }
    
    # 天気予報情報の取得
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        # 今日と明日の天気予報を取得
        today_weather = weather_data[0]['timeSeries'][0]['areas'][0]
        tomorrow_weather = weather_data[0]['timeSeries'][1]['areas'][0]
        
        print(f"Today's weather in {zip_code}:")
        print(f"Condition: {today_weather['weathers'][0]}")
        print(f"Temperature: {today_weather['temps'][0]} °C")
        
        print(f"\nTomorrow's weather in {zip_code}:")
        print(f"Condition: {tomorrow_weather['weathers'][0]}")
        print(f"Temperature: {tomorrow_weather['temps'][1]} °C")
    else:
        print(f"Failed to retrieve weather data. Status code: {response.status_code}")

# 例: 郵便番号100-0001の天気情報を取得
get_weather('1000001')
