import pandas as pd
import numpy as np
import requests
import io


def get_eventId(dtid_id):

    url = f'https://ultrasignup.com/register.aspx?dtid={dtid_id}'
    resp = requests.get(url=url)
    event_id = resp.url[-5:]
    dict = {'EventDateId': dtid_id, 'EventID': event_id}
    print('Conversion of', dtid_id, 'to', event_id, 'Completed.')

    return dict

def get_entrants(event_id, event_data):

    event_data = event_data[['EventDateId', 'EventId', '']]

    resp = requests.get(url=f'https://ultrasignup.com/entrants_event.aspx?did={event_id}')
    df = pd.read_html(resp.content)
    df = pd.DataFrame(df[0])
    df['Ev']


#scrape data
url = 'https://ultrasignup.com/service/events.svc/closestevents?virtual=0&open=1&past=0&lat=0&lng=0&mi=500&mo=12&&m=1&dist=3,4,5,6,7'


resp = requests.get(url=url)
data = resp.json()  # Check the JSON Response Content documentation below

data = pd.DataFrame(data)

# get eventId
event_id = [*map(get_eventId, data['EventDateId'])]
event_id = pd.DataFrame(event_id)
data = pd.merge(event_id, data)

# get entrant list
resp = requests.get(url='https://ultrasignup.com/entrants_event.aspx?did=78606')
df = pd.read_html(resp.content)
df = pd.DataFrame(df[0])

