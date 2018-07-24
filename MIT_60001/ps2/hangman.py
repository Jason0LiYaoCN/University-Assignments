# -*- coding: UTF-8 -*- 
# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import os
WORDLIST_FILENAME = "D:/Programming/University-Assignments/MIT_60001/ps2/words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for letters in secret_word:
      if letters not in letters_guessed:
        return False
    return True
# secret_word = 'naive'
# letters_guessed = []
# print(is_word_guessed(secret_word, letters_guessed))



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    final_string = []
    for count in range(len(secret_word)):
      final_string.append('_ ')    
    counter = 0
    for letters in secret_word:
      if letters in letters_guessed:
        final_string[counter] = letters
      counter += 1
    final_str = ''.join(final_string)
    return final_str

# secret_word = 'apple'
# letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
# print(get_guessed_word(secret_word, letters_guessed))

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    stra2z = "abcdefghijklmnopqrstuvwxyz"
    stra2z = list(stra2z)
    for letters in letters_guessed:
      if letters in stra2z:
        stra2z.pop(stra2z.index(letters))
    return ''.join(stra2z)

# letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
# print(get_available_letters(letters_guessed))
    
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # print(secret_word)
    unique = set(secret_word)
    unique_len = len(unique)
    vowels = ['a', 'e', 'i', 'o', 'u']
    num_guess = 6
    num_warning = 3
    Game_end = False
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %d letters long." % len(secret_word))
    while not Game_end:
      print("-------------")
      if(is_word_guessed(secret_word, letters_guessed)):
        total_score = num_guess * unique_len
        print("Congratulations, you won!")
        print("Your total score for this game is: %d" % total_score)
        Game_end = True
        break
      print("You have %d guesses left." % num_guess)
      print("Available letters: %s" % get_available_letters(letters_guessed))
      guessed_letter = input("Please guess a letter:")
      # decide whether the input is valid or not
      if not str.isalpha(guessed_letter) or len(guessed_letter) > 1:
        if num_warning > 0:
          num_warning = num_warning - 1
          print("Oops! That is not a valid letter. You have %d warnings left: %s" % (num_warning, get_guessed_word(secret_word, letters_guessed)))
        else :
          if num_guess > 0:
            print("Oops! That is not a valid letter. You have no warnings left")
            print("so you lose one guess: %s" % get_guessed_word(secret_word, letters_guessed))
            num_guess = num_guess - 1
            continue
          else:
            print("Sorry, you ran out of guesses. The word was else.")
            Game_end = True
            break
      guessed_letter = str.lower(guessed_letter)
      if guessed_letter in letters_guessed :
        if num_warning > 0:
          num_warning = num_warning - 1
          print("Oops! You've already guessed that letter. You have %d warnings left :" % num_warning)
          print("%s" % get_guessed_word(secret_word, letters_guessed))
        else:
          if num_guess > 0:
            print("Oops! You've already guessed that letter.You have no warnings left")
            print("so you lose one guess: %s" % get_guessed_word(secret_word, letters_guessed))
            num_guess = num_guess - 1
            continue
          else:
            print("Sorry, you ran out of guesses. The word was else.")
            Game_end = True
            break
      else:
        letters_guessed.append(guessed_letter)
        if guessed_letter in secret_word:
          print("Good guess:%s" % get_guessed_word(secret_word, letters_guessed))
          continue
        else:
          if guessed_letter in vowels:
            if num_guess > 1:
              print("Oops! That letter is not in my word: %s" % get_guessed_word(secret_word, letters_guessed))
              num_guess = num_guess -2
              continue
            else:
              print("Sorry, you ran out of guesses. The word was else.")
              Game_end = True
              break
          else:
            if num_guess > 0:
              print("Oops! That letter is not in my word: %s" % get_guessed_word(secret_word, letters_guessed))
              num_guess = num_guess -1
              continue
            else:
              print("Sorry, you ran out of guesses. The word was else.")
              Game_end = True
              break


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    final_str_list = []
    count = 0
    for word in my_word:
      if word != ' ':
        final_str_list.append(word)
    final_str = ''.join(final_str_list)
    if len(final_str) != len(other_word):
      return False
    for letters in final_str:
      if letters == '_':
        count = count + 1
        continue
      if letters != other_word[count]:
        return False
      count = count + 1
    return True

# print(match_with_gaps("ta_ t", "tact"))
      



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    output_list = []
    for other_word in wordlist:
      if match_with_gaps(my_word, other_word):
        output_list.append(other_word + ' ')
    if len(output_list) == 0:
      print("No matches found")
    else:
      print(''.join(output_list))

# show_possible_matches("t_ _ t")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    unique = set(secret_word)
    unique_len = len(unique)
    vowels = ['a', 'e', 'i', 'o', 'u']
    num_guess = 6
    num_warning = 3
    Game_end = False
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %d letters long." % len(secret_word))
    while not Game_end:
      print("-------------")
      if(is_word_guessed(secret_word, letters_guessed)):
        total_score = num_guess * unique_len
        print("Congratulations, you won!")
        print("Your total score for this game is: %d" % total_score)
        Game_end = True
        break
      print("You have %d guesses left." % num_guess)
      print("Available letters: %s" % get_available_letters(letters_guessed))
      guessed_letter = input("Please guess a letter:")
      # decide whether the input is valid or not
      if guessed_letter == '*':
        print("Possible word matches are:")
        show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        continue
      if not str.isalpha(guessed_letter) or len(guessed_letter) > 1:
        if num_warning > 0:
          num_warning = num_warning - 1
          print("Oops! That is not a valid letter. You have %d warnings left: %s" % (num_warning, get_guessed_word(secret_word, letters_guessed)))
        else :
          if num_guess > 0:
            print("Oops! That is not a valid letter. You have no warnings left")
            print("so you lose one guess: %s" % get_guessed_word(secret_word, letters_guessed))
            num_guess = num_guess - 1
            continue
          else:
            print("Sorry, you ran out of guesses. The word was else.")
            Game_end = True
            break
      guessed_letter = str.lower(guessed_letter)
      if guessed_letter in letters_guessed :
        if num_warning > 0:
          num_warning = num_warning - 1
          print("Oops! You've already guessed that letter. You have %d warnings left :" % num_warning)
          print("%s" % get_guessed_word(secret_word, letters_guessed))
        else:
          if num_guess > 0:
            print("Oops! You've already guessed that letter.You have no warnings left")
            print("so you lose one guess: %s" % get_guessed_word(secret_word, letters_guessed))
            num_guess = num_guess - 1
            continue
          else:
            print("Sorry, you ran out of guesses. The word was else.")
            Game_end = True
            break
      else:
        letters_guessed.append(guessed_letter)
        if guessed_letter in secret_word:
          print("Good guess:%s" % get_guessed_word(secret_word, letters_guessed))
          continue
        else:
          if guessed_letter in vowels:
            if num_guess > 1:
              print("Oops! That letter is not in my word: %s" % get_guessed_word(secret_word, letters_guessed))
              num_guess = num_guess -2
              continue
            else:
              print("Sorry, you ran out of guesses. The word was else.")
              Game_end = True
              break
          else:
            if num_guess > 0:
              print("Oops! That letter is not in my word: %s" % get_guessed_word(secret_word, letters_guessed))
              num_guess = num_guess -1
              continue
            else:
              print("Sorry, you ran out of guesses. The word was else.")
              Game_end = True
              break



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints('apple')
