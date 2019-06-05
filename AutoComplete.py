from nltk.corpus import brown
from nltk import ngrams
from tkinter import *
from tkinter.ttk import Combobox
from collections import Counter
import numpy

print ("**************************************")
print ("Auto-Complete (CS173 - Assignment 5)")
print ("[Using the Brown corpus]")
print ("**************************************")

###############################################################################
# Makes a custom trie using python dict
###############################################################################
def make_trie(*wordlist):
     start = dict()
     words = wordlist[0]
     for word in words:
         current_dict = start
         for letter in word:
             current_dict = current_dict.setdefault(letter, {})
         current_dict['$'] = '$'
     return start

###############################################################################
#Reverse Index For Ngrams Creater
###############################################################################
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
        if start not in bigram_count_index.keys():
            bigram_count_index[start] = {} #add if to bigram_count_index
        count = 0
        if end in bigram_count_index[start].keys():
            count = bigram_count_index[start][end]
        bigram_count_index[start][end] = count + 1

    for key in bigram_count_index.keys():
        sum_for_key = sum_ngram_counts(bigram_count_index, key)
        if (key not in bigram_prob_index.keys()):
            bigram_prob_index[key] = {}
        for second in bigram_count_index[key].keys():
            if (second not in bigram_prob_index[key].keys()):
                bigram_prob_index[key][second] = {}
            bigram_prob_index[key][second] = bigram_count_index[key][second] / sum_for_key
    return bigram_prob_index

###############################################################################
# Autocompleter Class definition
###############################################################################
class AutoCompleter():
    def __init__(self, data):
        self.trie = make_trie(data)
        self.phrase = []
        self.unigram_prob_index = reverseIndex1gram(ngrams(data,1))
        self.bigram_prob_index = reverseIndex2gram(ngrams(data,2))
        print("Auto Completer Set up")
    
    def predict(self,chain,count):
        if count < 1:
            return chain
        else:
            last = chain[-1]
            probs = self.bigram_prob_index[last]
            sorted_probs = sorted(probs.items(), key=lambda kv: kv[1],reverse=True)
            chain.append(sorted_probs[0][0])
        return self.predict(chain,count-1)

    def suggester(self, input):
        input_words = input.split()
        if input_words == []:
            return []  
        #grab the current word being created
        lastword = input_words[-1]
        #grab the list of suggested words
        singlewordsuggs = (self.trie_suggester(lastword))
        #
        suggs = [tuple([s,self.unigram_prob_index[s]]) for s in singlewordsuggs]
        sorted_suggs = sorted(suggs, key=lambda kv: kv[1],reverse=True)
        top5 = [x[0] for x in sorted_suggs[:5]]
        phrases = []
        for t in top5:
            temp = self.predict(input_words[:-1] + [t],3)
            phrases.append(' '.join(temp))
        
        return phrases

    def trie_suggester(self, word):
        wordlist = []
        sub_trie = self.trie
        for letter in word:
            if letter in sub_trie:
                sub_trie = sub_trie[letter]
            else:
                return wordlist

        for section in sub_trie.keys():
            if (section == '$'):
                wordlist.append(word)
                continue
            temp_word = word + section
            wordlist.extend(self.trie_suggester(temp_word))

        return wordlist

###############################################################################
# Code from
# http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
# edited to use custom autocompletion
###############################################################################
class AutocompleteEntry(Entry):
    def __init__(self, data, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.completer = AutoCompleter(data)

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.find_suggestions()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def find_suggestions(self):
        return (self.completer.suggester(self.var.get()))


if __name__ == '__main__':
    data = brown.words()

    root = Tk()
    root.title("Auto Complete - CS173")
    root.geometry("250x250") #You want the size of the app to be 500x500
    root.resizable(0, 0) #Don't allow resizing in the x or y direction

    entry = AutocompleteEntry(data, root)
    entry.grid(row=250, column=250)
    Button(text='Search').grid(row=251, column=250)

    root.mainloop()

    # word = "auto"
    # print (find_suggestions(trie, word))
