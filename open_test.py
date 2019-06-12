filename = "hi.txt"
import io
words_list = []
with io.open(filename, 'r', encoding='iso-8859-15') as f:
    words_list = [word for line in f for word in line.split()]
print(words_list)