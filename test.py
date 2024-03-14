import requests
import json
from string import ascii_lowercase
headers = {
    'authority': 'api.csacademyzone.com',
    'accept': 'application/json, text/plain, */*',
}
json_data = {
    'active': 1,
}
response = requests.post('https://api.csacademyzone.com/lectures', headers=headers, json=json_data)
data = response.json()
filtered_lectures = []
for lecture in data['lectures']:
    filtered_lecture = {
        "id": lecture["id"],
        "title": lecture["title"]
    }
    for part in ascii_lowercase:
        part_key = f"part_{part}_video"
        if part_key in lecture and lecture[part_key]:
            filtered_lecture[part_key] = lecture[part_key]
    filtered_lectures.append(filtered_lecture)
result = {"filtered_lectures": filtered_lectures}

with open("website/Backend/ashraf.json", 'w') as output_file:
    json.dump(result, output_file, indent=2)


print(result)
