from pymongo import MongoClient
from selenium import webdriver
import time
from datetime import datetime, timedelta

# Replace 'your_remote_host' and 'your_remote_port' with your MongoDB server's information
remote_host = '127.0.0.1'
remote_port = 27017
#https://github.com/mozilla/geckodriver/releases

while True:
    try:
        # Connect to MongoDB
        client = MongoClient(remote_host, remote_port)

        # Access the "music" database
        db = client['music']

        # Access the "URL" collection
        collection = db['url']

        # Query all entries where the "url" field has data
        entries = collection.find({}).sort("added_date")
        # Check if there are any entries
        entries_list = list()
        #for entry in entries_list:
        #    print(entry)
        #print(len(list(entries_list)))
        if len(list(entries_list)) == 0:
            print("No entries found. Sleeping for 5 seconds...")
            time.sleep(5)
            continue

        # Loop through entries
        for entry in entries_list:

            url = entry.get("url")
            video_length = entry.get("length", 60)  # use "length" field for video length, default to 60 seconds if not available
            entry_id = entry.get("_id")
            print(f"found entry {url} with length {video_length} ... opening in browser now.")
            # Open the URL in Chrome
            driver = webdriver.Firefox()
            driver.get(url)
            current_time = datetime.now()
            delay = 10
            finish_time = current_time + timedelta(seconds=video_length + delay)
            print(f"opened in browser sleeping for {video_length} seconds and will finish at {finish_time}")
            # Wait until the video is done
            time.sleep(video_length + delay)
            driver.quit()
            # Remove the entry from MongoDB using the entry _id
            collection.delete_one({"_id": entry_id})

    except Exception as e:
        print(f"Error: {e}")
        # Add any necessary error handling or logging here
        print(f"sleeping for 5")
        time.sleep(5)  # Sleep for 5 seconds before trying to connect again