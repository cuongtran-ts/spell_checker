import copy, string, operator
import numpy as np
from collections import OrderedDict

DEFAULT_FILE_PATH = './text.txt'


def get_text_fr_file(file_path=DEFAULT_FILE_PATH):
    """
    Read a corpus from file and convert it to a string
    """
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')

    file.close()
    return data


def compute_word_freq(all_words):
    """

    Compute distribution of words in a corpus.
    Return a dictionary where keys are words, and values are frequencies

    """
    if len(all_words) < 1:
        print('Warning, empty corpus !')
        return {}

    unique_words = list(set(all_words.split(" ")))
    n = len(unique_words)
    freq_dict = OrderedDict()
    for a_word in unique_words:
        freq = all_words.count(a_word) / n
        freq_dict[a_word] = freq

    return freq_dict


def get_high_freq_word(word_freq_dict, outlier_threshold=0.05):
    """

    Get only high frequency words, consider typos as of words
    that have smallest frequency
    """

    all_words = word_freq_dict.keys()
    high_freq_word = copy.deepcopy(word_freq_dict)

    freq_threshold = np.percentile(np.asarray(list(word_freq_dict.values())), q=100 * outlier_threshold)

    if len(all_words) < 1:
        print('Warning, empty dictionary !')
        return {}

    for key in all_words:
        if word_freq_dict[key] < freq_threshold:
            del high_freq_word[key]

    return high_freq_word


def is_correct_word(a_word, word_freq_dict):
    """
    Checking if an entering word is a correct or typos
    """
    words = word_freq_dict.keys()

    if a_word in words:
        print('Correct word!')
    else:
        print('Warning a typo!')


def insert_character(a_word, c, position=0):
    """
    Insert a character to a word at position
    """
    n = len(a_word)
    if (position >= n + 1) or (position < 0):
        print('Warning out of range, cannot insert ')
        return ""
    return a_word[:position] + c + a_word[position:]


def replace_character(a_word, c, position=0):
    '''
    Replace a character at position in a word by a given character
    '''
    n = len(a_word)
    if (position >= n) or (position < 0):
        print('Warning out of range, cannot insert ')
        return ""
    return a_word[:position] + c + a_word[position + 1:]


def del_character(a_word, position=0):
    '''
    Delete one character from a given word at the given position
    '''
    n = len(a_word)
    if (position >= n) or (position < 0):
        print('Warning out of range, cannot insert ')
        return ""
    return a_word[:position] + a_word[position + 1:]


def suggest_correct_spelling(a_word, word_freq_dict):
    '''
    Suggest a correct spelling for a typing word.
    If we can find several words  in a dictionary that closely match with given word
    then return the one that has the highest frequency.

    '''

    possible_matchings = {}
    for i in range(len(a_word)):

        temp_word = del_character(a_word, position=i)
        if temp_word in word_freq_dict.keys():
            possible_matchings[temp_word] = word_freq_dict[temp_word]
            # return temp_word

        for c in alphabet:
            temp_word = insert_character(a_word, c, position=i)
            if temp_word in word_freq_dict.keys():
                possible_matchings[temp_word] = word_freq_dict[temp_word]
                # return temp_word

            temp_word = replace_character(a_word, c, position=i)
            if temp_word in word_freq_dict.keys():
                possible_matchings[temp_word] = word_freq_dict[temp_word]
                # return temp_word

    if len(possible_matchings.keys()) < 1:
        return 'Cannot suggest correct words'
    else:
        # return the word with highest frequency
        return max(possible_matchings.items(), key=operator.itemgetter(1))[0]
