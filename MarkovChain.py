#this program takes lists of sentences and uses them to generate new ones using a Markov chain sentence generator
#run this program on text files which have lines of sentences that start with two start keywords and end with an end keyword
#files created by TweetReformatter.py can be used with this program
import random, os

#specifies file names for the txt file to obtain data from and the txt file to write data to
input_txt_file = "reformatted_tweets.txt" #can edit
output_txt_file = "output.txt" #can edit

#specifies keywords which will start and end each line
start_keyword_A = "TWEETSTARTA" #can edit
start_keyword_B = "TWEETSTARTB" #can edit
end_keyword = "TWEETEND" #can edit

markov_chain = {} #dictionary to store Markov chain data
markov_output = [] #stores each list of words (sentence) outputted by Markov chain sentence generator
num_outputs = 100 #number of sentences to be generated
print_outputs = False #if True, outputs will be printed to console (better to leave as False for higher num_outputs)
write_outputs_to_file = True #if True, outputs will be written to sentence_txt_file

#yields word triplets from words, or stops the generator if words has no word triplets
def generate_word_triplets(words):
    if len(words) < 3:
        return
    for i in range(len(words) - 2):
        yield (words[i], words[i + 1], words[i + 2])

#if no output methods are set to True then the program doesn't run
if not print_outputs and not write_outputs_to_file:
    print("No output methods selected!")
else:
    if os.path.exists(os.path.join("reformatted_tweets", input_txt_file)):
        #opens file to obtain data from
        with open(os.path.join("reformatted_tweets", input_txt_file), "r") as data_file:
            for line in data_file.readlines():
                words = line.split()
                #generates word triplets from the words in each line of data_file
                for word_A, word_B, next_word in generate_word_triplets(words):
                    #use a tuple containing word_A and word_B as the key for markov_chain. check if the key already exists in markov_chain. if the key already exists, append next_word to the list of values associated with that key. if it doesn't, add the new key and value to markov_chain
                    if (word_A, word_B) in markov_chain:
                        markov_chain[(word_A, word_B)].append(next_word)
                    else:
                        markov_chain[(word_A, word_B)] = [next_word]

        if not os.path.exists("markov_output"):
            os.makedirs("markov_output")
        #opens file that sentences will be written to if write_outputs_to_file is True
        with open(os.path.join("markov_output", output_txt_file), "w") as output_file:
            #generate num_output sentences
            for i in range(num_outputs):
                #make the first key to be looked up in markov_chain (start_keyword_A, start_keyword_B) since that was the beginning of every line of input_txt_file
                word_A = start_keyword_A
                word_B = start_keyword_B
                while True:
                    #pick random words to continue the Markov-chain-generated sentence until end_keyword is reached, then break
                    word_A, word_B = word_B, random.choice(markov_chain[(word_A, word_B)])
                    if word_B == end_keyword:
                        break
                    markov_output.append(word_B)

                sentence = "" #string to store each sentence created by the Markov chain
                for j in range(len(markov_output)):
                    #add each word generated by the Markov chain to sentence
                    sentence += markov_output[j] + " "

                #print each generated sentence if print_outputs is True
                if(print_outputs):
                    print(str(i + 1) + ".) " + sentence[:-1])

                #writes each generated sentence to output_txt_file if write_outputs_to_file is True
                if(write_outputs_to_file):
                    output_file.write(str(i + 1) + ".) " + sentence[:-1] + "\n")

                markov_output.clear()

        if not print_outputs and write_outputs_to_file:
            print("Finished writing Markov-chain-generated sentences to " + output_txt_file + ".") #lets the user know that Markov chain generator has finished if the write-to-file option was selected and the print-outputs option wasn't
        elif not write_outputs_to_file:
            os.remove(os.path.join("markov_output", output_txt_file)) #deletes the empty output file that was created if the write-to-file option wasn't selected
    else:
        print("Reformatted file not found!")
        print("Run TweetReformatter.py to generate reformatted tweet files.")
