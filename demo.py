from spellchecker import *

all_words = get_text_fr_file(file_path='./short_corpus.txt')
word_freq_dict = compute_word_freq(all_words)
word_freq_dict =  get_high_freq_word(word_freq_dict)
input_text ='booke'

if is_correct_word(input_text, word_freq_dict):
    print ('Found on dictionary, correct word !')
else:
    print('A typo !')


print(suggest_correct_spelling(input_text, word_freq_dict))




