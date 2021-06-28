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

def get_entrants(data, event_id):

    data = data[['EventDateId', 'EventId', 'EventName', 'EventDate']].drop_duplicates()
    data = data[data[0] == event_id]

    resp = requests.get(url=f'https://ultrasignup.com/entrants_event.aspx?did={event_id}')
    df = pd.read_html(resp.content)

    df = pd.DataFrame(df[0])

    df['EventName'] = data[2]

    df['EventDateId'] = data[0]

    df['EventId'] = data[1]

    df['EventDate'] = data[3]

    return df

#scrape data
url = 'https://ultrasignup.com/service/events.svc/closestevents?virtual=0&open=1&past=0&lat=0&lng=0&mi=500&mo=12&&m=1&dist=3,4,5,6,7'


resp = requests.get(url=url)
data = resp.json()  # Check the JSON Response Content documentation below

event_data = pd.DataFrame(data)

# get eventId
event_id = [*map(get_eventId, event_data['EventDateId'])]
event_id = pd.DataFrame(event_id)
data = pd.merge(event_id, event_data)

event_data.reset_index(inplace=True)

# get entrant list
event_id = [*map(get_entrants, event_data, data['EventID'])]

