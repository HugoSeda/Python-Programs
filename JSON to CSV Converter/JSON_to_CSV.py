import pandas as pd
import json
from pandas import json_normalize
import requests

"""
This program converts NYPhil's Performance History JSON files to CSV files.
It's currently pointing to the 2011-12_TO_NOW file, but the url can be changed 
to another file within that folder. The url does need to be the "raw" version.

"""

d = requests.get('https://raw.githubusercontent.com/nyphilarchive/PerformanceHistory/master/Programs/json/2011-12_TO_NOW.json').json()

nyphil = json_normalize(d['programs'])

works_data = json_normalize(data=d['programs'], record_path='works', 
                            meta=['programID'])

concerts_data = json_normalize(data=d['programs'], record_path='concerts',
							meta=['programID'])

new = pd.merge(nyphil, concerts_data, on='programID', how='outer')
new2 = pd.merge(new, works_data, on='programID', how='outer')

#Removes redundant columns
del new2['concerts']
del new2['works']

new2.to_csv('NYPhil.csv')