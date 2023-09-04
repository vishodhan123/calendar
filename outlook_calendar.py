import requests
from msal import ConfidentialClientApplication
from datetime import datetime
import pytz

client_id = '64646384-e935-4f96-8e2c-180e9126bc7e'
client_secret = 'G3w8Q~aybD~RqjAtvlHnRMlMKYZLLkCSLjHrocpm'
tenant_id = '34ff36e5-5c1f-468c-ba38-2f92da7bcd6b'



app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=f'https://login.microsoftonline.com/{tenant_id}'
)

# Get an access token
scopes = ['https://graph.microsoft.com/.default']
result = app.acquire_token_silent(scopes=scopes, account=None)
print(result)
if not result:
    result = app.acquire_token_for_client(scopes=scopes)
print(result, "123")
access_token = result['access_token']

# Using the access token to make API requests
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.get('https://graph.microsoft.com/v1.0/me/events', headers=headers)
events = response.json()
print(events)

for event in events['value']:
    print(event['subject'])

# ist_timezone = pytz.timezone('Asia/Kolkata')
#
# current_time = datetime.now(ist_timezone)
# start_time = current_time.replace(hour=14, minute=0, second=0, microsecond=0)
# end_time = current_time.replace(hour=15, minute=0, second=0, microsecond=0)
#
# new_event = {
#     'subject': 'Meeting',
#     'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
#     'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'}
# }
#
# response = requests.post('https://graph.microsoft.com/v1.0/me/events', headers=headers, json=new_event)
# print(response.status_code)
