import requests

# Parameters
img = r"pictures\red_apple.jpg"
api_user_token = '2710ac37c1819349968b4936d26201cc149ecfa1'
headers = {'Authorization': 'Bearer ' + api_user_token}

# Food Type Detection
api_url = 'https://api.logmeal.es/v2'
endpoint = '/image/recognition/dish'
response = requests.post(api_url + endpoint,
                    files={'image': open(img, 'rb')},
                    headers=headers)

resp = response.json()
print(resp)

#Loop through food_types and print the name with highest probability
max_prob = 0
max_name = ''
for food in resp['recognition_results']:
    if food['prob'] > max_prob:
        max_prob = food['prob']
        max_name = food['name'].lower()
print(max_name)