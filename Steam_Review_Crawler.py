import requests
import json

# Ask user to input the ID of their game - P5S:1382330
appid =  input("Please enter the steam ID: ")

# Take the input id and append it to the steam review API
url = "https://store.steampowered.com/appreviews/" + str(appid) + "?json=1"

# request GET from the given url
response = requests.get(url)

# Process the resonse in JSON format and print 
review = response.json()
print(review)