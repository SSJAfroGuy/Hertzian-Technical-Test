import requests
import json
import uuid
import random
import urllib.parse
import time

# Set variables for quick testing
review_cursor = "*"
# Review count should be definied by the user and done inside a function? This means changing the division number for the total number of 100 iterations as it'll no longer be 100
review_count = 100
review_num = 0
review_iteration = 0

# Define random numbers to the ID variables 
rnduuid=random.Random()
rndid=random.Random()

# Get the app id from user input (Currently a static value for tests)
def __get_app_id__():    
    appid = 1382330 #input("Please enter the steam ID: ")
    return appid
appid = __get_app_id__()

# Generate the name of the output file - This will contain the app ID (consider date/time and/or game name etc etc.)
def __name_review_file__():
    review_store = f'Processed_Reviews_ID{appid}.txt'
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
processed_url = __generate_url__(appid, "all", "english", 365, review_cursor, "all", "all", review_count)

# Return the data in a readable JSON format from the URL generated 
def __generate_data__(processed_url):    
    response = requests.get(processed_url)
    data = json.loads(response.text)
    return data
processed_data = __generate_data__(processed_url)

print("Total number of reviews for the steam ID: ", processed_data['query_summary']['total_reviews'])
total_reviews = processed_data['query_summary']['total_reviews']

# Check the total number of reviews for the game
# If this number is > 5000, limit the number to 5000
# If the number is < 5000. Divide it by 100 (Max number of reviews in a single request) and iterate by the resulting integer.
# The number after the decimal is equal to the number of reviews reamaining for the final crawl

def __calculate_iterations__():
    # this code checks the total reviews and prevents more than 5000 responses being retreived 50 * 100 = 5000
    # if total_reviews >= 5000:
    #     return 50, 0
    # else:
        # This is the number of times the 100 reviews will be grabbed
        iterations = total_reviews // 100
        # This is the single number of reviews that needs to be grabbed after the batches of 100
        leftover_iterations = total_reviews % 100
        return iterations, leftover_iterations

crawl_number =__calculate_iterations__()
print("the total number we will crawl by is: ", crawl_number)

# Update cursor to grab the next batch of reviews - Uses URL encoding to ensure characters are URL friendly
def __generate_cursor__(processed_data):    
    review_cursor = urllib.parse.quote(processed_data['cursor'])
    return review_cursor
print("RCursor before = ",review_cursor)
review_cursor = __generate_cursor__(processed_data)
print("RCursor after = ",review_cursor)

# Create a list which will store the data from each list. This will be the output
full_review_list = []

# Create a list to store the currently processed reviews in
review_list = []

# ID generation uses the author ID with the Game ID appended on as the seed

def __crawl_reviews__(full_requests, leftover_requests, processed_data, review_count, review_num, review_cursor):    
    while full_requests >= 1:
        print("Full requests is equal to: ", full_requests)
        processed_url = __generate_url__(appid, "all", "english", 365, review_cursor, "all", "all", review_count)        
        
        processed_data = __generate_data__()
        print("Processing data")
        review_cursor = __generate_cursor__()
        print(review_cursor)
        full_requests -=1
        
    if leftover_requests > 0 & full_requests == 0:
        print("leftover requests is equal to: ", leftover_requests)
        review_cursor = __generate_cursor__()
        # Set the review count to the remainder. This will complete the last batch of reviews falling below the 100 per page standard set before
        review_count = leftover_requests
        processed_url = __generate_url__(appid, "all", "english", 365, review_cursor, "all", "all", review_count)        
        # Create the new data based off the new number per page value
        # processed_data = __generate_data__()
        
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
    return
# __crawl_reviews__(*crawl_number, processed_data, review_count, review_num, review_cursor)        

def __crawl_test__(full_requests, leftover_requests, processed_data, review_count, review_num, review_cursor):    
    while full_requests >= 1:
        for x in processed_data['reviews']:
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
                'review number': review_num
                # 'franchise': franchise,
                # 'gameName': gameName
                }

            # Temp store to add to final output 
            review_list.append(review_item)    
            print("Current review length: ", len(review_list))    
    # Final output will be from this
    full_review_list.extend(review_list)
    print("Full review length: ", len(full_review_list))
    full_requests -=1
    processed_url = __generate_url__(appid, "all", "english", 365, review_cursor, "all", "all", review_count)        
    processed_data =  __generate_data__(processed_url)
    review_curosr = __generate_cursor__(processed_data)        
