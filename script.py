import json, requests

file = open("imdb.json",)
data = json.load(file)

for record in data:
    url = "http://localhost:5000/api/v1/add/movie"
    header = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=json.dumps(record), headers=header)
    print(response)
