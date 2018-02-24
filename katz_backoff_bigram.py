from nltk.corpus import gutenberg
from nltk.corpus import brown
import collections
import math
import time
from sklearn.cross_validation import train_test_split
import warnings
warnings.filterwarnings("ignore")

def magic(unigram_count,l):
    count=0
    for word in l:
        count+=unigram_count[tuple([word])]
    return count

def kartz_bigram(lam,corpus):
    vocabulary=set()
    alpha_bi=dict()
    unigram_count=dict()
    bigram_count=dict()
    bigram_dis_count=dict()
    word_follow_bi=collections.defaultdict(set)

    for sentences in corpus:
        words = sentences
        words = ['*'] + words + ['Stop']
        for index, token in enumerate(words):
            if (index >= 1 and index < len(words)):
                unigram_tuple = tuple([token])
                if unigram_tuple not in unigram_count:
                    unigram_count[unigram_tuple]=1
                    vocabulary.add(token)
                else:
                    unigram_count[unigram_tuple]+=1

            if (index >= 1 and index < len(words) - 1):
                bigram_tuple = tuple([token, words[index + 1]])
                if bigram_tuple not in bigram_count:
                    bigram_count[bigram_tuple]=1
                    tup=tuple([token])
                    word_follow_bi[tup].add(words[index+1])
                else:
                    bigram_count[bigram_tuple]+=1


    for bigram in bigram_count:
        bigram_dis_count[bigram] = bigram_count[bigram] - lam

    for word in vocabulary:
        tup=tuple([word])
        alpha_bi[tup]=(len(word_follow_bi[tup])*lam)/unigram_count[tup]

    return unigram_count,bigram_dis_count,alpha_bi,vocabulary,word_follow_bi

def katz_perpexility(test_data,unigram_count,bigram_dis_count,alpha_bi,vocabulary,word_follow_bi):
    vocab_total_unigram_count=0
    for word in vocabulary:
        vocab_total_unigram_count+=unigram_count[tuple([word])]
    total=0
    probability=0
    for sentences in test_data:
        words = sentences
        words = ['*'] + words + ['Stop']
        total += len(words)
        for index,token in enumerate(words):
            if(index>=1 and index<len(words)-1):
                bigram = tuple([token, words[index + 1]])
                unigram1=tuple([token])
                unigram2=tuple([words[index+1]])
                if bigram in bigram_dis_count:
                    #print(bigram)
                    probability+=math.log(bigram_dis_count[bigram]/unigram_count[tuple([token])],2)
                else:
                    if unigram1 in unigram_count and unigram2 in unigram_count:
                        probability+=math.log(alpha_bi[tuple([token])]*unigram_count[tuple([words[index+1]])]/(vocab_total_unigram_count-magic(unigram_count,word_follow_bi[tuple([token])])),2)
                    else:
                        probability+=math.log(1/vocab_total_unigram_count,2)
    probability /= total
    prob = 2 ** (-1 * probability)
    return prob







if __name__=='__main__':

    s=time.clock()

    brown_corpus = list(brown.sents(brown.fileids()))
    for i in range(len(brown_corpus)):
        brown_corpus[i] = list(map(lambda x: x.lower(), brown_corpus[i]))
    brown_train, part2 = train_test_split(brown_corpus, test_size=.2)
    brown_dev,brown_test=train_test_split(part2,test_size=.5)
    best_lamb = 1
    perpex_min = 100000
    for i in range(1, 10):
        unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi = kartz_bigram(i * .1, brown_train)
        perpex = katz_perpexility(brown_dev, unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi)
        if (perpex < perpex_min):
            best_lamb = i * .1
            perpex_min = perpex
    print('Best lambda obtain after cross validation on brown corpus', best_lamb)
    lamb_brown = best_lamb
    unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi = kartz_bigram(lamb_brown,
                                                                                         brown_train + brown_dev)
    print('Perpexility on Brown corpus using bi-gram katz\'s backoff',katz_perpexility(brown_test, unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi))
    print()




    gutenberg_corpus = list(gutenberg.sents(gutenberg.fileids()))
    for i in range(len(gutenberg_corpus)):
        gutenberg_corpus[i] = list(map(lambda x: x.lower(), gutenberg_corpus[i]))
    gutenberg_train, part1 = train_test_split(gutenberg_corpus, test_size=.2)
    gutenberg_dev,gutenberg_test=train_test_split(part1,test_size=.5)

    best_lamb = 1
    perpex_min = 100000
    for i in range(1, 10):
        unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi = kartz_bigram(i * .1, gutenberg_train)
        perpex = katz_perpexility(gutenberg_dev, unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi)
        if (perpex < perpex_min):
            best_lamb = i * .1
            perpex_min = perpex
    print('Best lambda obtain after cross validation on gutenberg corpus ', best_lamb)
    lamb_gut = best_lamb
    unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi = kartz_bigram(lamb_gut,gutenberg_train+gutenberg_dev)
    print('Perpexility on gutenburg corpus using bi-gram katz\'s backoff',katz_perpexility(gutenberg_test, unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi))
    print()







    combined_corpus=gutenberg_train+gutenberg_dev+brown_train+brown_dev
    unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi = kartz_bigram(lamb_brown,combined_corpus)
    print('Perpexility on Brown test data using training data of brown and gutenburg corpus',
          katz_perpexility(brown_test, unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi))
    print()
    unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi = kartz_bigram(lamb_gut, combined_corpus)
    print('Perpexility on Gutenburg test data using training data of brown and gutenburg corpus',
          katz_perpexility(gutenberg_test, unigram_count, bigram_dis_count, alpha_bi, vocabulary, word_follow_bi))
    print()



    print('Total time taken', time.clock() - s)