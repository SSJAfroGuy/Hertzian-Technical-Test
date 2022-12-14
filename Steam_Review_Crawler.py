import requests
import json
import uuid
import random
import urllib.parse

# Set variables for quick testing
# This will always be the default initial cursor - This could be passed as a default value for URL generation if none is set though? 
review_cursor = "*"
# This number is essentially the default unless the total number of reviews is already below 100. 100 is the maximum and lowers the total requests made so it's the most efficient number to use?
review_count = 100
# Used to count the total number of reviews that have been cralwed through. This allows an upper limit to be reached
review_iteration = 0

# Define random numbers to the ID variables 
rndid=random.Random()

# Grab values from the user for use in the review crawling - Needs data validation added at least. Add asking the user if they wish to filter reviews between 2 dates
def __get_input__():    
    appid     = input("Please enter the steam ID: ")
    gameName  = input("Please enter the game name: ")
    franchise = input("Please enter the franchise name: ")     
    source    = input("Please enter the source name: ")         
    return appid, gameName, franchise, source
user_input = __get_input__()
appid      = user_input[0]
gameName   = user_input[1]
franchise  = user_input[2]
source     = user_input[3]

# Function to ask the user for a start and end date (I guess use unix timestamp for the sake of testing, idk how else to input date time as a user with a terminal :eyes: something to look into)
# Sdate = input start date
# Edate = input end date

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
# First time calling the function also essentially sets the default values - there's a better way to do this when no value is passed - something to fix up
processed_url = __generate_url__(appid, "recent", "all", 365, review_cursor, "all", "all", review_count)

# Return the data in a readable JSON format from the URL generated 
def __generate_data__(processed_url):    
    response = requests.get(processed_url)
    data     = json.loads(response.text)
    return data
processed_data = __generate_data__(processed_url)

# Find the current total and set the max number of reviews to be 5000 (Could be a seperate variable?)
def __set_total_reviews__():
    print("Total number of reviews for the steam ID: ", processed_data['query_summary']['total_reviews'])
    total_reviews = processed_data['query_summary']['total_reviews']    
    if total_reviews > 5000:
        total_reviews = 5000
    return total_reviews
total_reviews = __set_total_reviews__()

# Update cursor to grab the next batch of reviews - Uses URL encoding to ensure characters are URL friendly
def __generate_cursor__(processed_data):    
    review_cursor = urllib.parse.quote(processed_data['cursor'])
    return review_cursor
# print("RCursor before = ",review_cursor)
review_cursor = __generate_cursor__(processed_data)
# print("RCursor after = ",review_cursor)

# Create a list which will store the data from each list. This will be used for the final output
full_review_list = []

# Create a list to store the currently processed reviews in
review_list = []

# Keep adding data to the list until the number of reviews processed equals the total reviews - This should be a function? I think 
while review_iteration != total_reviews:
    # initialise the currnet count for the number of reviews in the batch from the URL 
    review_num = 0
    for x in processed_data['reviews']:
        print("Current review num: ", review_num)
        print("Total review num: ", review_iteration)
        # print("Total review length: ", review_count)    
        id          = str(processed_data['reviews'][review_num]['author']['steamid']) + str(appid)
        author      = processed_data['reviews'][review_num]['author']['steamid']
        date        = processed_data['reviews'][review_num]['timestamp_created']
        hours       = processed_data['reviews'][review_num]['author']['playtime_forever']
        content     = processed_data['reviews'][review_num]['review']
        comments    = processed_data['reviews'][review_num]['comment_count']        
        helpful     = processed_data['reviews'][review_num]['votes_up']
        funny       = processed_data['reviews'][review_num]['votes_funny']
        recommended = processed_data['reviews'][review_num]['voted_up']
        # Generate the ID and Author values
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
            # 'review number': review_num,
            # 'cursor': review_cursor,
            'franchise': franchise,
            'gameName': gameName
            }
        review_num += 1     
        # Temp store to add to final output 
        review_list.append(review_item)    
        print("Current review length: ", len(review_list))
    
    # Count the number of total reviews grabbed - ensures that reviews that if for some reason less than 100 are grabbed, the literal number will be used instead of assuming
    review_iteration += len(processed_data['reviews'])
    print("The number of reviews is equal to: ", review_iteration)     
    
    # Check if the next batch could exceed the total number of reviews, and ensure the URL only grabs the remainder
    if review_iteration + 100 > total_reviews:
        review_count = total_reviews - review_iteration
        # print("This code has stopped more than the total reviews!")
                
    # Generate the new information using updated numbers 
    processed_url = __generate_url__(appid, "recent", "all", 365, review_cursor, "all", "all", review_count)
    print("url has been printed")
    
    processed_data =  __generate_data__(processed_url)
    print("data has been processed by the new URL")
    
    print("RCursor before = ",review_cursor)
    review_cursor = __generate_cursor__(processed_data)
    print("RCursor after = ",review_cursor)                  
          
# Final output will be from this
full_review_list.extend(review_list)
print("Full review length: ", len(full_review_list))

# Clear and write the full_review_list to the review file - Should be a function only called if there is data to store too
# If total reviews > 0 then run this function
with open(review_store, 'w') as f:
    json.dump(full_review_list, f, ensure_ascii=True, indent=2)

print("Your reviews have been processed, please check the:", review_store, "file") 