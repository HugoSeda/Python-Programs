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

soloists_data = json_normalize(data=d['programs'], record_path=['works', 'soloists'],
							meta=['programID', ['works', 'ID']])
							
soloists_data.columns = ['soloistName', 'soloistInstrument', 'soloistRoles', 'programID', 'ID']

new = pd.merge(nyphil, concerts_data, on='programID', how='outer')
new2 = pd.merge(new, works_data, on='programID', how='outer')
new3 = pd.merge(new2, soloists_data, on=['programID', 'ID'], how='outer')

#Removes redundant columns
del new3['concerts']
del new3['works']
del new3['soloists']

new3.to_csv('2011-12_TO_NOW.csv')