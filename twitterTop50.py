import csv
import json
import editdistance
from nltk.tokenize import RegexpTokenizer
import os

rootdir = '/home/saad/Desktop/top_50_datasets'

data = {}

# Iterate over all subdirectories in this folder
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if(file=="tweets.csv"):
            tk = RegexpTokenizer('\#\w*') # Segregate all hashtags from text
            with open(os.path.join(subdir, file)) as input:
                try:
                    csv_reader = csv.DictReader(input)
                    for i in csv_reader:   # Input format is csv as received from twitter API
                        id = i['Tweet Id']  # Storing tweets in JSON against tweet IDs
                        id = id.replace('"','')
                        text = i["Tweet Content"]
                        tokenized = tk.tokenize(text)
                        tokenized = [j.lower() for j in tokenized]    # converting all hashtags to .lower() to prevent false negatives
                        if('#metoo' in tokenized):    # Searching for all #metoo hashtags
                            print("exact match found for metoo!")
                            data[id] = i
                        else:
                            check_add = False
                            for word in tokenized:
                                if(editdistance.eval('#metoo', word)<=2):   # Allowing difference upto 1 edit distance from #metoo
                                    check_add = True
                                    print("edit distance <= 1 found")
                            if(check_add==True):
                                print("adding tweet with edit dist <= 1")   # If such a tweet is found add to dictionary
                                data[id] = i
                            check_add = False
                except:
                    print("wrong data!")

json_obj = json.dumps(data)    # Converting Dictionary to JSON

with open('/home/saad/Desktop/twitterTop50CovidTweets.json', "w") as output:
    output.write(json_obj)