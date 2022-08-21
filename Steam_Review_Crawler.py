import requests
import json

# Ask user to input the ID of their game - P5S:1382330
appid = input("Please enter the steam ID: ")
review_store = "Processed_Reviews.txt"
open(review_store, 'w').close()
# review_type = input("Would you like your results sorted by date? (Y/N)")

# request_options = 
# {
#     "json": "1",
#     "language": "all",  # API language code e.g. english or schinese
#     "filter": "recent",  # To work with 'start_offset', 'filter' has to be set to either recent or updated, not all.
#     "review_type": "all",  # e.g. positive or negative
#     "purchase_type": "all",  # e.g. steam or non_steam_purchase
#     "num_per_page": "100",  # default is 20, maximum is 100
# }


# Take the input id and append it to the steam review API
url = "https://store.steampowered.com/appreviews/" + str(appid) + "?json=1"

# request GET from the given url
response = requests.get(url)

# Process the resonse in JSON format and print 
review = response.json()
# processed_review = 
print(review)

with open(review_store, 'w') as f:
    json.dump(review, f)