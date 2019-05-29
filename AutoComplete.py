from nltk.corpus import brown
from tkinter import *
from tkinter.ttk import Combobox

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
# Code from
# http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
# edited to use custom trie (prefix tree)
###############################################################################
class AutocompleteEntry(Entry):
    def __init__(self, trie, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.trie = trie
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
        return (self.find_sugg_rec(self.var.get()))

    def find_sugg_rec(self, word):
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
            wordlist.extend(self.find_sugg_rec(temp_word))

        return wordlist

if __name__ == '__main__':
    root = Tk()
    root.title("Auto Complete - CS173")
    root.geometry("250x250") #You want the size of the app to be 500x500
    root.resizable(0, 0) #Don't allow resizing in the x or y direction

    trie = make_trie(brown.words())
    entry = AutocompleteEntry(trie, root)
    entry.grid(row=250, column=250)
    Button(text='Search').grid(row=251, column=250)

    root.mainloop()

    # word = "auto"
    # print (find_suggestions(trie, word))
