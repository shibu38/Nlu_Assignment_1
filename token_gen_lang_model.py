from nltk.corpus import gutenberg
from nltk.corpus import brown
import collections
import random
import time
import warnings
warnings.filterwarnings("ignore")

def remove_punctuation(words):
    punc = [',', '\'', '?', '.', '\"', ':', '\/', '\\', ';', '[', ']', '{', '}', '(', ')', '#', '$', '--', '``', '\'\'',
            '.--', '*--', '-']
    l=list()
    for word in words:
        if word not in punc:
            l.append(word)
    return l

def training(corpus):
    unigram_list=collections.defaultdict(list)
    bigram_list=collections.defaultdict(list)
    trigram_list=collections.defaultdict(list)
    for sentences in corpus:
        words=remove_punctuation(sentences)
        words=['*','*','*']+words+['\STOP']


        for index,token in enumerate(words):
            if(index>=2 and index<len(words)-2):
                unigram=tuple([words[index]])
                unigram_list[unigram].append(words[index+1])

            if(index>=1 and index<len(words)-3):
                bigram=tuple([words[index],words[index+1]])
                bigram_list[bigram].append(words[index+2])


    return dict(unigram_list),dict(bigram_list)


def generate_trigram_token(bigram_list):
    keys=list(bigram_list.keys())
    text=list()
    first=random.choice(keys)
    text.append(first[0])
    text.append(first[1])
    i=2
    while (i != 10):
        s = bigram_list.get(tuple([text[len(text) - 2],text[len(text)-1]]),[])
        if (len(s) == 0):
            i+=1
            continue
        t = random.choice(s)
        #print(t)
        text.append(t)
        i += 1
    s=''
    for i in range(len(text)):
        s+=text[i]+' '

    if(len(text)!=10):
        return False,s
    else:
        return True,s

if __name__=='__main__':
    time.clock()

    print()

    brown_corpus=list(brown.sents(brown.fileids()))
    for i in range(len(brown_corpus)):
        brown_corpus[i]=list(map(lambda x:x.lower(),brown_corpus[i]))
    gutenberg_corpus = list(gutenberg.sents(gutenberg.fileids()))
    for i in range(len(gutenberg_corpus)):
        gutenberg_corpus[i] = list(map(lambda x: x.lower(), gutenberg_corpus[i]))
    combined_corpus=brown_corpus+gutenberg_corpus

    unigram_list, bigram_list= training(combined_corpus)
    i=0
    while(i<1):
        bool,s=generate_trigram_token(bigram_list)
        if(bool):
            i+=1
            print(s)

    print()
    print('Total time taken', str(time.clock()))