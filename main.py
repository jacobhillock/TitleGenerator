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

key_words  = []	# List of Key Words
idf_list   = []	# Will contain the IDF of each keyword
tf_list    = [] # Contains the number of times each keyword appears over the whole document
ntf_list   = []	# Contains the normalized term frequency of each keyword
score_list = [] # ntf_list * idf_list

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

#calculates the IDF of a word given the number of sentences it appears in 
def calc_idf(count):
    global num_of_sentences
    if count == 0:
        count = 1
        print("Potential error with idf. Found count to be 0, changing to 1...")
	
    idf = math.log((num_of_sentences/count), 2) + 1
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
        # Tracks if a word has appeared in a sentence at least once
        count = 0 
        # Tracks total number of occurences of word over all sentences
        glob_count = 0 
        for sent in sentences:
            # Get number of times key word appears in sentence
            temp = re.findall(key, sent)
            if len(temp) > 0:
                count += 1
                glob_count += len(temp)
        idf_list.append(calc_idf(count))
        tf_list.append(glob_count)

def calc_scores ():
    global idf_list
    global ntf_list
    global score_list

    for i, n in zip(idf_list, ntf_list):
        score_list.append(i*n)

def process_scores (max_score):
    global score_list
    for i in range(len(score_list)):
        if score_list[i] > max_score:
            score_list[i] = 0

def find_title (sentences, length):
    ps = PorterStemmer()
    global score_list
    high_score = -1
    high_score_title = []
    for sent in sentences:
        words = sent.split(' ')
        for i in range(len(words) - length):
            score = 0
            for w in words[i:i+length]:
                if w in key_words:
                    word_locatoin = key_words.index(ps.stem(w))
                    score += score_list[word_locatoin]
            if score > high_score:
                high_score = score
                high_score_title = words[i:i+length]
    return high_score, high_score_title

# main takes a keyword to use when scraping the wikipedia
def main(article, do_scrape, title_length, max_score):
    # -----------------------------------------------------------
    # Load document into memport
    # -----------------------------------------------------------
    article = article.replace(' ', '_')

    # perform some scraping from wikipedia using the keyword passed
    if do_scrape:
        article = scrape(url='https://en.wikipedia.org/wiki/'+article)
    file_name = f'scrapes/{article}'
    
    # Load file, and store content
    text = ''
    with open(file_name) as file:
        doc = file.read()
        text = doc.replace('\n', ' ')
    

    # -----------------------------------------------------------
    # Document processing
    # -----------------------------------------------------------
    # make everything lowercase
    test_mod = text.lower()
    # Splits sentences (assuming all sentences end with a '. ')
    sentences = test_mod.split('. ')

    # Stem words, remove stop words, and collect wordlist
    stop = set(stopwords.words('english'))
    ps = PorterStemmer()
    global key_words
    global num_of_sentences
    
    for i in range(len(sentences)):
        # remove punctuation (link 1)
        sentences[i] = sentences[i].translate(str.maketrans('', '', string.punctuation))
        # remove stopwords
        sentences[i] = [w for w in sentences[i].split(" ") if w not in stop]
        temp = ''
        
        # reconstruct sentence
        for j in range(len(sentences[i])):
            w = ps.stem(sentences[i][j])
            # w = sentences[i][j]
            if len(w) > 1:
                key_words.append(w)
            temp += w + ' '
        
        # put sentence back in string form
        sentences[i] = temp
    
    # remove duplicate words and empty string
    key_words = list(set(key_words))
    if '' in key_words:
        key_words.remove('')
	
    # fill in remaining global variables
    num_of_sentences = len(sentences)
    prep_idf_tf(sentences)
    calc_ntf()
    calc_scores()
    if max_score != 'N':
        process_scores(float(max_score))

    # -----------------------------------------------------------
    # Title generation
    # -----------------------------------------------------------
    # makes text lowercase, removes punctuation from text, and splits it into sentences again
    sentences_raw = text.lower()
    sentences_raw = sentences_raw.split('. ')
    for i in range(len(sentences_raw)):
        sentences_raw[i] = sentences_raw[i].translate(str.maketrans('', '', string.punctuation))
    
    if title_length[0] != 'A':
        # initialize high_score
        high_score, high_score_title = find_title(sentences_raw, int(title_length))
        
        print(high_score)
        print(high_score_title)
    
    else:
        scores_title = {}
        titles       = {}
        for i in range(int(title_length[1:]),11):
            scores_title[i], titles[i] = find_title(sentences_raw, i)
        
        best_score_word = -1
        best_length = 0
        for k in sorted(titles.keys()):
            if (s:=(scores_title[k] / (k+1))) > best_score_word:
                best_length = k
                best_score_word = s
        
        print(scores_title[best_length])
        print(titles[best_length])





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--article', default='Artificial_Intelligence',
                        help='Wikipedia article to scrape and title [default: Aritificial Intelligence]')
    parser.add_argument('--doc', default='',
                        help='Document to title [default: \'\']')
    parser.add_argument('--length', default='A1',
                        help='Length of the title; integer is hard length, add \'A\' to front of integer for minimum length [default: A1]')
    parser.add_argument('--maxScore', default='N',
                        help='Max word score; N for no max [default: N]')

    FLAGS = parser.parse_args()

    # lets capture the keyword to scrape from wikipedia
    article = FLAGS.article
    doc = FLAGS.doc
    if doc == '':
        main(article, True, FLAGS.length, FLAGS.maxScore)
    else:
        main(doc, False, FLAGS.length, FLAGS.maxScore)
