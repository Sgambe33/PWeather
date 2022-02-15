import requests
url = 'https://wttr.in/?format="%l"'
res = requests.get(url)
print(res.text)