# __crawl_test__(*crawl_number, processed_data, review_count, review_num, review_cursor) 

# Set the number of full (100) review iterations
full_iterations = crawl_number[0]

number_reviews_grabbed = processed_data['reviews']
print("There are: ", len(number_reviews_grabbed), " in this batch")

# if total reviews > 5000 total reviews = 5000

# whlie review iteration is NOT equal to total reviews 
# Run this code
#     for x in processed data 
#         Create a single batch of reviews        
#     Add the number of reviews in the batch to the review iteration
#     check review iteration against total reviews and generate URL - data - cursor accordingly

# Set the max number of reviews to be 5000 (Could be a seperate variable?)
if total_reviews > 5000:
    total_reviews = 5000

while review_iteration != total_reviews:
    
    for x in processed_data['reviews']:
        print("Current review num: ", review_num)      
        # print("Total review length: ", review_count)    
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
            'review number': review_num
            # 'franchise': franchise,
            # 'gameName': gameName
            }
        review_num += 1     
        # Temp store to add to final output 
        review_list.append(review_item)    
        print("Current review length: ", len(review_list))
    
    # Count the number of total reviews grabbed (Won't always be equal to the review_num variable because steam)
    review_iteration += len(processed_data['reviews'])
    print("The number of reviews is equal to: ", review_iteration)     
    # Initialise the review num count to go through a new list 
    review_num = 0
    # Wait 5 seconds - this made no difference for the reviews grabbed, keeping as a safety feature possibly? tbf I am not patient enough to test this :D Nor smart enough to try catch or whatever you'd do instead
    # time.sleep(5)
    
    if review_iteration + 100 > total_reviews:
        review_count = total_reviews - review_iteration
        print("This code has stopped more than the total reviews!")
        
        
    # Generate the new information using updated numbers 
    processed_url = __generate_url__(appid, "all", "english", 365, review_cursor, "all", "all", review_count)        
    processed_data =  __generate_data__(processed_url)
    print("RCursor before = ",review_cursor)
    review_cursor = __generate_cursor__(processed_data)
    print("RCursor after = ",review_cursor)          
        


# while total_reviews >= 1:
    
#     for x in processed_data['reviews']:
#         print("Current review num: ", review_num)      
#         print("Total review length: ", review_count)    
#         id          = str(processed_data['reviews'][review_num]['author']['steamid']) + str(appid)
#         author      = processed_data['reviews'][review_num]['author']['steamid']
#         date        = processed_data['reviews'][review_num]['timestamp_created']
#         hours       = processed_data['reviews'][review_num]['author']['playtime_forever']
#         content     = processed_data['reviews'][review_num]['review']
#         comments    = processed_data['reviews'][review_num]['comment_count']
#         source      = processed_data['reviews'][review_num]['steam_purchase']
#         helpful     = processed_data['reviews'][review_num]['votes_up']
#         funny       = processed_data['reviews'][review_num]['votes_funny']
#         recommended = processed_data['reviews'][review_num]['voted_up']
#         id_str   = str((__randomise_id__(id)))
#         uuid_str = str((__randomise_id__(author)))       
#     # Create an easy to read layout with the values
#         review_item = {
#             'id': id_str,
#             'author-UUID': uuid_str,
#             'date': date,
#             'hours': hours,
#             'content': content,
#             'comments': comments,
#             'source': source,
#             'helpful': helpful,
#             'funny': funny,
#             'recommended': recommended,
#             'review number': review_num
#             # 'franchise': franchise,
#             # 'gameName': gameName
#             }
#         review_num += 1     
#         # Temp store to add to final output 
#         review_list.append(review_item)    
#         print("Current review length: ", len(review_list))
    
#     review_iteration -= number_reviews_grabbed
#     full_iterations -=1        
#     review_num = 0
#     time.sleep(5)
#     processed_url = __generate_url__(appid, "all", "english", 365, review_cursor, "all", "all", review_count)        
#     processed_data =  __generate_data__(processed_url)
#     print("RCursor before = ",review_cursor)
#     review_cursor = __generate_cursor__(processed_data)
#     print("RCursor after = ",review_cursor)      

          
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
