from nltk.corpus import brown
from nltk import ngrams
import numpy as np

def sum_ngram_counts(ngram_dict, key):
    total = 0
    for k in ngram_dict[key].keys():
        total = total + ngram_dict[key][k]
    return total

def reverseIndex1gram(unigrams):
    unigram_count_index = {}
    unigram_prob_index = {}

    total = 0
    for unigram in unigrams:
        start = unigram[0]
        if start not in unigram_count_index.keys():
            unigram_count_index[start] = 1 #add if to bigram_count_index
        else:
            unigram_count_index[start] +=1
        total +=1
    for key in unigram_count_index.keys():
        unigram_prob_index[key] = unigram_count_index[key]/total
    return unigram_prob_index

def reverseIndex2gram(bigrams):
    bigram_count_index = {}
    bigram_prob_index = {}

    for bigram in bigrams:
        start = bigram[0]
        end = bigram[1]
        key = tuple([start])
        if key not in bigram_count_index.keys():
            bigram_count_index[key] = {} #add if to bigram_count_index
        count = 0
        if end in bigram_count_index[key].keys():
            count = bigram_count_index[key][end]
        bigram_count_index[key][end] = count + 1

    for key in bigram_count_index.keys():
        sum_for_key = sum_ngram_counts(bigram_count_index, key)
        if (key not in bigram_prob_index.keys()):
            bigram_prob_index[key] = {}
        for second in bigram_count_index[key].keys():
            if (second not in bigram_prob_index[key].keys()):
                bigram_prob_index[key][second] = {}
            bigram_prob_index[key][second] = bigram_count_index[key][second] / sum_for_key
    return bigram_prob_index

def reverseIndex3gram(trigrams):
    trigram_count_index = {}
    trigram_prob_index = {}
    for trigram in trigrams:
        start = trigram[0]
        mid = trigram[1]
        end = trigram[2]
        key = tuple([start,mid])
        if key not in trigram_count_index.keys():
            trigram_count_index[key] = {} #add if to bigram_count_index
        count = 0
        if end in trigram_count_index[key].keys():
            count = trigram_count_index[key][end]
        trigram_count_index[key][end] = count + 1

    for key in trigram_count_index.keys():
        sum_for_key = sum_ngram_counts(trigram_count_index, key)
        if (key not in trigram_prob_index.keys()):
            trigram_prob_index[key] = {}
        for second in trigram_count_index[key].keys():
            if (second not in trigram_prob_index[key].keys()):
                trigram_prob_index[key][second] = {}
            trigram_prob_index[key][second] = trigram_count_index[key][second] / sum_for_key
    return trigram_prob_index

unigrams = [("i",), 
            ("i",), 
            ("i",),
            ("you",),
            ("hello",),
            ("bye",),
            ("try",),
            ("is",),
            ("is",),
            ("it",),
            ("it",),
            ("it",),
            ("it",)] 

bigrams = [("i", "love"), 
            ("i", "hate"), 
            ("i", "hate"),
            ("hello","there"), 
            ("hello","there"), 
            ("hello", "world"), 
            ("hello","my"), 
            ("world", "is"), 
            ("you","and"),
            ("you","are"),
            ("you","are"),
            ("you","are"),
            ("you","are"),
            ("you","are"),
            ("you","are"),
            ("are","my"),
            ("my", "name"), 
            ("my","fire"),
            ("my","fire"),
            ("my","fire"),
            ("my","fire"),
            ("my","fire"),
            ("fire","my"),
            ("fire","my"),
            ("fire","my"),
            ("fire","my"),
            ("hate", "you"),
            ("hate", "you"),]

trigrams = [("i", "love","you"), 
            ("i", "hate","me"), 
            ("i", "hate","you"),
            ("you","and","i"),
            ("you","and","me"),
            ("hello","there","obi"), 
            ("hello","there","wan")]

#data = brown.words()
#bigrams = ngrams(data,2)
#trigrams = ngrams(data,3)

unigram_prob_index= reverseIndex1gram(unigrams)
bigram_prob_index = reverseIndex2gram(bigrams)
trigram_prob_index = reverseIndex3gram(trigrams)

def P(*argv):
    try:
        if len(argv) == 1:
            return unigram_prob_index[argv[0]]
        elif len(argv) == 2:
            key = tuple([argv[0]])
            return bigram_prob_index[start][argv[1]]
    except KeyError:
        return np.finfo(float).tiny 

def predict_list(words):
    try:
        if len(words) == 1:
            return bigram_prob_index[words]
        elif len(words) == 2:
            return trigram_prob_index[words]
    except KeyError:
        return {}

def predict_chain(chain,count):
    if count < 1:
        return chain
    else:
        last = tuple([ chain[-1] ])
        probs = predict_list(last)
        if probs:
            sorted_probs = sorted(probs.items(), key=lambda kv: kv[1],reverse=True)
            chain.append(sorted_probs[0][0])
    return predict_chain(chain,count-1)

def suggester(input):
    input_words = input.split()
    if input_words == []:
        return []  
    #grab the current word being created
    lastword = input_words[-1]
    #grab the list of suggested words
    singlewordsuggs = ["i","you","hello"]
    top5 = []
    if(len(input_words)) <  2: #calculate the unigram probability
        suggs = [tuple([s,P(s)]) for s in singlewordsuggs]
        sorted_suggs = sorted(suggs, key=lambda kv: kv[1],reverse=True)
        top5 = [x[0] for x in sorted_suggs[:5]]
    elif (len(input_words)) <  3:   #calculate the bigram probability
        suggs = [tuple([s, P(lastword,s)]) for s in singlewordsuggs]
        sorted_suggs = sorted(suggs, key=lambda kv: kv[1],reverse=True)
        top5 = [x[0] for x in sorted_suggs[:5]]
    else: #try to use trigrams
        suggs = [tuple([s, P(input_words[-2],lastword,s)]) for s in singlewordsuggs]
        sorted_suggs = sorted(suggs, key=lambda kv: kv[1],reverse=True)
        top5 = [x[0] for x in sorted_suggs[:5]]

    phrases = []
    for t in top5:
        temp = predict_chain(input_words[:-1] + [t],3)
        phrases.append(' '.join(temp))
    
    return phrases

phrases = suggester("$")
print(phrases)