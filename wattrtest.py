import requests
city = input('input the city name')
print(city)
print('Displaying Weather report for: ' + city)


url = 'https://v2.wttr.in/{}?format=%h+%t+%f'.format(city)
res = requests.get(url)
print(res.text)