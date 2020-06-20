import csv
import json
from nltk.tokenize import RegexpTokenizer

data = {}   # Stores all tweet data

tk = RegexpTokenizer('\#\w*')   # Segregates all hashtags from the text using regex pattern matching
with open('/home/saad/Desktop/COVID.csv') as input:
    csv_reader = csv.DictReader(input)    # Iterate over all tweets
    for i in csv_reader:
        id = i['ID']     # Tweet ID
        id = id.replace('"','')
        text = i["Tweet_Content"]   # Tweet text 
        tokenized = tk.tokenize(text)
        tokenized = [j.lower() for j in tokenized]   # converting to lower to prevent False negatives based on case
        print(tokenized)
        if('#coronavirus' in tokenized):   # select only those tweets having #coronavirus
            data[id] = i

json_obj = json.dumps(data)   # Convert dictionaery to json

with open('/home/saad/Desktop/twitterCovidTweets.json', "w") as output:
    output.write(json_obj)

