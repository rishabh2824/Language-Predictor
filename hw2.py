import sys
import math
import re

"""
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    described in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    """


def get_parameter_vectors():
    # Implementing vectors e,s as lists (arrays) of length 26
    # with p[0] being the probability of 'A' and so on
    e = [0] * 26
    s = [0] * 26

    with open('e.txt', encoding='utf-8') as f:
        for line in f:
            char, prob = line.strip().split(" ")
            e[ord(char) - ord('A')] = float(prob)
    f.close()

    with open('s.txt', encoding='utf-8') as f:
        for line in f:
            char, prob = line.strip().split(" ")
            s[ord(char) - ord('A')] = float(prob)
    f.close()

    return e, s


"""Shreds the file and returns a hashmap with occurrences of each letter"""


def shred(filename):
    # Using a dictionary here.
    X = dict()
    with open(filename, encoding='utf-8') as f:
        text = f.read()

        # Regex for stripping everything except for letters. CITATION - CHATGPT
        # PROMPT - How to remove all characters other than letters in python
        letters = re.sub(r'[^a-zA-Z]', '', text).upper()

        for letter in letters:
            if letter in X:
                X[letter] += 1
            else:
                X[letter] = 1
    return X


"""Calculates the conditional probability. Takes the below inputs as parameters:
letterCounts - Dictionary containing all the letters and their respective counts
englishPriorProb - The prior probability of english P(Y = English)
spanishPriorProb - The prior probability of spanish P(Y = Spanish)"""


def conditionalProbability(letterCounts, englishPriorProb, spanishPriorProb):
    # get the parameter vectors
    e, s = get_parameter_vectors()

    # Start building F(X)
    F_English = math.log(englishPriorProb)
    F_Spanish = math.log(spanishPriorProb)

    # Loop through each letter
    for i in range(26):
        # Calculate the correct index for hashmap and handle missing letters
        char = chr(i + ord('A'))
        occurrences = letterCounts.get(char, 0)

        if occurrences > 0:
            englishProbability = math.log(e[i])
            spanishProbability = math.log(s[i])

            F_English += occurrences * englishProbability
            F_Spanish += occurrences * spanishProbability

    # Calculate the difference for edge cases
    delta_F = F_Spanish - F_English

    # Check edge cases
    if delta_F >= 100:
        englishConditionalProbability = 0
    elif delta_F <= -100:
        englishConditionalProbability = 1
    else:
        # Regular Case
        englishConditionalProbability = 1 / (1 + math.exp(delta_F))

    return F_English, F_Spanish, englishConditionalProbability


"""Main method"""


def main():
    filename = sys.argv[1]
    englishPriorProb = float(sys.argv[2])
    spanishPriorProb = float(sys.argv[3])

    # Q1 - Print all letters and their occurrences
    letterCounts = shred(filename)
    print("Q1")
    for letter in range(26):
        char = chr(letter + ord('A'))
        print(f"{char} {letterCounts.get(char, 0)}")

    # Q2
    e, s = get_parameter_vectors()
    countOfA = letterCounts.get('A', 0)

    englishQ2 = countOfA * math.log(e[0])
    spanishQ2 = countOfA * math.log(s[0])

    print("Q2")
    print(f"{englishQ2:.4f}")
    print(f"{spanishQ2:.4f}")

    # Q3 - Print F_English and F_Spanish with 4 decimal places
    F_English, F_Spanish, englishConditionalProbability = conditionalProbability(letterCounts, englishPriorProb,
                                                                                 spanishPriorProb)
    print("Q3")
    print(f"{F_English:.4f}")
    print(f"{F_Spanish:.4f}")

    # Q4 - Print the conditional probability for english
    print("Q4")
    print(f"{englishConditionalProbability:.4f}")


if __name__ == '__main__':
    main()
