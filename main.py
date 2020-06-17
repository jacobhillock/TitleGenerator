# links:
# https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
# https://stackoverflow.com/questions/19130512/stopword-removal-with-nltk


# Programmed by Jacob Hillock, Tangeni Shikomba, and Chisulo Mukabe
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import re
import math
import argparse
from wikipedia_scrape import scrape

num_of_sentences = 0 #Number of sentences in the document

key_words=[]	#List of Key Words
idf_list =[]	#Will contain the IDF of each keyword
tf_list =[]		#Contains the number of times each keyword appears over the whole document
ntf_list =[]	#Contains the normalized term frequency of each keyword

#Displays key words
def display_keywords():
    global key_words

    print()
    print("Key Words: ")

    for word in key_words:
        print(word)

    print("Total keywords: ", len(key_words))

def display_idf():
    global idf_list	
    print("IDF List: ", idf_list)

def display_ntf():
    global tf_list
    global ntf_list

    print("NTF Global: ", tf_list)
    print()
    print("NTF Normal: ", ntf_list)
    print()

#Extracts keywords from a given sentence list
def extract_keywords(sentences):
    global key_words
    repeat = False

    for sent in sentences:
        words = sent.split(" ")
        for w in words:
            if w.lower() not in key_words and w is not "":
                key_words.append(w.lower())

#calculates the IDF of a word given the number of sentences it appears in 
def calc_idf(count):
    global num_of_sentences
    if count == 0:
        count = 1
        print("Potential error with idf. Found count to be 0, changing to 1...")
	
    idf = math.log((num_of_sentences/count), 2) +1
    #print ("IDF: " + str(idf))

    return idf	

def calc_ntf():
    global tf_list
    global ntf_list

    max_val = max(tf_list)
    if max_val == 0:
        max_val = 1
        print("Potential error with ntf. Found max value to be 0, changing to 1.")

    for i in tf_list:
        ntf_list.append(i/max_val)
	
    #print("Global/Normal Length: ", len(tf_list), len(ntf_list))

#prep_idf_tf counts the frequency of the words both per sentence and over the entire document
def prep_idf_tf(sentences):
    global key_words
    global idf_list
    global tf_list

    for key in key_words:
        count = 0 #Tracks if a word has appeared in a sentence does not count multiple occurrences
        glob_count = 0 #tracks total number of occurences of word over all sentences
        for sent in sentences:
            temp = re.findall(key, sent.lower()) #Get number of times key word appears in sentence
            if len(temp) > 0:
                count +=1
                glob_count += len(temp)
        #print(key + ": ", count)		
        idf_list.append(calc_idf(count))
        tf_list.append(glob_count)


# main takes a keyword to use when scraping the wikipedia
def main(article):

    article = article.replace(' ', '_')

    # perform some scraping from wikipedia using the keyword passed
    scrape(url='https://en.wikipedia.org/wiki/'+article)

    file_name = 'scrapes/'+article+'.txt'
    title, text = '', ''
    ps = PorterStemmer()
    with open(file_name) as file:
        doc = file.read()
        print(doc)
        data = doc.split('\n\n')
        # print(data)
        data[0] = data[0].replace('\n', ' ')
        # print(data)
        text = data[0]
    
    test_mod = text.lower()
    sentences = test_mod.split('. ')

    # python stopwords (link 2)
    stop = set(stopwords.words('english'))
    word_list = set()
    for i in range(len(sentences)):
        # remove punctuation (link 1)
        sentences[i] = sentences[i].translate(str.maketrans('', '', string.punctuation))
        sentences[i] = [w for w in sentences[i].split(" ") if w not in stop]
        temp = ''
        for j in range(len(sentences[i])):
            w = ps.stem(sentences[i][j])
            # w = sentences[i][j]
            word_list.add(w)
            temp += w + ' '
        sentences[i] = temp
    word_list = list(word_list)

    for s in sentences:
        print(s)
    
    print(len(word_list))
	
    global num_of_sentences
    num_of_sentences = len(sentences)
    extract_keywords(sentences)
    #display_keywords() 
    prep_idf_tf(sentences)
    #display_idf()
    calc_ntf() #calculates NTF values of the keywords
    #display_ntf()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--article', default='Artificial_Intelligence',
                        help='Keyword to scrape [default: Aritificial Intelligence]')

    FLAGS = parser.parse_args()

    # lets capture the keyword to scrape from wikipedia
    article = FLAGS.article

    main(article)
