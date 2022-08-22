import requests
import json

# Ask user to input the ID of their game - P5S:1382330
# appid = input("Please enter the steam ID: ")
appid = 1382330
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
url = f'https://store.steampowered.com/appreviews/{appid}?json=1'

# request GET from the given url
response = requests.get(url)

# Process the resonse in JSON format and print 
# review = response.json()
# print(review)

# with open(review_store, 'w') as f:
    # json.dump(review, f, sort_keys=True, ensure_ascii=False, indent=4)

# review_str = json.dumps(review, indent=2)

# processed_review = review_str[0]['success']
# print(processed_review)

data = json.loads(response.text)

#placeholder id generation
id = str(data['reviews'][0]['author']['steamid']) + str(appid)
if (data['reviews'][0]['steam_purchase']) == True:
    review_source = "steam"
else:
    review_source = "other"

print(id)
print(data['reviews'][0]['author']['steamid'])
print(data['reviews'][0]['timestamp_created'])
print(data['reviews'][0]['author']['playtime_forever'])
print(data['reviews'][0]['review'])
print(data['reviews'][0]['comment_count'])
print(review_source)
print(data['reviews'][0]['votes_up'])
print(data['reviews'][0]['votes_funny'])
print(data['reviews'][0]['voted_up'])




    


# {
# "id": “your generated id”
# "author": “e605d04b-1b85-44f7-a693-ce0d87176512”,
# "date":”2020-01-01”,
# "hours":100,
# "content":”Lorem ipsum dolor sit amet”,
# "comments":4,
# "source":”steam”,
# "helpful":6,
# "funny":3,
# "recommended": True,
# "franchise":”A franchise name”,
# "gameName":”A game Name”
# }