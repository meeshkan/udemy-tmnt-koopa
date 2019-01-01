# try
# python search_bing_api.py --query "teenage mutant ninja turtles" --query "teenage mutant ninja turtles cartoon" --query "teenage mutant ninja turtles leonardo" --query "teenage mutant ninja turtles michelangelo" --query "teenage mutant ninja turtles raphael" --output dataset/tmnt
# python search_bing_api.py --query "koopa troopa" --query "koopa paratroopa" --query "koopa red" --query "koopa troopa costume" --output dataset/koopa
# import the necessary packages
from requests import exceptions
import argparse
import requests
from PIL import Image
import os
# Microsoft Bing API key for the course
from key import API_KEY
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, action="append",
	help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())

# set (1) the
# maximum number of results for a given search and (2) the group size
# for results (maximum of 50 per request)
MAX_RESULTS = 250
GROUP_SIZE = 50
N_TRIES = 5
# set the endpoint API URL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
# insight url
INSIGHT_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/details"

# when attempting to download images from the web both the Python
# programming language and the requests library have a number of
# exceptions that can be thrown so let's build a list of them now
# so we can filter on them
EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])

# store the search term in a convenience variable then set the
# headers and search parameters
# initialize the total number of images downloaded thus far
total = 0
for term in args["query"]:
	headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
	curOffset = 0
	for trynum in range(N_TRIES):
		params = {"q": term, "offset": curOffset, "count": GROUP_SIZE}
		 
		# make the search
		search = requests.get(URL, headers=headers, params=params)
		search.raise_for_status()
		 
		# grab the results from the search, including the total number of
		# estimated results returned by the Bing API
		results = search.json()

		estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
		print("[INFO] {} total results for '{}'".format(estNumResults,
			term))
		 
		# loop over the estimated number of results in `GROUP_SIZE` groups
		for offset in range(0, estNumResults, GROUP_SIZE):
			# update the search parameters using the current offset, then
			# make the request to fetch the results
			print("[INFO] making request for group {}-{} of {}...".format(
				offset, offset + GROUP_SIZE, estNumResults))
			params["offset"] = offset
			search = requests.get(URL, headers=headers, params=params)
			search.raise_for_status()
			results = search.json()
			print("[INFO] saving images for group {}-{} of {}...".format(
				offset, offset + GROUP_SIZE, estNumResults))
			# loop over the results
			for v in results["value"]:
				# try to download the image
				try:
					# make a request to download the image
					print("[INFO] fetching: {}".format(v["contentUrl"]))
					r = requests.get(v["contentUrl"], timeout=30)
		 
					# build the path to the output image
					extl = v["contentUrl"].rfind(".")
					ext = v["contentUrl"][extl:extl+5]
					if ext is not '.jpeg':
						ext = ext[:4]
						if ext not in ['.png', '.jpg']:
							print("[INFO] skipping: {} extension".format(ext))
							continue
					p = os.path.sep.join([args["output"], "{}{}".format(
						str(total).zfill(8), ext)])
					# write the image to disk
					f = open(p, "wb")
					f.write(r.content)
					f.close()
		 
				# catch any errors that would not unable us to download the
				# image
				except Exception as e:
					# check to see if our exception is in our list of
					# exceptions to check for
					if type(e) in EXCEPTIONS:
						print("[INFO] skipping: {}".format(v["contentUrl"]))
						continue
				# try to load the image from disk
				try:
				    im=Image.open(p)
				    # do stuff
				except IOError:
				# if the image is `None` then we could not properly load the
				# image from disk (so it should be ignored)
					print("[INFO] deleting: {}".format(p))
					os.remove(p)
					continue
		 
				# update the counter
				total += 1
		if curOffset == results["nextOffset"]:
			break
		curOffset = results["nextOffset"]