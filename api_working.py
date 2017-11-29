import json
from urllib.request import urlopen
import functools
import numpy as np
import pandas as pd

# gecode wrapper
def geocode(base_url, address, api_key = None):
	if api_key is None:
		file = open('data/google_api_key.txt')
		key = file.read()
		file.close()

	parsed_address = parse_address(address)
	# url = base_url + parsed_address + '&key=' + key + '&sensor=false'
	url = base_url + 'key=' + key + '&address=' + parsed_address
	api = call_api(url)
	return get_coords(api)

# From left to right increasing granularity
# np array-like
# e.g.
# array(['1600 Amphitheatre Parkway', 'Mountain View', 'CA'])
# parses address into format to send to the api called
def parse_address(address):
	return functools.reduce(lambda x, y: x + ',+' + y, address).replace(' ','+')

# calling api with parsed string
def call_api(url):
	try:
		output = json.loads(urlopen(url).read())
	except:
		print('FAILED!')
		output = {'results:':None, 'status':'API_Call_Fail'}
	return output

# clean api response 	
def get_coords(api_response):
	if api_response['status'] == 'OK':
		print('API SUCCESS')
		loc = api_response['results'][0]['geometry']['location']
	else:
		print('NO RESPONSE FROM API')
		loc = {'lat':0, 'long':0}
	return tuple(loc.values())

def main():
	qrcs = pd.read_csv('data/qrc_locs_no_coords2.csv', encoding = 'latin1')
	qrcs.fillna('', inplace = True)
	base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

	coords = []

	for row in qrcs.itertuples():
		needed_fields = ['Address', 'City', 'State', 'Country']
		iter_address = [getattr(row, field) for field in needed_fields]
		coords.append(geocode(base_url, iter_address))

	output = pd.DataFrame(coords,
		columns = ['latitude', 'longitude'],
		index = qrcs['QRC_Index'])
	qrcs.set_index('QRC_Index', inplace = True)
	write_out = qrcs.merge(output, how = 'inner',
		right_index = True, left_index = True)
	write_out.to_csv('data/qrcs_with_coords.csv')

if __name__ == '__main__':
	main()