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
        self.content_plasma = ""
        self.content_magnitude = ""
        self.content_weather = ""
        self.date = ''
        self.time = ''
        self.speed = ''
        self.density = ''
        self.bz = ''
        self.bt = ''
        self.lat = ''
        self.long = ''
        self.temperature = ''

        self.w_main = ''
        self.w_description = ''
        self.w_humidity = ''
        self.w_wind_speed = ''
        self.w_wind_angle = ''
        self.w_clouds = ''
        self.w_temperature = ''
        self.w_sunrise = ''
        self.w_sunset = ''

    def update_weather(self):
        weather_res = response(weather_url)
        weather_res = weather_res.decode('utf-8')

        obj = json.loads(weather_res)
        self.w_main = obj['weather'][0]['main']
        self.w_description = obj['weather'][0]['description']
        self.w_humidity = obj['main']['humidity']
        self.w_wind_speed = obj['wind']['speed']
        self.w_wind_angle = obj['wind']['deg']
        self.w_clouds = obj['clouds']['all']
        self.w_temperature = str(int(obj['main']['temp']) - 273)

        sunrise = int(obj['sys']['sunrise']) - 1507586428
        sunset = int(obj['sys']['sunset']) - 1507586428
        self.w_sunrise = str(int(sunrise/3600)) + ':' + str(int(sunrise%3600/60))
        self.w_sunset = str(int(sunrise/3600)) + ':' + str(int(sunrise%3600/60))

    def update_magnitude(self):
        mag_res = response(mag_url)
        mag_res = mag_res.decode('utf-8')
        obj = json.loads(mag_res)
        data = obj[2]

        self.date, self.time = data[0].split(' ')
        self.bz = data[3]
        self.long = data[4]
        self.lat = data[5]
        self.bt = data[6]

    def update_plama(self):
        plasma_res = response(plasma_url)
        plasma_res = plasma_res.decode('utf-8')
        pla = json.loads(plasma_res)
        data = pla[2]

        self.density = data[1]
        self.speed = data[2]
        self.temperature = data[3]

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

# test = Capture()utf-8
# test.update_weather()


#
# def monitor():
#     mag_res = response(mag_url)
#     mag_res = mag_res.decode('utf-8')
#
#     plasma_res = response(plasma_url)
#     plasma_res = plasma_res.decode('utf-8')
#
#     obj = json.loads(mag_res)
#     captions = obj[0]
#     data1 = obj[1]
#     data2 = obj[2]
#
#     pla = json.loads(plasma_res)
#
#
#
#     mon = Capture(obj[2], pla[2])
#
#     print(mon.time,'\t', mon.speed, ' ',mon.density, '\t ', mon.bz)
#

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
    run(monitor)

# print(json.loads(mag_res[0].decode('utf-8')))
