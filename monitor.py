import urllib.request
import json
import time

api_key_weather = 'd854e74a8cb4e5736b93589aa0e75716'


def response(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

class Auritor():
    def __init__(self):

        self.mag_url = 'http://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json'
        self.plasma_url = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
        self.weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=tromso,no&appid=' + api_key_weather
        self.kp_url = 'http://services.swpc.noaa.gov/products/noaa-planetary-k-index.json'

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
        weather_res = response(self.weather_url)
        weather_res = weather_res.decode('utf-8')
        obj = json.loads(weather_res)
        print(obj)
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
        mag_res = response(self.mag_url)
        mag_res = mag_res.decode('utf-8')
        obj = json.loads(mag_res)
        data = obj[2]

        self.magnitude_vars['date'], self.magnitude_vars['time'] = data[0].split(' ')
        self.magnitude_vars['bz'] = data[3]
        self.magnitude_vars['long'] = data[4]
        self.magnitude_vars['lat'] = data[5]
        self.magnitude_vars['bt'] = data[6]

    def update_plama(self):
        plasma_res = response(self.plasma_url)
        plasma_res = plasma_res.decode('utf-8')
        pla = json.loads(plasma_res)
        data = pla[2]

        self.plasma_vars['date'] = data[0].split(" ")[0]
        self.plasma_vars['time'] = data[0].split(" ")[1]
        self.plasma_vars['density'] = data[1]
        self.plasma_vars['speed'] = data[2]
        self.plasma_vars['temperature'] = data[3]

    def update_kp(self):
        kp_res = response(self.kp_url)
        kp_res = kp_res.decode('utf-8')
        kp_res = json.loads(kp_res)

        for kp in kp_res:
            print(kp[0], kp[1])
        print('---')
        print(kp_res)

    # def create_json(self):
    #     weather = {}
    #     magnitude = {}
    #     plasma = {}
    #     dic = {}
    #
    #     dic['magnitude'] = self.magnitude_vars
    #     dic['plasma'] = self.plasma_vars
    #     # dic['kp'] = self.kp
    #     dic['weather'] = self.weather_vars
    #     # print(dic)
    #     return json.dumps(dic, indent=4)

    def monitor(self, magnitude = 1, plasma = 1, weather = 0):
        dic = {}
        try:
            if magnitude:
                self.update_magnitude()
                dic['magnitude'] = self.magnitude_vars
            if plasma:
                self.update_plama()
                dic['plasma'] = self.plasma_vars
            if weather:
                self.update_weather()
                dic['weather'] = self.weather_vars
        except Exception as e:
            dic['Error'] = 'Unable to fetch data ...'
            print(e)

        return json.dumps(dic, indent=4)

if __name__ == "__main__":
    # print('Time\t\t Speed\t Density  Bz')
    auritor = Auritor()
    # run(monitor)
    try:
        result = auritor.monitor(weather = 1)
        print(result)
        # monitor.update_plama()
        # monitor.update_magnitude()
        # monitor.update_kp()
        # monitor.update_weather()
        # print(monitor.create_json())
    except Exception as e:
        print("Unable to fetch data ...")
        print(e)
