import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time


# build table of names and place


URL = "https://www.opensplittime.org/events/2017-high-lonesome-100/spread"

def main(year):


    url = f"https://www.opensplittime.org/events/{year}-high-lonesome-100/spread"

    r = requests.get(url)

    if r.status_code != 200:
        print('No Data for', year)
        pass
    else:
        print('Getting data for', year)
        time.sleep(2)
        soup = BeautifulSoup(r.content, 'lxml') # If this line causes an error, run 'pip install html5lib' or install html5lib
        table = soup.findAll('table')

        table1 = table[0]

        body = table1.find_all("tr")

        # Head values (Column names) are the first items of the body list
        head = body[0] # 0th item is the header row
        body_rows = body[1:] # All other items becomes the rest of the rows

        # Lets now iterate through the head HTML code and make list of clean headings

        # Declare empty list to keep Columns names
        headings = []
        for item in head.find_all("th"): # loop through all th elements
            # convert the th elements to text and strip "\n"
            item = (item.text).rstrip("\n")
            # append the clean column name to headings
            headings.append(item)

        # Next is now to loop though the rest of the rows

        #print(body_rows[0])
        all_rows = [] # will be a list for list for all rows
        for row_num in range(len(body_rows)): # A row at a time
            row = [] # this will old entries for one row
            for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
                # row_item.text removes the tags from the entries
                # the following regex is to remove \xa0 and \n and comma from row_item.text
                # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
                aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
                #append aa to row - note one row entry is being appended
                row.append(aa)
            # append one row to all_rows
            all_rows.append(row)

        # all_rows becomes our data and headings the column names
        df = pd.DataFrame(data=all_rows,columns=headings)
        df['year'] = year

        # convert to long data
        df = pd.melt(df,id_vars=['O/GPlace', 'Bib', 'Name', 'Category', 'From', 'Status', 'year'],var_name='aid_station', value_name='time')

        #clean aid station data
        df[['aid_station', 'mile']] = df['aid_station'].str.split("(", expand=True)
        df[['in', 'out']] = df['time'].str.split("/", expand=True)
        df['mile'] = df['mile'].str.strip()
        df['mile'] = df['mile'].str.replace('Mile ',  '')
        df['mile'] = df['mile'].str.replace(')', '')
        df['aid_station'] = df['aid_station'].str.strip().str.replace(' / Out', '').str[:-2].str.replace('Fini', 'Finish')

        df = [['O/GPlace', 'Bib', 'Name', 'From', 'Status', 'year',
       'aid_station', 'mile', 'in', 'out']]

        return df
xa

data = []

for i in range(2017, 2022):

    data.append(main(i))

data = pd.concat(data)
