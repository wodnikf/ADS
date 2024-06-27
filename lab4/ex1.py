import numpy as np
from collections import defaultdict

def levensthein_d(text1, text2):
    matrix = np.zeros((len(text1) + 1, len(text2) + 1), dtype=int)
    for i in range(len(text1) + 1):
        matrix[i, 0] = i
    
    for j in range(len(text2) + 1):
        matrix[0, j] = j
        
    for i in range(1, len(text1) + 1):
        for j in range(1, len(text2) + 1):
            if text1[i-1] == text2[j-1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            matrix[i, j] = min(matrix[i-1, j] + 1, matrix[i, j-1] + 1, matrix[i-1, j-1] + substitution_cost)
    
    return matrix[len(text1), len(text2)]


def hamming_d(text1, text2):
    if len(text1) != len(text2):
        raise ValueError("Strings must be of equal length")
    distance_counter = 0
    for i in range(len(text1)):
        if text1[i] != text2[i]:
            distance_counter += 1
    
    return distance_counter

def indel_d(text1, text2):
    matrix = np.zeros((len(text1) + 1, len(text2) + 1))
    for i in range(len(text1) + 1):
        matrix[i, 0] = i
    
    for j in range(len(text2) + 1):
        matrix[0, j] = j
        
    for i in range(1, len(text1) + 1):
        for j in range(1, len(text2) + 1):
            if text1[i-1] == text2[j-1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = 1 + min(matrix[i - 1][j], matrix[i][j - 1])
    
    return matrix[len(text1), len(text2)]

keybord_neighbourhood = {
    'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'erfcxs', 'e': 'rdsw', 'f': 'rtgvcd', 'g': 'tyhbvf',
    'h': 'yujnbg', 'i': 'uojkl', 'j': 'uikmnh', 'k': 'iolmj', 'l': 'opk', 'm': 'njk', 'n': 'bhjm',
    'o': 'ipkl', 'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'wedxz', 't': 'rfgy', 'u': 'yhji', 'v': 'cfgb',
    'w': 'qase', 'x': 'zsdc', 'y': 'tghu', 'z': 'asx'
}

def weight_sub_cost(char1, char2):
    if char1 == char2:
        return 0
    elif char2 in keybord_neighbourhood.get(char1, ''):
        return 0.5
    else:
        return 1

def modified_levensthein_d(text1, text2):
    matrix = np.zeros((len(text1) + 1, len(text2) + 1))
    for i in range(len(text1) + 1):
        matrix[i, 0] = i
    
    for j in range(len(text2) + 1):
        matrix[0, j] = j
        
    for i in range(1, len(text1) + 1):
        for j in range(1, len(text2) + 1):
            if text1[i - 1] == text2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]    
            else:
                matrix[i, j] = min(matrix[i-1, j] + 1, matrix[i, j-1] + 1, matrix[i-1, j-1] + weight_sub_cost(text1[i - 1], text2[j - 1]))
    
    return matrix[len(text1), len(text2)]

def modified_hamming_d(text1, text2):
    if len(text1) != len(text2):
        raise ValueError("Strings must be of equal length")
    distance = 0
    for i in range(len(text1)):
        if text1[i] != text2[i]:
            distance += weight_sub_cost(text1[i], text2[i])
    
    return distance

def load_words(file_path):
    with open(file_path) as file:
        words = file.read().split()
    return words

def suggest_word(incorrect_word, word_list):
    min_distance = float("inf")
    suggested_word = None
    
    for word in word_list:
        distance = modified_levensthein_d(incorrect_word, word)
        if distance < min_distance:
            min_distance = distance
            suggested_word = word
            
    return suggested_word

def correct_text_file(input_file_path, output_file_path, words_list):
    with open(input_file_path) as file:
        text = file.read()
        
    words = text.split()
    corrected_words = [suggest_word(word, words_list) for word in words]
    corrected_text = ' '.join(corrected_words)
    
    with open(output_file_path, 'w') as file:
        file.write(corrected_text)

def build_length_based_dict(word_list):
    length_dict = defaultdict(list)
    for word in word_list:
        length_dict[len(word)].append(word)
    return length_dict

def suggest_word_optimized(incorrect_word, length_dict):
    min_distance = float('inf')
    suggested_word = None
    word_length = len(incorrect_word)
    
    possible_words = length_dict[word_length] + length_dict[word_length - 1] + length_dict[word_length + 1]
    
    for word in possible_words:
        distance = modified_levensthein_d(incorrect_word, word)
        if distance < min_distance:
            min_distance = distance
            suggested_word = word
    
    return suggested_word

def correct_text_optimized(input_file_path, output_file_path, length_dict):
    with open(input_file_path) as file:
        text = file.read()
        
    words = text.split()
    corrected_words = [suggest_word_optimized(word, length_dict) for word in words]
    corrected_text = ' '.join(corrected_words)
    
    with open(output_file_path, 'w') as file:
        file.write(corrected_text)

words_list = load_words("words_alpha.txt")
length_dict = build_length_based_dict(words_list)

correct_text_optimized("in.txt", "out.txt", length_dict)
