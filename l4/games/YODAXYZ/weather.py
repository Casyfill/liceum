import os
API_KEY = os.environ.get('OWM_KEY', None)


def show_status(city):
    global owm
    observation = owm.weather_at_place(city)
    w = observation.get_weather()  # weather data
    print("_" * 40)
    print()
    print(city)
    print("-" * 40)
    print(w.get_detailed_status())
    print("-" * 40)
    print("temp: ", w.get_temperature('celsius')['temp'], 'c°', w.get_temperature()['temp'], 'f°')
    print("-" * 40)
    print("humidity: ", w.get_humidity())
    print("-" * 40)
    print("wind: ", w.get_wind()['speed'], "m/c")
    print("_" * 40)



def main():
    import pyowm
    owm = pyowm.OWM(API_KEY)

    while True:
        city = input("Your city: ")
        if city.lower() == 'england':
            print('England is my city!')  # Philipp - England is not a city
            break
        try:
            show_status(city)
            break
        except:
            print('City is not found! Enter again')


if __name__ == '__main__':
    main()





