import requests
import json
import uuid
import random
import urllib.parse

# Set variables for quick testing
review_cursor = "*"
review_num = 0
review_count = 100

# Define random numbers to the ID variables 
rnduuid=random.Random()
rndid=random.Random()

# Get the app id from user input (Currently a static value for tests)
def __get_app_id__():    
    appid = 1382330 #input("Please enter the steam ID: ")
    return appid
appid = __get_app_id__()

# Generate the name of the output file (static value for now)
def __name_review_file__():
    review_store = "Processed_Reviews.txt"
    return review_store

review_store = __name_review_file__()

# Randomise function for the ID and UUID generation, ensures the same seed is easily replicable so the ID values can be the same with the same input
def __randomise_id__(id):
    rndid.seed(int(id))
    rnd = uuid.UUID(int=rndid.getrandbits(128), version=4)
    return rnd

# Generate the url to the steam API
def __generate_url__(appid, filter, language, day_range, cursor, review_type, purchase_type, num_per_page):
    url = f'https://store.steampowered.com/appreviews/{appid}?json=1&filter={filter}&language={language}&day_range={day_range}&cursor={cursor}&review_type={review_type}&purchase_type={purchase_type}&num_per_page={num_per_page}'
    print(url)
    return url

# Return the data in a readable JSON format from the URL generated 
def __generate_data__():
    processed_url = __generate_url__(appid, "all", "english", 365, review_cursor, "all", "all", review_count)
    response = requests.get(processed_url)
    data = json.loads(response.text)
    return data

processed_data = __generate_data__()

# Update cursor to grab the next batch of reviews - Uses URL encoding to ensure characters are URL friendly
def __generate_cursor__():    
    review_cursor = urllib.parse.quote(processed_data['cursor'])
    return review_cursor

# Create a list which will store the data from each list. This will be the output
full_review_list = []

# Create a list to store the currently processed reviews in
review_list = []

# ID generation uses the author ID with the Game ID appended on as the seed
# Iterate based on total number of reviews grabbed (this might fail with less than 100 reviews total rip lol)
# Add a check for the literal grabbed number of reviews to fix the above error
while review_count > review_num:
    print("Current review num: ", review_num)
    print("Total review length: ", review_count)    
    id          = str(processed_data['reviews'][review_num]['author']['steamid']) + str(appid)
    author      = processed_data['reviews'][review_num]['author']['steamid']
    date        = processed_data['reviews'][review_num]['timestamp_created']
    hours       = processed_data['reviews'][review_num]['author']['playtime_forever']
    content     = processed_data['reviews'][review_num]['review']
    comments    = processed_data['reviews'][review_num]['comment_count']
    source      = processed_data['reviews'][review_num]['steam_purchase']
    helpful     = processed_data['reviews'][review_num]['votes_up']
    funny       = processed_data['reviews'][review_num]['votes_funny']
    recommended = processed_data['reviews'][review_num]['voted_up']
    id_str   = str((__randomise_id__(id)))
    uuid_str = str((__randomise_id__(author)))
    review_num += 1
    # print(review_num)
    # print(review_cursor)    

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
        # 'franchise': franchise,
        # 'gameName': gameName
        }

    # Temp store to add to final output 
    review_list.append(review_item)    
    print("Current review length: ", len(review_list))
        
# Final output will be from this
full_review_list.extend(review_list)
print("Full review length: ", len(full_review_list))

# Clear and write the full_review_list to the review file
with open(review_store, 'w') as f:
    json.dump(full_review_list, f, ensure_ascii=True, indent=2)


# EVERYTHING BELOW IS TO TEST IN TERMINAL. 
# --------------------------------------------
# print("First batch of reviews")
# print(review_id)
# print(processed_data['reviews'][0]['author']['steamid'])
# print(processed_data['reviews'][0]['timestamp_created'])
# print(processed_data['reviews'][0]['author']['playtime_forever'])
# print(processed_data['reviews'][0]['review'])
# print(processed_data['reviews'][0]['comment_count'])
# print(processed_data['reviews'][0]['votes_up'])
# print(processed_data['reviews'][0]['votes_funny'])
# print(processed_data['reviews'][0]['voted_up'])
# print(processed_data['cursor'])

# processed_data = __generate_data__()

# print("Second batch of reviews")
# print(review_id)
# print(processed_data['reviews'][0]['author']['steamid'])
# print(processed_data['reviews'][0]['timestamp_created'])
# print(processed_data['reviews'][0]['author']['playtime_forever'])
# print(processed_data['reviews'][0]['review'])
# print(processed_data['reviews'][0]['comment_count'])
# print(processed_data['reviews'][0]['votes_up'])
# print(processed_data['reviews'][0]['votes_funny'])
# print(processed_data['reviews'][0]['voted_up'])
# print(processed_data['cursor'])
