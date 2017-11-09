import urllib.request
import json
import time

api_key_weather = 'd854e74a8cb4e5736b93589aa0e75716'

mag_url = 'http://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json'
plasma_url = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=tromso,no&appid=' + api_key_weather
kp_url = 'http://services.swpc.noaa.gov/products/noaa-planetary-k-index.json'

def response(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

class Capture():
    def __init__(self):

        self.plasma_vars = {
            'date': None,
            'time': None,
            'speed': None,
            'density': None,
            'temperature': None
        }

        self.magnitude_vars = {
            'date': None,
            'time': None,
            'bz': None,
            'bt': None,
            'lat': None,
            'long': None
        }

        self.weather_vars = {
            'main': None,
            'description': None,
            'humidity': None,
            'wind_speed': None,
            'wind_angle': None,
            'wind_clouds': None,
            'temperature': None,
            'sunrise': None,
            'sunset': None
        }

        self.kp = None

    def update_weather(self):
        weather_res = response(weather_url)
        weather_res = weather_res.decode('utf-8')

        obj = json.loads(weather_res)
        self.weather_vars['main'] = obj['weather'][0]['main']
        self.weather_vars['description'] = obj['weather'][0]['description']
        self.weather_vars['humidity'] = obj['main']['humidity']
        self.weather_vars['wind_speed'] = obj['wind']['speed']
        self.weather_vars['wind_angle'] = obj['wind']['deg']
        self.weather_vars['wind_clouds'] = obj['clouds']['all']
        self.weather_vars['temperature'] = str(int(obj['main']['temp']) - 273)

        sunrise = int(obj['sys']['sunrise']) - 1507586428
        sunset = int(obj['sys']['sunset']) - 1507586428
        self.weather_vars['sunrise'] = str(int(sunrise/3600)) + ':' + str(int(sunrise%3600/60))
        self.weather_vars['sunset'] = str(int(sunrise/3600)) + ':' + str(int(sunrise%3600/60))

    def update_magnitude(self):
        mag_res = response(mag_url)
        mag_res = mag_res.decode('utf-8')
        obj = json.loads(mag_res)
        data = obj[2]

        self.magnitude_vars['date'], self.magnitude_vars['time'] = data[0].split(' ')
        self.magnitude_vars['bz'] = data[3]
        self.magnitude_vars['long'] = data[4]
        self.magnitude_vars['lat'] = data[5]
        self.magnitude_vars['bt'] = data[6]

    def update_plama(self):
        plasma_res = response(plasma_url)
        plasma_res = plasma_res.decode('utf-8')
        pla = json.loads(plasma_res)
        data = pla[2]

        self.plasma_vars['density'] = data[1]
        self.plasma_vars['speed'] = data[2]
        self.plasma_vars['temperature'] = data[3]

    def update_kp(self):
        kp_res = response(kp_url)
        kp_res = kp_res.decode('utf-8')

        # print(type(kp_res.decode('utf-8')))
        kp = json.loads(kp_res)
        print(kp)

    def printAll(self):
        print(self.w_main)
        print(self.w_description)
        print('--- Weather ----')
        print('Clouds: ',self.w_clouds)
        print('Humidity: ',self.w_humidity)
        # print('Wind: ',self.w_wind_speed, 'm/s')
        # print('Wind: ',self.w_wind_angle, 'deg')
        # print('Temp: ', self.w_temperature, ' celcius')
        # print('Sunrise: ', self.w_sunrise)
        # print('Sunset: ', self.w_sunset)
        print('--- Aurora ---')
        print('Density: ', self.density)
        print('Speed: ', self.speed)
        print('Bz: ', self.bz)

    def create_json(self):
        weather = {}
        magnitude = {}
        plasma = {}
        dic = {}





def run(monitor):
    # print(monitor.update_kp())
    while(1):
        monitor.update_weather()
        i = 1
        while i < 15:
            monitor.update_plama()
            monitor.update_magnitude()
            monitor.printAll()
            i += 1
            time.sleep(60)

if __name__ == "__main__":
    print('Time\t\t Speed\t Density  Bz')
    monitor = Capture()
    # run(monitor)
    monitor.update_plama()
    print(monitor.plasma_vars)
    monitor.update_magnitude()
    print(monitor.magnitude_vars)

# print(json.loads(mag_res[0].decode('utf-8')))
