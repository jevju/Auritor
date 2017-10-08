import urllib.request
import json
import time

mag_url = 'http://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json'
plasma_url = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'

def response(url):
    with urllib.request.urlopen(url) as response:
        return response.read()
#

class Capture():
    def __init__(self, data1, data2):
        self.date = ''
        self.time = ''
        self.speed = ''
        self.density = ''
        self.bz = ''
        self.bt = ''
        self.lat = ''
        self.long = ''
        self.temperature = ''

        self.analyze(data1, data2)

    def analyze(self, data1, data2):
        self.date, self.time = data1[0].split(' ')
        self.bz = data1[3]
        self.long = data1[4]
        self.lat = data1[5]
        self.bt = data1[6]
        self.density = data2[1]
        self.speed = data2[2]
        self.temperature = data2[3]




def monitor():
    mag_res = response(mag_url)
    mag_res = mag_res.decode('utf-8')

    plasma_res = response(plasma_url)
    plasma_res = plasma_res.decode('utf-8')

    obj = json.loads(mag_res)
    captions = obj[0]
    data1 = obj[1]
    data2 = obj[2]

    pla = json.loads(plasma_res)


    #
    # for d, i in enumerate(captions):
    #     print(i, '\t', data1[d], '\t', data2[d])


    mon = Capture(obj[2], pla[2])

    print(mon.time,'\t', mon.speed, ' ',mon.density, '\t ', mon.bz)


if __name__ == "__main__":
    print('Time\t\t Speed\t Density  Bz')
    while(1):
        try:
            monitor()
        except:
            pass
        time.sleep(30)

# print(json.loads(mag_res[0].decode('utf-8')))
