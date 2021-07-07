import pandas as pd
import numpy as np
import requests
import io
from datetime import datetime

def get_past_events(month):

    # get event data
    data = pd.read_json(f'https://ultrasignup.com/service/events.svc/closestevents?virtual=0&open=0&past=1&lat=0&lng=0&mi=500&mo=12&&m={month}&dist=4,5,6')

    return data


def get_results(event_date_id):

    r = requests.get(f'https://ultrasignup.com/results_event.aspx?dtid={event_date_id}')
    d_id = r.url.split("=", 1)[1]
    dict = {'event_date_id': event_date_id, 'did': d_id}

    return dict


# get event data

month = [*range(1, 7)]

data = [*map(get_past_events, month)]

data = pd.concat(data)

data.reset_index(inplace=True, drop=True)

# filter event data

data['EventDate'] = pd.to_datetime(data['EventDate'])

data = data[data['EventDate'] < datetime.today()]

data = data[data['Cancelled'] == False]
data = data[data['VirtualEvent'] == False]


