from nltk.corpus import gutenberg
from nltk.corpus import brown
import collections
import math
import time
from sklearn.cross_validation import train_test_split
import warnings
warnings.filterwarnings("ignore")

def calculate_probability(corpus):
    vocabulary = set()
    unigram_probability = collections.defaultdict(int)
    bigram_probability = collections.defaultdict(int)

    for sentences in corpus:
        words = sentences
        words = ['*'] + words + ['Stop']
        for index, token in enumerate(words):
            if (index >= 1 and index < len(words)):
                vocabulary.add(token)
                unigram_tuple = tuple([token])
                unigram_probability[unigram_tuple] += 1

            if (index >= 1 and index < len(words) - 1):
                bigram_tuple = tuple([token, words[index + 1]])
                bigram_probability[bigram_tuple] += 1

    # Calculating Probabilities for bigrams
    for bigram in bigram_probability:
        if (bigram[0] == '*'):
            bigram_probability[bigram] = math.log(float(bigram_probability[bigram] / len(corpus)), 2)
        else:
            uni = tuple([bigram[0]])
            bigram_probability[bigram] = math.log(float(bigram_probability[bigram] / unigram_probability[uni]), 2)

    # Calculating Probabilities for unigrams
    total = 0
    for unigram in unigram_probability:
        total += unigram_probability[unigram]
    for unigram in unigram_probability:
        unigram_probability[unigram] = math.log(float(unigram_probability[unigram] / total), 2)

    return dict(unigram_probability), dict(bigram_probability), total

def perpexility_backoff(test_data,bigram_probability,unigram_probability,total_words):
    total=0
    prob=0
    for sentences in test_data:
        words=sentences
        words = ['*'] + words + ['Stop']
        total+=len(words)
        for index,token in enumerate(words):
            if(index<len(words)-1):
                bigram=tuple([token,words[index+1]])
                q=bigram_probability.get(bigram,-100)
                if(q==-100):
                    unigram=tuple([token])
                    p=unigram_probability.get(unigram,-100)
                    if p==-100:
                        prob+=math.log(1/total_words,2)
                    else:
                        prob+=p
                else:
                    prob+=q

    prob/=total
    prob=2**(-1*prob)
    return prob

if __name__=='__main__':
    s=time.clock()

    print()

    brown_corpus=list(brown.sents(brown.fileids()))
    for i in range(len(brown_corpus)):
        brown_corpus[i]=list(map(lambda x:x.lower(),brown_corpus[i]))
    brown_train,brown_test=train_test_split(brown_corpus,test_size=.1)
    unigram_probability,bigram_probability,total_words=calculate_probability(brown_train)
    print('Perpexility on Brown Corpus using bi-gram backoff',perpexility_backoff(brown_test,bigram_probability,unigram_probability,total_words))



    gutenberg_corpus=list(gutenberg.sents(gutenberg.fileids()))
    for i in range(len(gutenberg_corpus)):
        gutenberg_corpus[i]=list(map(lambda x:x.lower(),gutenberg_corpus[i]))
    gutenberg_train,gutenberg_test=train_test_split(gutenberg_corpus,test_size=.1)
    unigram_probability,bigram_probability,total_words=calculate_probability(gutenberg_train)
    print('Perpexility on Gutenberg Corpus using bi-gram backoff',perpexility_backoff(gutenberg_test,bigram_probability,unigram_probability,total_words))


    combined_corpus=brown_train+gutenberg_train
    unigram_probability,bigram_probability,total_words=calculate_probability(combined_corpus)
    print('Perpexility on brown test data using combined corpus for training',perpexility_backoff(brown_test,bigram_probability,unigram_probability,total_words))
    print('Perpexility on gutenberg test data using combined corpus for training',perpexility_backoff(gutenberg_test,bigram_probability,unigram_probability,total_words))

    print('Total time taken',time.clock()-s)