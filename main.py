# links:
# https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
# https://stackoverflow.com/questions/19130512/stopword-removal-with-nltk


# Programmed by Jacob Hillock, Tangeni Shikomba, and Chisulo Mukabe
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string


def main():

    file_name = 'scrapes/Python_(programming_language).txt'
    title, text = '', ''
    ps = PorterStemmer()
    with open(file_name) as file:
        doc = file.read()
        data = doc.split('\n\n')
        data[1] = data[1].replace('\n', ' ')
        # print(data)
        title = data[0]
        text = data[1]
    
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

    


if __name__ == '__main__':
    main()