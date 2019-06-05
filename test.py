
unigrams = {("hello",):1, ("world",):4, ("my",):6 ,("i",):8, ("you",):10}

start = [tuple([k,v]) for k,v in unigrams.items()]

start = sorted(start, key = lambda x: x[1], reverse=True)

bigrams = {("i", "love"):4, ("i", "hate"):4, ("hello","there"):6, ("world", "is"):8, 
            ("hello", "world"):10, ("my", "name"):7, ("hello","my"): 10, ("you","are"): 20,
            ("you","and"): 2,
            ("are","my"):10,("my","fire"):20}

trigrams = {("i","love","you"):4, ("i","love","my"):3, ("i","hate","you"):1, ("hello","there","my"):6, 
            ("hello","world","my"):5, ("my","name","is"):7, ("hello","my","name"): 1}

#build a dict of possible unigrams {($,): [next possible word]}

def build_lookup():
    test = {}
    for y in bigrams.keys():
        if y[:1] not in test: 
            l = []
            for x in bigrams.keys():
                if x[:1] == y[:1]:
                    l.append(x[1])
            test[y[:1]] = l
    return test

bi_words = build_lookup()

#build a dict of possible bigrams {(word,): [next possible word]}
#bi_words = {x[:1]: [y[1] for y in bigrams.keys() if x[:1] == y[:1] ] for x in bigrams.keys()}
#print(bi_words)
#build a dict of possible trigrams{(word,word): [next possible word]}
#tri_words = {x[:2]:[y[2] for y in trigrams.keys() if x[:2] == y[:2]] for x in trigrams.keys()}

def make_tup(*argv):
    return tuple([arg for arg in argv])

def P_bigram(*argv):
    tup = make_tup(*argv)
    try:
        return bigrams[tup]
    except KeyError:
        return 0

class MarkovModel():
    def __init__(self):
        pass

    def predict(self,chain,count):
        if count < 1:
            return chain
        else:
            last = chain[-1]
            poss = bi_words[make_tup(last)]
            poss = [make_tup(x,P_bigram(last,x)) for x in poss]
            poss = sorted(poss, key = lambda x: x[1], reverse=True)
            chain.append(poss[0][0])
        return self.predict(chain,count-1)
            


mc = MarkovModel()
chain = ["you"]
chain = mc.predict(chain,2)
print(chain)


