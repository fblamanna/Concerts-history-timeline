#
# 
# This Python script returns a .csv file with all information about the concerts for a single band or artist, 
# available on the [setlist.fm](http://www.setlist.fm/) website.
# You need to apply for a setlist.fm API key to download data and use them; they are free for non-commercial projects.
# You can get it here: http://api.setlist.fm/docs/index.html. 
# Please read the API Terms of Use (http://www.setlist.fm/help/terms) carefully.
#
# The algorithm takes as input the artist name (just for naming the output file) and 
# the Musicbrainz MBID (https://musicbrainz.org/doc/MusicBrainz_Database) code,
# which is an identifiable code for each artist or band in the database.
# I'm now working on an automatic call artist name - code. 
# In the meantime you have to manually add the code available on the Musicbrainz website.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
__author__ = """ Fabio Lamanna (fabio@fabiolamanna.it) """
#
#########################################################################
#
# Copyright (c) 2017 Fabio Lamanna (fabio@fabiolamanna.it). 
# Code under License GPLv3.
#
# Version History:
# 22.07.2016 - Version 0.1
# 27.12.2016 - Version 0.2 - Fixing bugs while reading .json
# 31.08.2017 - Version 0.3 - Adding Compatibility with Setlist.fm API 1.0
# 26.05.2018 - Version 0.4 - Handle missing json fields - Drop Python 2 support
#
# Input Parameters:
# artistname: name of the artist or band (string)  
# artistcode: Musicbrainz MBID (string)
# API_KEY: Setlist.fm valid API Key
#
# Execution:
# You can run the code using the command:  
# $ python TheConcertsTracker.py 'artistcode' 'artistname' 'API_KEY'
#
#########################################################################

# Import Modules
try:
	import ujson as json
except:
	import json

import requests
import csv
import sys
import math

#########################################################################

def main():

	# Set Workbooks for .csv
	f = open(sys.argv[2] + 'ConcertsTracker.csv', 'wt', encoding='utf-8')

	# Inizialize .csv file
	writer = csv.writer(f, delimiter=';')

	# Write .csv headers
	writer.writerow( 
	                (
	                'eventID',
	                'artist',
	                'eventdate',
	                'tourname',
	                'venue',
	                'venue_id',
	                'city',
	                'city_id',
	                'city_lat',
	                'city_lon',
	                'state',
	                'state_id',
	                'country',
	                'country_id'
	                )
	                )

	# Call Setlist.fm API
	url = 'https://api.setlist.fm/rest/1.0/artist/' + sys.argv[1] + '/setlists?p=1'
	headers = {'Accept': 'application/json', 'x-api-key': sys.argv[3]}
	r = requests.get(url, headers=headers)
	
	# Get .json Data
	data = r.json()

	# Get total number of shows and handle missing shows
	try:
		
		totalshows = int(data['total'])

	except:
		print('Sorry, the artist you are looking for has no concerts in the database')
		sys.exit(1)

	# Total Number of Pages needed to load
	pages = int(math.ceil(totalshows/20))

	for page in range(1,pages):

		url = 'https://api.setlist.fm/rest/1.0/artist/' + sys.argv[1] + '/setlists?p=' + str(page)
		headers = {'Accept': 'application/json', 'x-api-key': sys.argv[3]}
		r = requests.get(url, headers=headers)
	
		# Get .json Data
		data = r.json()

		# Read .json file line per line
		for line in data:

			for i in range(len(data['setlist'])):

				# Check existence of Tour Name (other fields are mandatory or automatically created)
				try:
					c = data['setlist'][i]['tour']['name']
				except KeyError:
					c = 'None'

				writer.writerow(
				                (
				                # Event ID
				                data['setlist'][i]['id'],
				                # Artist
				                data['setlist'][i]['artist']['name'],
				                # Eventdate
				                data['setlist'][i]['eventDate'],
				                # TourName
				                c,
				                # Venue
				                data['setlist'][i]['venue'].get('name'),
				                # Venue ID
				                data['setlist'][i]['venue'].get('id'),
				                # City
				                data['setlist'][i]['venue']['city'].get('name'),
				                # City ID
				                data['setlist'][i]['venue']['city'].get('id'),
				                # City Latitude
				                float(data['setlist'][i]['venue']['city']['coords'].get('lat')),
				                # City Longitude
				                float(data['setlist'][i]['venue']['city']['coords'].get('long')),
				                # State
				                data['setlist'][i]['venue']['city'].get('state'),
				                # State Code
				                data['setlist'][i]['venue']['city'].get('stateCode'),
				                # Country
				                data['setlist'][i]['venue']['city']['country'].get('name'),
				                # Country Code
				                data['setlist'][i]['venue']['city']['country'].get('code')
				                )
				                )

	f.close()

if __name__ == '__main__':

	main()


