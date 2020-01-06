import string
from itertools import combinations

dictionary = dict()
boards = dict()


## Load a word list from a file. This is only used for testing
def LoadWordList():
    words = list()
    with open("wordlist.txt") as wordList:
        for word in wordList:
            word = word[0:-1]
            if len(word) > 3:
                uniqueLetters = "".join(set(word))
                uniqueSorted = "".join(sorted(uniqueLetters))                
                words.append([word, uniqueSorted])
    return words

## Calculate the score for a set of letters against a word list
## This is used to check results
def TestLetters(wordList, letters, centerLetter):
    score = 0
    for w in wordList:
        if ContainsAll(w[1], centerLetter):
            if ContainsAll(letters, w[1]):
                print("{}".format(w[0]))
                score += CalcWordScore(w[0], w[1])
    print("String '{}' with center letter '{}' scores {}".format(
        letters, centerLetter, score))        


## Calculate a word's Spelling Bee score
def CalcWordScore(word, unique):
    if len(word) == 4:
        return 1
    score = len(word)
    if len(unique) == 7:
        score += 7
    return score


## Load a word list and generate a dictionary object that's easily 
## searchable by setting the dictionary keys to the sorted unique letters
## from each word
def GenerateDict():
    with open("wordlist.txt") as wordList:
        for word in wordList:
            word = word[0:-1]
            wordLength = len(word)
            ## Disregard any words that are 3 letters or less or have an S in them
            if 's' not in word and wordLength > 3:
                ## Find the unique letters in the word and sort them
                ## This greatly reduces the potential search space
                uniqueLetters = "".join(sorted(set(word)))
                numUniqueLetters = len(uniqueLetters)

                ## Disregard any words with more than 7 unique letters
                if numUniqueLetters <= 7:
                    score = CalcWordScore(word, uniqueLetters)

                    # If the key already exists, then add to the score 
                    # expected wih this set of unique letters
                    # Otherwise, create a new dictionary entry
                    if uniqueLetters in dictionary:
                        dictionary[uniqueLetters]['score'] = dictionary[uniqueLetters]['score'] + score
                        dictionary[uniqueLetters]['words'] = dictionary[uniqueLetters]['words'] + 1
                    else:
                        dictionary[uniqueLetters] = {'score' : score, 
                        'num_letters': numUniqueLetters, 'words' : 1}
    return dictionary


## Given a string of letters, and a single letter that must be included
## generate all possible sorted combinations of letters
## These values represent potential keys to check for in the dictionary
## For the Spelling Bee, there are 63 combinations of unique letters for 
## each board
def GenerateKeys(letters, mustInclude):
    k = list()
    s1 = letters.replace(mustInclude, '')
    for i in range(1, len(s1)):
        for c in combinations(s1, i):
            t = "".join(c) + mustInclude
            k.append("".join(sorted(t)))
    k.append(letters)
    return k

## Find all sets of 7 unique letters in the dictionary and use
## these as potential Spelling Bee boards
def GenerateBoards():
    global boards
    for key, val in dictionary.items():
        if val['num_letters'] == 7:
            boards[key] = []

## For every possible board, calculate the score for each board with
## each letter as the center letter. (I.e. for every board, there are 7 scores)
def CalcBoardScores():
    global boards
    ## the key is the string of unique letters
    for key, val in boards.items():
        for centerLetter in key:
            dictKeys = GenerateKeys(key, centerLetter)
            score = 0
            for k in dictKeys:
                try:
                    ## If the key exists in the dictionary, add the score for those letters
                    score += dictionary[k]['score']
                except:
                    pass
            boards[key].append( score )
    return boards


## Sort the boards by score
def SortBoards():
    scores = list()
    for key, val in boards.items():
        for i, s in enumerate(boards[key]):
            scores.append([key, key[i], s ])
    scores = sorted(scores, key = lambda x: x[2])
    return scores


if __name__ == "__main__":
    # execute only if run as a script
    GenerateDict()
    GenerateBoards()
    CalcBoardScores()
    scores = SortBoards()
    with open('boardscores.txt', 'w') as f:
        for s in scores:
            f.write("{} {} {}\n".format(s[0], s[1], s[2]))
