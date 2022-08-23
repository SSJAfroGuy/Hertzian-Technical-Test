import requests
import json
import uuid
import random

# Ask user to input the ID of their game - P5S:1382330
appid = input("Please enter the steam ID: ")
franchise = input("Please enter the franchise of your game: ")
gameName = input("Please enter the name of your game: ")
# review_type = input("Would you like your results sorted by date? (Y/N)")

# Use https://partner.steamgames.com/doc/webapi/ISteamApps to gather full list of steam apps and use that as a reference to know if the entered ID is valid
# That would also allow the franchise and name of the game to be passed through - user confirmation
# Could allow game name entry instead of ID too for ease of use
# Couldn't I just donwload that once, have it as a text file and have an option to update it if it's out of date, whilst not relying on waitinf for the 100k+ steam apps to be loaded into a text file each time :v

review_cursor = "*"
rnduuid=random.Random()
rndid=random.Random()
review_num = 0
# Clear text file upon run - redundant as this happens at the end - but was kept in for the sake of testing
review_store = "Processed_Reviews.txt"
open(review_store, 'w').close()

# Randomise function for the ID and UUID generation, ensures the same seed is easily replicable so the ID values can be the same with the same input
def __randomise_id__(id):
    rndid.seed(int(id))
    rnd = uuid.UUID(int=rndid.getrandbits(128), version=4)
    return rnd

# request GET from the given url, passes through user input for appid
def __generate_url__(cursor):
    url = f'https://store.steampowered.com/appreviews/{appid}?json=1'
    print(url)
    return url

# Return the data in a readable JSON format from the URL generated 
def __generate_data__():
    processed_url = __generate_url__(review_cursor)
    response = requests.get(processed_url)
    data = json.loads(response.text)
    return data


processed_data = __generate_data__()

#placeholder id generation - This became un-placeholder, steamid + appid strings added together to generate unique number
review_id = str(processed_data['reviews'][0]['author']['steamid']) + str(appid)

# I didn't understand what "source" was supposed to be at first and didn't realise it was passed through by the user? In theory all of these reviews will be "steam" hindsight op
if (processed_data['reviews'][0]['steam_purchase']) == True:
    review_source = "steam"
else:
    review_source = "other"

# Here for seeing results in terminal
# print(review_id)
# print(processed_data['reviews'][0]['author']['steamid'])
# print(processed_data['reviews'][0]['timestamp_created'])
# print(processed_data['reviews'][0]['author']['playtime_forever'])
# print(processed_data['reviews'][0]['review'])
# print(processed_data['reviews'][0]['comment_count'])
# print(review_source)
# print(processed_data['reviews'][0]['votes_up'])
# print(processed_data['reviews'][0]['votes_funny'])
# print(processed_data['reviews'][0]['voted_up'])
# print(franchise)
# print(gameName)
# print(processed_data['cursor'])

full_review_list = []
# This part should be itterated up to 5000 times - Check the total number of reviews first, if > 5000, limit it to 5000. if < 5000, then only go up to the returned total review number
# Each iteration passes the newly generated cursor value into my generate_url function


# Create a list, and iterate through it for the processed data to add each value - This is how the info I want is extracted and the parts that aren't required get left out 
review_list = []

for review in processed_data:
    id          = review_id
    author      = processed_data['reviews'][review_num]['author']['steamid']
    date        = processed_data['reviews'][review_num]['timestamp_created']
    hours       = processed_data['reviews'][review_num]['author']['playtime_forever']
    content     = processed_data['reviews'][review_num]['review']
    comments    = processed_data['reviews'][review_num]['comment_count']
    source      = review_source
    helpful     = processed_data['reviews'][review_num]['votes_up']
    funny       = processed_data['reviews'][review_num]['votes_funny']
    recommended = processed_data['reviews'][review_num]['voted_up']
    uuid_str = str((__randomise_id__(author)))
    id_str   = str((__randomise_id__(id)))
    review_num += 1

# Create an easy to read layout with the values
    review_item = {
        'id': id_str,
        'author-UUID': uuid_str,
        'date': date,
        'hours': hours,
        'content': content,
        'comments': comments,
        'source': source,
        'helpful': helpful,
        'funny': funny,
        'recommended': recommended,
        'franchise': franchise,
        'gameName': gameName
        }

    review_list.append(review_item)

full_review_list.append(review_list)

# Clear and write the review_list to the review file
with open(review_store, 'w') as f:
    json.dump(review_list, f, ensure_ascii=True, indent=2)