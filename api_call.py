import requests

url = "http://0.0.0.0:5001/generate_img"

payload = {}
files=[
  ('image',('file',open('/home/leo/Downloads/387325501_1331935500745611_5516241521850637824_n.jpg','rb'),'application/octet-stream'))
]
headers = {
  'accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)