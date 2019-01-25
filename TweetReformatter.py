#raw_tweets.json obtained from http://trumptwitterarchive.com/archive on 10/5/18 at 2:40PM PST
import json, os

#specifies file names for json source file and txt file that tweets will be written to
input_json_file = "raw_tweets.json" #can edit
output_txt_file = "reformatted_tweets.txt" #can edit

#specifies keywords which will start and end each tweet
start_keyword_A = "TWEETSTARTA" #can edit
start_keyword_B = "TWEETSTARTB" #can edit
end_keyword = "TWEETEND" #can edit
if not os.path.exists("raw_tweets"):
    os.makedirs("raw_tweets")
print("Extracting tweets from " + input_json_file + "...")
if os.path.exists(os.path.join("raw_tweets", input_json_file)):
    #opens file to read raw tweets from
    with open(os.path.join("raw_tweets", input_json_file), encoding="utf8", errors="ignore") as file:
        tweets = json.load(file) #loads input_json_file into a dictionary

    print("Loading tweets into " + output_txt_file + "...")
    if not os.path.exists("reformatted_tweets"):
        os.makedirs("reformatted_tweets")
    #opens file to write reformatted tweets to
    with open(os.path.join("reformatted_tweets", output_txt_file), "w") as output_file:
        #loops through all tweets and adds the non-retweets to output_file
        for tweet in tweets:
            if not tweet["is_retweet"]:
                tweet["text"] = start_keyword_A + " " + start_keyword_B + " " + tweet["text"] + " " + end_keyword #adds markers for the start and end of each tweet

                #adds each word in the tweet to words, while removing all hashtags, urls, newline characters, etc.
                words = ("".join(ch for ch in word if ch.isalnum() or ch == "/" or ch == "%") for word in tweet["text"].split() if word[0] != "#" and not "@" in word and not (len(word) > 3 and ("http:" in word or "https:" in word)) and len("".join(ch for ch in word if ch.isalnum())) != 0) #note: the '&' symbol gets read as &amp and written as amp

                tweet_output = "" #string to store the modified tweet without all the hashtags, etc.
                word_count = 0 #counts the number of words in the modified tweet
                for word in words:
                    tweet_output += str(word) + " "
                    word_count += 1
                #if the modified tweet contains only the 2 start keywords and 1 end keyword (empty tweet) then don't write it to output_file
                if(word_count > 3):
                    output_file.write(tweet_output[:-1] + "\n") #write the modified tweet to output_file

    print("Done.") #lets the user know that the program has finished running
else:
    #lets the user know that the file was not found
    print("Specified file not found in raw_tweets folder.")
    print("Exiting.")
