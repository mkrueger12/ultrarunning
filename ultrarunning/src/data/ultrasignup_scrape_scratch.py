# %load_ext line_profiler

import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re


def get_past_events(month):

    # get event data
    data = pd.read_json(f'https://ultrasignup.com/service/events.svc/closestevents?virtual=0&open=0&past=1&lat=0&lng=0&mi=500&mo=12&&m={month}&dist=4,5,6')

    return data


def get_d_id(event_date_id):

    r = requests.get(f'https://ultrasignup.com/results_event.aspx?dtid={event_date_id}')
    d_id = r.url.split("=", 1)[1]
    dict = {'EventDateId': event_date_id, 'did': d_id}

    return dict


def get_historical_d_id(d_id):

    r = requests.get(f'https://ultrasignup.com/results_event.aspx?did={d_id}')

    print(r.status_code, d_id)

    parsed_html = BeautifulSoup(r.content)

    links = []

    for link in parsed_html.find_all('a'):
        links.append(link.get('href'))

    links = pd.DataFrame(links, columns=['d_id'])

    links = links[links['d_id'].str.contains('did=') == True]

    links = list(links['d_id'].str.split("="))

    d_id_hist = set([el[1] for el in links])  # list of historical d_ids

    return d_id_hist


def get_d_id_event_title(d_id):

    ''' Takes a d_id and gets the event title '''

    r = requests.get(f'https://ultrasignup.com/results_event.aspx?did={d_id}')

    print(r.status_code, d_id)

    html = BeautifulSoup(r.content)

    title = remove_html_tags(str(html.title))

    title = title.strip()

    year = title[0:4]

    dict = {'EventName': title, 'EventD_Id': d_id, 'Year': year}

    return dict


def get_results(d_id, event_name):

    r = requests.get(f'https://ultrasignup.com/service/events.svc/results/{d_id}/1/json?_search=false&nd=1625680201306&rows=1500&page=1&sidx=status%20asc%2C%20&sord=asc')
    r = pd.DataFrame(r.json())
    r['EventName'] = event_name
    print(event_name)

    return r


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


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

# get event d_ids

d_id_list = [*map(get_d_id, data['EventDateId'])]

d_id_list = pd.DataFrame(d_id_list)

# merge d_id into master df

data = pd.merge(data, d_id_list)

# get historical d_id

hist_d_id = [*map(get_historical_d_id, set(data['did']))]

hist_d_id = [item for sublist in hist_d_id for item in sublist]

hist_d_id = set(hist_d_id)

# create df of hist d_id and event name

# %lprun -f get_d_id_event_title(hist_d_id)

hist_events = [*map(get_d_id_event_title, hist_d_id)]

hist_events = pd.DataFrame(hist_events)

# get results

results = [*map(get_results, hist_events['EventD_Id'], hist_events['EventName'])]

results = pd.concat(results)

