import keyring
import requests
import json
import logging
from splunk_hec_handler import SplunkHecHandler

logger = logging.getLogger('SplunkHecHandlerExample')
logger.setlevel(logging.DEBUG)
hec_handler = SplunkHecHandler('localhost', hec_handler, port=8088, proto='http', source="s1")
logger.addHandler(splunk_handler)
### logging to splunk

host = "localhost"
port = ":8088"
site = "http://" + host + port
endpoint = "/services/collector/event"
headers = {"Authorization": "Splunk "+hec_handler, 'Content-Type': 'application/json'}
server= "app.scalyr.com"
port= "443"
token = keyring.get_password("dataset","dataset")
server = "https://" + server+":"+port+"/api/powerquery"
headers = {"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}
query = "serverHost = * | group count = count() by serverHost"
body= json.dumps[{
"token": token,
"query": query,
"startTime": "5.1 minutes",
"endTime": "0.1 minutes",
"priority": "low"
}]
reponse = requests.post(server, data=body, headers=headers)
if response.status_code != 200
  print('status: ', response.status_code, 'Headers: ', response.headers)
  print('error')
  exit()
data-response.json()
print(data.values)
values= data["values"]
for value in values:
  print(value)
  logger.info(value)
exit()
